from helpers.binance import binance
import socketio
sio = socketio.Client()
SYMBOL = 'ETH/USDT'

@sio.event
def connect():
    print('connected to server')
    price = binance.fetch_ticker(SYMBOL)['close']
    sio.emit('priceETH', str(price))
    sio.disconnect()
sio.connect('http://127.0.0.1:8000')
sio.wait()