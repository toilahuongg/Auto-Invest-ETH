from db.history import HistoryModel
from db.user import User, UserModel
HistoryModel.delete_many({})
UserModel.delete_many({})
user = User({ "_id": None, "id": 1, "fullname": "Vu Ba Huong", "ETH": 0, "USDT": 5000000, "remaining_investment_time": 1000 })
UserModel.insert_one(user._dict())
user2 = User({ "_id": None, "id": 2, "fullname": "Vu Ba Huong", "ETH": 0, "USDT": 5000000,  "remaining_investment_time": 1000 })
UserModel.insert_one(user2._dict() )