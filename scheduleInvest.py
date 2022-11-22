from db.user import User, UserModel
from db.history import HistoryModel
from bson.json_util import dumps
import pandas as pd
import numpy as np
from datetime import datetime
from helpers.binance import binance
from helpers.common import f_time
from sklearn import linear_model
import socketio
sio = socketio.Client()

SYMBOL = 'ETH/USDT'
TIME_FRAME = '1m'
N = 50
users = UserModel.find()
btc_usdt_ohlcv = binance.fetch_ohlcv(SYMBOL, TIME_FRAME, limit=N)
data = pd.DataFrame(btc_usdt_ohlcv, columns=[
                    "Date", "Open", "High", "Low", "Close", "Volume"])
data['FDate'] = [f_time(x) for x in data['Date']]
current = data.iloc[-1]
regr = linear_model.LinearRegression()
regr.fit(np.array(data['Date']).reshape(
    N, 1), np.array(data['Close']).reshape(N, 1))
pred = regr.predict(
    np.array([[int(current['Date'])+60*1000]]))
@sio.event
def connect():
    for user in users:
        if user.get('status'):
            _user = User(user)
            if int(current['Date']) < int(_user.date_of_maturity) - 10*60*1000:
                continue
            timestamp, ms = divmod(int(_user.date_of_maturity), 1000)
            d = datetime.fromtimestamp(timestamp)
            date_of_maturity = round(datetime.strptime(datetime.strftime(
                d, '%Y-%m-%d'), '%Y-%m-%d').timestamp())*1000 + 60*1000
            amount = _user.money_per_turn/current['Close']
            if int(current['Date']) + 15*60*1000 < int(_user.date_of_maturity):
                if pred[0][0] > current['Close']:
                    _user.set_date_of_maturity(date_of_maturity)
                    status = _user.create_market(
                        'buy', amount, current['Close'])
                    if not status:
                        break
                    res = HistoryModel.insert_one({"user_id": _user.id, "ETH": _user.ETH, "USDT": _user.USDT,
                                            "Total": _user.USDT + _user.ETH*current['Close'], "create_at": current['FDate']})
                    result = HistoryModel.find_one({ "_id": res.inserted_id })
                    sio.emit("update_after_market", dumps({
                      "remaining_investment_time": _user.remaining_investment_time,
                      "history": result
                    }))
                    sio.disconnect()
            else:
                _user.set_date_of_maturity(date_of_maturity)
                status = _user.create_market('buy', amount, current['Close'])
                if not status:
                    break
                res = HistoryModel.insert_one({"user_id": _user.id, "ETH": _user.ETH, "USDT": _user.USDT,
                                        "Total": _user.USDT + _user.ETH*current['Close'], "create_at": current['FDate']})
                result = HistoryModel.find_one({ "_id": res.inserted_id })
                sio.emit("update_after_market", dumps({
                  "remaining_investment_time": _user.remaining_investment_time,
                  "history": result
                }))
                sio.disconnect()

sio.connect('http://127.0.0.1:8000')
sio.wait()