from test.dao.paydao import Paydao


class PayImp(Paydao):
    def __init__(self, discount):
        self.discount = discount
