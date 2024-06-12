from test.dao.bookdao import Bookdao


class BookDaoImp(Bookdao):
    def show(self):
        print("im Bookdao's Imp")

class BookDaoImp2(Bookdao):
    def show(self):
        print("im Bookdao's another Imp")