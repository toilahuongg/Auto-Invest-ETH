from db.database import db

UserModel = db['users']

class User:
  def __init__(self, user):
    self._id = user['_id']
    self.id = user['id']
    self.fullname = user['fullname'] 
    self.ETH = user['ETH'] 
    self.USDT = user['USDT'] 
    self.date_of_maturity = user.get('date_of_maturity')
    self.money_per_turn = user.get('money_per_turn')
    self.investment_time = user.get('investment_time')
    self.day_per_turn = user.get('day_per_turn')
    self.remaining_investment_time = user.get('remaining_investment_time')
    self.status = user.get('status')
  def _dict(self):
    d = self.__dict__.copy()
    d.pop("_id")
    return d
  def print_balance(self):
    print('Fullname: ', self.fullname)
    print('ETH: ', self.ETH)
    print('USDT: ', self.USDT)
  def total_usdt(self, ethPrice: float):
    print('Total USDT', self.ETH*ethPrice+self.USDT)
  def set_date_of_maturity(self, value):
    self.date_of_maturity = str(value)
  def invest(self, _invest):
    self.money_per_turn = _invest['money_per_turn']
    self.investment_time = _invest['investment_time']
    self.remaining_investment_time = _invest['investment_time']
    self.day_per_turn = _invest['day_per_turn']
    self.status = True
  def stop_investing(self):
    self.status = False
  def create_market(self, side, amount, price): 
    if side == 'buy' and self.USDT >= amount*price and self.remaining_investment_time > 0:
      self.ETH += amount
      self.USDT -= amount*price
      self.remaining_investment_time -= 1
      UserModel.update_one({ "id": self.id }, { "$set": self.__dict__ })
      return True
    return False
    # elif self.ETH >= amount:
    #   self.ETH -= amount
    #   self.USDT += amount*price
    # else:
    #   self.ETH = 0
    #   self.USDT += self.ETH*price

    