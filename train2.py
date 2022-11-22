import pandas as pd
import numpy as np
import os
import math
from datetime import datetime
from db.user import UserModel, User
from db.history import HistoryModel
from helpers.binance import binance, binanceAuth
from helpers.common import f_time, truncate
from sklearn import linear_model
TYPE = '1'
TIME = '365'
SYMBOL = 'ETH/USDT'
DEV = False
N = 50
TURN = 5000000/int(TIME)
_user = UserModel.find_one({ "id": 2})
user = User(_user)
user.print_balance()

# START_DATE = '2021-11-15'
# day = '2021-11-11 00:00:00'
# start = round(datetime.strptime(str(START_DATE), '%Y-%m-%d %H:%M:%S').timestamp()*1000)
# btc_usdt_ohlcv = binance.fetch_ohlcv(SYMBOL,'15m', since, limit=1000)
data = pd.read_csv(os.path.join(os.path.abspath(os.getcwd()), 'out.csv'))
data['FDate'] = [f_time(x) for x in data['Date']]
train = data.iloc[0:N,:]
user.set_date_of_maturity(round(datetime.strptime('2021-11-12', '%Y-%m-%d').timestamp())*1000)
for i in range(N-1, data.shape[0]):
  current = data.loc[i]
  # print (current['Date'], int(user.date_of_maturity) - int(TYPE)*24*60*60*1000)
  if int(current['Date']) < int(user.date_of_maturity) - int(TYPE)*24*60*60*1000: continue
  timestamp, ms = divmod(int(user.date_of_maturity), 1000)
  d = datetime.fromtimestamp(timestamp)
  date_of_maturity = round(datetime.strptime(datetime.strftime(d, '%Y-%m-%d'), '%Y-%m-%d').timestamp())*1000 + int(TYPE)*24*60*60*1000
  amount = TURN/current['Close']
  if int(current['Date']) + 15*60*1000 < int(user.date_of_maturity):

    regr = linear_model.LinearRegression()
    regr.fit(np.array(train['Date']).reshape(N, 1), np.array(train['Close']).reshape(N, 1))
    pred = regr.predict(np.array([[int(current['Date'])+15*60*1000]]))
    if pred[0][0] > current['Close']:
      user.set_date_of_maturity(date_of_maturity)
      status = user.create_market('buy', amount, current['Close'])
      if not status: break
      HistoryModel.insert_one({ "user_id": user.id, "ETH": user.ETH, "USDT": user.USDT, "Total": user.USDT + user.ETH*current['Close'], "create_at": current['FDate'] })

  else:
    user.set_date_of_maturity(date_of_maturity)
    status = user.create_market('buy', amount, current['Close'])
    if not status: break
    HistoryModel.insert_one({ "user_id": user.id, "ETH": user.ETH, "USDT": user.USDT, "Total": user.USDT + user.ETH*current['Close'], "create_at": current['FDate'] })
  train = data.iloc[i-N+2:i+2,:]

  # neu current + 15m < date_of_maturity
  ## thi tien hanh du doan
  ### neu du doan tiep theo co xu huong tang -> mua
  # neu > date_of_maturity --> mua