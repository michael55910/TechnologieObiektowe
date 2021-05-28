import numpy as np
import copy as cp
import pandas as pd

from dataConnector.models import Candle


class Prediction:
    # candles: list[Candle]

    def __init__(self, pair_symbol, interval):
        self.candles = Candle.objects.filter(symbol=pair_symbol,
                                             is_real=True,
                                             interval=interval).only('open', 'high',
                                                                     'low', 'close',
                                                                     'volume',
                                                                     'quote_asset_volume',
                                                                     'number_of_trades',
                                                                     'taker_buy_base_asset_volume',
                                                                     'taker_buy_quote_asset_volume')

    # def get_prediction(self, window_size):


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

    def collect_windows(self, candles, window_size, offset=0, previous_y=False):
        """
            Input: X is the input matrix, each column is a variable
            Returns: diferent mappings window-output
        """
        cols = len(list(candles)) - 1
        n = len(candles)

        self.offset = offset
        self.window_size = window_size
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
