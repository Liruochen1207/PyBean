from test.dao.paydao import Paydao


class PayImp(Paydao):
    def __init__(self, discount, price):
        self.discount = discount
        self.price = price
