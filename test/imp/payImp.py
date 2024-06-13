from test.dao.paydao import Paydao


class PayImp(Paydao):
    pass

class NoDiscount(Paydao):
    def discount(self):
        return 1


class Discount85(Paydao):
    def discount(self):
        return 0.85
