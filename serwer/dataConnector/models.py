from .submodels import Cryptocurrency
from .submodels import ExchangeInfo
from .submodels import Rate
from .submodels import Candle
from .submodels import update_coins
from .submodels import update_exchanges
from .submodels import update_rates
from .submodels import update_candles
import schedule, time

# schedule.every(5).seconds.do(update_rates)
# schedule.every(5).seconds.do(update_candles)

# schedule.every().day.at("10:00").do(update_rates)
# schedule.every().day.at("10:00").do(update_candles)

"""
while True:
    schedule.run_pending()
    time.sleep(1)
"""

# update_coins()
# update_exchanges()
# update_rates()
# update_candles()
