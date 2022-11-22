import pandas as pd
import numpy as np
from datetime import datetime
from db.user import UserModel, User
from db.history import HistoryModel
from helpers.binance import binance, binanceAuth
from helpers.common import f_time
from sklearn import linear_model
TYPE = '1'
TIME = '365'
SYMBOL = 'ETH/USDT'
DEV = False
N = 20
TURN = 5000/int(TIME)
# _user = UserModel.find_one({ "id": 1})
# user = User(_user)
# user.print_balance()
# day = '2021-11-11 00:00:00'
# since = round(datetime.strptime(str(day), '%Y-%m-%d %H:%M:%S').timestamp()*1000)
# btc_usdt_ohlcv = binance.fetch_ohlcv(SYMBOL,'15m', since, limit=1000)
print(binance.fetch_ticker(SYMBOL)['close'])


# data = pd.DataFrame(btc_usdt_ohlcv, columns = ["Date", "Open", "High", "Low", "Close", "Volume"])
# data['FDate'] = [f_time(x) for x in data['Date']]
# train = data.iloc[0:N,:]
# user.set_date_of_maturity(data.loc[N]['Date'])
# for i in range(N-1, 1000):
#   current = data.loc[i]
#   amount = TURN/int(current['Close'])
#   if int(current['Date']) + 15*60*1000 < int(user.date_of_maturity):

#     regr = linear_model.LinearRegression()
#     regr.fit(np.array(train['Date']).reshape(N, 1), np.array(train['Close']).reshape(20, 1))
#     pred = regr.predict(np.array([[int(current['Date'])+15*60*1000]]))
#     if pred[0][0] >current['Date']:
#       user.set_date_of_maturity(int(user.date_of_maturity) + int(TYPE)*24*60*60*1000)
#       user.create_market('buy', amount, current['Close'])
#       HistoryModel.insert_one({ "ETH": user.ETH, "USDT": user.USDT, "Total": user.USDT + user.ETH*current['Close'], "create_at": current['FDate'] })

#   else:
#     user.set_date_of_maturity(int(user.date_of_maturity) + int(TYPE)*24*60*60*1000)
#     user.create_market('buy', amount, current['Close'])
#     HistoryModel.insert_one({ "ETH": user.ETH, "USDT": user.USDT, "Total": user.USDT + user.ETH*current['Close'], "create_at": current['FDate'] })
#   train = data.iloc[i-N+2:i+2,:]

#   # neu current + 15m < date_of_maturity
#   ## thi tien hanh du doan
#   ### neu du doan tiep theo co xu huong tang -> mua
#   # neu > date_of_maturity --> mua