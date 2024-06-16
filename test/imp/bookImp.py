from test.dao.bookdao import Bookdao


class BookDaoImp(Bookdao):

    def show(self):
        super(BookDaoImp, self).show()
        print("im Bookdao's Imp")


class BookDaoImp2(Bookdao):
    def __init__(self, bookName):
        super(BookDaoImp2, self).__init__(bookName)
    def show(self):
        super(BookDaoImp2, self).show()
        print("im Bookdao's another Imp")