import logging
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from fitxf.math.dsp.Dft import Dft
# from statsmodels.tsa.seasonal import seasonal_decompose
from poc.utils import Logging


#
# https://en.wikipedia.org/wiki/Decomposition_of_time_series
#
class TsDecompose:

    def __init__(
            self,
            logger: Logging = None,
    ):
        self.logger = logger if logger is not None else logging.getLogger()
        return


class TsDecomposeUnitTest:
    def __init__(self, logger: Logging = None):
        self.logger = logger if logger is not None else logging.getLogger()
        return

    def test(self):
        # Generate random time series, with cycle of sine
        N = 100
        k = 3
        t = np.arange(N).astype(np.float32)
        # random values from 0-10, add 2 cycles of sine pertubation
        y = np.sin(t * 2 * np.pi * k / N) + np.random.rand(N)
        self.logger.info('Generated time series length ' + str(len(y)) + ': ' + str(y))
        # plt.plot(t, y, marker='o', linestyle='-', color='b', label='Line 1')
        # plt.show()

        #
        # Do some statistical study
        #
        avg, var = np.mean(y), np.var(y)
        self.logger.info('Mean & var ' + str(avg) + ', ' + str(var))

        #
        # Calculate seasonality (if any) by DFT
        #
        # df = pd.DataFrame({'t': t, 'series': y})
        # df.reset_index(inplace=True)
        # df.set_index('t', inplace=True)
        # res = seasonal_decompose(x=df['series'], model='additive')
        # res.plot()
        # plt.show()
        dft_helper = Dft(logger=self.logger)
        dft = dft_helper.DFT(x=y)
        dft_mag = np.absolute(dft)
        self.logger.info('DFT (' + str(len(dft_mag)) + '): ' + str(dft_mag))
        plt.plot(t, dft_mag, marker='o', linestyle='-', color='b', label='DFT')
        plt.title('DFT')
        plt.show()

        # moving average
        ma = y[0]
        mv_avg = []
        w_ma = 0.5
        for i in range(len(y)):
            ma = y[0] if i==0 else w_ma*ma + (1-w_ma)*y[i]
            mv_avg.append(ma)
        self.logger.info('MA ' + str(mv_avg))
        plt.plot(t, mv_avg, marker='o', linestyle='-', color='b', label='Moving Average')
        plt.title('MA')
        plt.show()

        # Modeling absolute series

        # Modeling differences
        return


if __name__ == '__main__':
    lgr = Logging.get_default_logger(log_level=logging.INFO, propagate=False)

    TsDecomposeUnitTest(logger=lgr).test()
    exit(0)
