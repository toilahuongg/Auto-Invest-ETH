from flask import Flask, request
from bson.json_util import dumps
import datetime
from db.history import HistoryModel
from db.user import User, UserModel
from helpers.binance import binance
from flask_cors import CORS
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SYMBOL'] = 'ETH/USDT'
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)


@socketio.on('message')
def handle_message(data):
    print('received message: ' + data)

@socketio.on('update_remaining')
def update_remaining(data):
    socketio.emit('update_remaining', data)

@socketio.on('update_after_market')
def update_after_market(data):
    print(data)
    socketio.emit('update_after_market', data)

@socketio.on('priceETH')
def price_ETH(data):
    socketio.emit('priceETH', data)

@app.get("/user/<int:user_id>")
def user(user_id):
    user = UserModel.find_one({"id": user_id})
    price = binance.fetch_ticker(app.config['SYMBOL'])['close']
    result = dict(user)
    result['priceETH'] = price
    return dumps(result)

@app.post("/user/<int:user_id>/invest")
def invest(user_id):
    body = request.json
    user = UserModel.find_one({"id": user_id})
    _user = User(user)
    _user.invest({ "money_per_turn": body["money"], "day_per_turn": 1, "investment_time": body["time"]})
    _user.set_date_of_maturity(round(datetime.datetime.now().timestamp()+5*60)*1000)
    UserModel.update_one({"id": user_id}, { "$set": _user.__dict__ })
    return dumps({"oke": 1})

@app.post("/user/<int:user_id>/stop-investing")
def stop_investing(user_id):
    user = UserModel.find_one({"id": user_id})
    _user = User(user)
    _user.stop_investing()
    UserModel.update_one({"id": user_id}, { "$set": _user.__dict__ })
    return dumps({"oke": 1})

@app.get("/histories/<int:user_id>")
def histories(user_id):
    histories = HistoryModel.f`ind({"user_id": user_id})
    return dumps(list(histories))

if __name__ == '__main__':
    app.run()
