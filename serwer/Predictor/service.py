import copy as cp
import os
import pickle

import numpy as np
import pandas as pd
import time

from Predictor.models import PredictionType, prediction_models_directory
from dataConnector.models import Candle


class Learning:

    def __init__(self, pair_symbol, interval, window_size=60, response_size=5):
        candles_queryset = Candle.objects.filter(symbol=pair_symbol,
                                                 is_real=True,
                                                 interval=interval).order_by('open_time').defer('id', 'symbol',
                                                                                                'interval',
                                                                                                'is_real',
                                                                                                'prediction_type')
        self.pair_symbol = pair_symbol
        self.interval = interval
        self.window_size = window_size
        self.response_size = response_size

        candles = np.array(
            list(candles_queryset.values_list('open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time',
                                              'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume',
                                              'taker_buy_quote_asset_volume')))
        self.dataset = pd.DataFrame(candles,
                                    columns=['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time',
                                             'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume',
                                             'taker_buy_quote_asset_volume'])

        delta_t = np.array(
            [(self.dataset.close_time[i] + 1 - self.dataset.open_time[i]) for i in range(len(self.dataset))])
        # delta_t = np.concatenate((np.array([0]), delta_t))
        y = np.array([(self.dataset.close[i] - self.dataset.open[i]) for i in range(len(self.dataset))])

        self.dataset.insert(1, '∆t', delta_t)
        self.dataset.drop(columns=['close_time'], inplace=True)
        self.dataset.insert(len(list(self.dataset)), 'y', y)

        candles_count = self.dataset.__len__()
        trainset = self.dataset.iloc[:round(candles_count * 0.75)]
        testset = self.dataset.iloc[round(candles_count * 0.75):]

        # Create Windows
        train_constructor = WindowSlider(self.window_size, self.response_size)
        self.train_windows = train_constructor.collect_windows(trainset.iloc[:, 1:], previous_y=False)

        test_constructor = WindowSlider(self.window_size, self.response_size)
        self.test_windows = test_constructor.collect_windows(testset.iloc[:, 1:], previous_y=False)

        train_constructor_y_inc = WindowSlider(self.window_size, self.response_size)
        self.train_windows_y_inc = train_constructor_y_inc.collect_windows(trainset.iloc[:, 1:], previous_y=True)

        test_constructor_y_inc = WindowSlider(self.window_size, self.response_size)
        self.test_windows_y_inc = test_constructor_y_inc.collect_windows(testset.iloc[:, 1:], previous_y=True)

    def learn(self, method=PredictionType.MLRW):
        return {
            PredictionType.MLRW: self.learn_mlr_with_windows(),
        }[method]

    def learn_mlr_with_windows(self):
        from sklearn.linear_model import LinearRegression
        lr_model = LinearRegression()
        lr_model.fit(self.train_windows.iloc[:, :-1], self.train_windows.iloc[:, -1])

        t0 = time.time()
        lr_y = self.test_windows['Y'].values
        # lr_y_fit = lr_model.predict(self.train_windows.iloc[:, :-1])
        lr_y_pred = lr_model.predict(self.test_windows.iloc[:, :-1])
        tf = time.time()

        lr_residuals = lr_y_pred - lr_y.astype('float64')
        lr_rmse = np.sqrt(np.sum(np.power(lr_residuals, 2)) / len(lr_residuals))
        lr_time = (tf - t0)
        print('RMSE = %.2f' % lr_rmse)
        print('Time to train = %.2f seconds' % lr_time)

        file_path = prediction_models_directory + self.pair_symbol + '_' + self.interval + '_mlr_with_windows_' + self.window_size.__str__() \
                    + '-' + self.response_size.__str__() + '.pkl'
        file = open(file_path, 'wb')
        pickle.dump([lr_model, lr_rmse, lr_time], file)
        file.close()


def predict_using_mlr_with_windows(symbol, interval, prediction_model):
    file_path = prediction_models_directory + prediction_model + '.pkl'
    if not os.path.isfile(file_path):
        return None
    lr_model, lr_rmse, lr_time = pickle.load(open(file_path, 'rb'))

    # lr_y_pred = lr_model.predict(self.dataset.iloc[:, :-1])
    #
    # candle_list = []
    #
    # current_symbol_fk = ExchangeInfo.objects.get(symbol=symbol)
    # for x in lr_y_pred:
    #     new_candle = Candle(symbol=current_symbol_fk, interval=interval,
    #                         open_time=x['open_time'],
    #                         open=x['open'], high=x['high'], low=x['low'], close=x['close'], volume=x['volume'],
    #                         close_time=x['close_time'],
    #                         quote_asset_volume=x['quote_asset_volume'], number_of_trades=x['number_of_trades'],
    #                         taker_buy_base_asset_volume=x['taker_buy_base_asset_volume'],
    #                         taker_buy_quote_asset_volume=x['taker_buy_quote_asset_volume'], is_real=False,
    #                         prediction_type=PredictionType.MLRW)
    #     candle_list.append(new_candle)
    #
    # print("Inserting data to database")
    # Candle.objects.bulk_create(candle_list, ignore_conflicts=True, batch_size=1000)
    # print("Results saved to database")


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

    def collect_windows(self, dataset, offset=0, previous_y=False):

        cols = len(list(dataset)) - 1
        n = len(dataset)

        self.offset = offset
        self.max_length = n - (self.window_size + self.response_size) + 1

        # Create the names of the variables in the window
        # Check first if we need to create that for the response itself
        if previous_y:
            self.final_predictors = (cols + 1) * self.window_size
            x = cp.deepcopy(dataset)
        else:
            self.final_predictors = cols * self.window_size
            x = dataset.drop(dataset.columns[-1], axis=1)

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

        for i in range(self.max_length):
            slices = np.array([])

            # Flatten the lags of predictors
            for p in range(x.shape[1]):
                line = dataset.values[i:self.window_size + i, p]
                if p == 0:
                    line = self.re_init(line)
                slices = np.concatenate((slices, line))

            # Incorporate the timestamps where we want to predict
            line = self.re_init(dataset.values[i:i + self.window_size + self.response_size, 0])[-self.response_size:]
            y = np.array(dataset.values[self.window_size + i + self.response_size - 1, -1]).reshape(1, )
            slices = np.concatenate((slices, line, y))

            df.iloc[i, :] = slices

        return df
