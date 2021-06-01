import numpy as np
import copy as cp
import pandas as pd
import time
import pickle
import os

from Predictor.models import PredictionType
from dataConnector.models import Candle
from dataConnector.submodels import ExchangeInfo


class Learning:

    def __init__(self, pair_symbol, interval, window_size=60, response_size=5):
        candles = Candle.objects.filter(symbol=pair_symbol,
                                        is_real=True,
                                        interval=interval).order_by('open_time').defer('symbol', 'interval', 'is_real',
                                                                                       'prediction_type')
        self.pair_symbol = pair_symbol
        self.interval = interval
        self.window_size = window_size
        self.response_size = response_size
        self.file_path = self.pair_symbol + '_' + self.interval + '_mlr_with_windows_' + self.window_size.__str__() \
                         + '-' + self.response_size.__str__() + '.pkl'

        self.candles = pd.DataFrame(candles)

        delta_t = np.array(
            [(self.candles.close_time[i] + 1 - self.candles.open_time[i]) for i in range(len(self.candles))])
        delta_t = np.concatenate((np.array([0]), delta_t))

        self.candles.insert(1, '∆t', delta_t)
        # self.candles.head(3)

        candles_count = candles.count()
        trainset = candles.iloc[:round(candles_count * 0.75)]
        testset = candles.iloc[round(candles_count * 0.75):]

        # Create Windows
        train_constructor = WindowSlider(self.window_size, self.response_size)
        self.train_windows = train_constructor.collect_windows(trainset.iloc[:, 1:], previous_y=False)

        test_constructor = WindowSlider(self.window_size, self.response_size)
        self.test_windows = test_constructor.collect_windows(testset.iloc[:, 1:], previous_y=False)

        train_constructor_y_inc = WindowSlider(self.window_size, self.response_size)
        self.train_windows_y_inc = train_constructor_y_inc.collect_windows(trainset.iloc[:, 1:], previous_y=True)

        test_constructor_y_inc = WindowSlider(self.window_size, self.response_size)
        self.test_windows_y_inc = test_constructor_y_inc.collect_windows(testset.iloc[:, 1:], previous_y=True)

        # train_windows.head(3)

    def learn_mlr_with_windows(self):
        from sklearn.linear_model import LinearRegression
        lr_model = LinearRegression()
        lr_model.fit(self.train_windows.iloc[:, :-1], self.train_windows.iloc[:, -1])

        t0 = time.time()
        lr_y = self.test_windows['y'].values
        lr_y_fit = lr_model.predict(self.train_windows.iloc[:, :-1])
        lr_y_pred = lr_model.predict(self.test_windows.iloc[:, :-1])
        tf = time.time()

        lr_residuals = lr_y_pred - lr_y
        lr_rmse = np.sqrt(np.sum(np.power(lr_residuals, 2)) / len(lr_residuals))
        lr_time = (tf - t0)
        print('RMSE = %.2f' % lr_rmse)
        print('Time to train = %.2f seconds' % lr_time)

        pickle.dump([lr_model, lr_rmse, lr_time], open(self.file_path, 'wb'))

    def predict_using_mlr_with_windows(self):
        if not os.path.isfile(self.file_path):
            self.learn_mlr_with_windows()
        lr_model, lr_rmse, lr_time = pickle.load(open(self.file_path, 'rb'))
        lr_y_pred = lr_model.predict(self.candles.iloc[:, :-1])

        candle_list = []

        current_symbol_fk = ExchangeInfo.objects.get(symbol=self.pair_symbol)
        for x in lr_y_pred:
            new_candle = Candle(symbol=current_symbol_fk, interval=self.interval,
                                open_time=x['open_time'],
                                open=x['open'], high=x['high'], low=x['low'], close=x['close'], volume=x['volume'],
                                close_time=x['close_time'],
                                quote_asset_volume=x['quote_asset_volume'], number_of_trades=x['number_of_trades'],
                                taker_buy_base_asset_volume=x['taker_buy_base_asset_volume'],
                                taker_buy_quote_asset_volume=x['taker_buy_quote_asset_volume'], is_real=False,
                                prediction_type=PredictionType.MLRW)
            candle_list.append(new_candle)

        print("Inserting data to database")
        Candle.objects.bulk_create(candle_list, ignore_conflicts=True, batch_size=1000)
        print("Results saved to database")


class WindowSlider(object):
    def __init__(self, window_size, response_size):
        """
            Window Slider object
            ====================
            w: window_size - number of time steps to look back
            o: offset between last reading and temperature
            r: response_size - number of time steps to predict
            l: maximum length to slide - (#observation - w)
            p: final predictors - (#predictors * w)
        """
        self.window_size = window_size
        self.offset = 0
        self.response_size = response_size
        self.max_length = 0
        self.final_predictors = 0
        self.names = []

    def re_init(self, arr):
        """
            Helper function to initializate to 0 a vector
        """
        arr = np.cumsum(arr)
        return arr - arr[0]

    def collect_windows(self, candles, offset=0, previous_y=False):
        """
            Input: X is the input matrix, each column is a variable
            Returns: diferent mappings window-output
        """
        cols = len(list(candles)) - 1
        n = len(candles)

        self.offset = offset
        # self.window_size = window_size
        self.max_length = n - (self.window_size + self.response_size) + 1
        if not previous_y:
            self.final_predictors = cols * self.window_size
        else:
            self.final_predictors = (cols + 1) * self.window_size

        # Create the names of the variables in the window
        # Check first if we need to create that for the response itself
        if previous_y:
            x = cp.deepcopy(candles)
        else:
            x = candles.drop(candles.columns[-1], axis=1)

        for j, col in enumerate(list(x)):

            for i in range(self.window_size):
                name = col + ('(%d)' % (i + 1))
                self.names.append(name)

        # Incorporate the timestamps where we want to predict
        for k in range(self.response_size):
            name = '∆t' + ('(%d)' % (self.window_size + k + 1))
            self.names.append(name)

        self.names.append('Y')

        df = pd.DataFrame(np.zeros(shape=(self.max_length, (self.final_predictors + self.response_size + 1))),
                          columns=self.names)

        # Populate by rows in the new dataframe
        for i in range(self.max_length):

            slices = np.array([])

            # Flatten the lags of predictors
            for p in range(x.shape[1]):

                line = candles.values[i:self.window_size + i, p]
                # Reinitialization at every window for ∆T
                if p == 0:
                    line = self.re_init(line)

                # Concatenate the lines in one slice
                slices = np.concatenate((slices, line))

                # Incorporate the timestamps where we want to predict
            line = np.array([self.re_init(candles.values[i:i + self.window_size + self.response_size, 0])[-1]])
            y = np.array(candles.values[self.window_size + i + self.response_size - 1, -1]).reshape(1, )
            slices = np.concatenate((slices, line, y))

            # Incorporate the slice to the cake (df)
            df.iloc[i, :] = slices

        return df

# class Predictor:
#     def __init__(self, pair_symbol, interval, window_size=60, response_size=5):
#         candles = Candle.objects.filter(symbol=pair_symbol,
#                                         is_real=True,
#                                         interval=interval).order_by('open_time')
#         self.pair_symbol = pair_symbol
#         self.interval = interval
#         self.window_size = window_size
#         self.response_size = response_size
