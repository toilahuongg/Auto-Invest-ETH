
import os
import ccxt
from dotenv import load_dotenv
load_dotenv()
binance = ccxt.binance()
binanceAuth = ccxt.binance({
  'apiKey': os.getenv('API_KEY'),
  'secret': os.getenv('SECRET_KEY')
})
binanceAuth.set_sandbox_mode(True)