class Bookdao:
    def __init__(self, bookName):
        self.bookName = bookName
    def show(self):
        print("im Bookdao Named" + self.bookName)