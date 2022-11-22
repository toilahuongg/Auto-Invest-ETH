from datetime import datetime
from helpers.binance import binance
import pandas as pd
day = '2019-11-11 00:00:00'
SYMBOL = 'ETH/USDT'
since = round(datetime.strptime(str(day), '%Y-%m-%d %H:%M:%S').timestamp()*1000)
result = []

data = pd.DataFrame(columns = ["Date", "Open", "High", "Low", "Close", "Volume"])
while True:
  if since > datetime.now().timestamp()*1000: break
  btc_usdt_ohlcv = binance.fetch_ohlcv(SYMBOL,'15m', since, limit=1000)
  data = pd.concat([data, pd.DataFrame(btc_usdt_ohlcv, columns = ["Date", "Open", "High", "Low", "Close", "Volume"])],ignore_index=True)
  last = data['Date'].iloc[-1]
  since = last + 15*60*1000

data.to_csv('out.csv')