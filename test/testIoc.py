from PyBean import bean
from PyBean.by import By
from PyBean.ioc import Application


if __name__ == '__main__':
    ioc = Application('resource/applicationContext.xml')
    print(ioc.getBeanList())
    bookDao: bean = ioc.getBean(by=By.id, arg='bookDao', requiredType='dao.bookdao.Bookdao')
    bookImp: bean = ioc.getBean('bookImp', requiredType='imp.bookImp.BookDaoImp')
    # print(ioc.getBean(requiredType='imp.bookImp.BookDaoImp'))


    getDao: bean = ioc.getBean(arg=bookImp.attribute('dao'))
    print(getDao.instance == bookImp.instance)
    print(type(getDao.instance) == type(bookImp.instance))

    bookDao.instance.show()
    bookImp.instance.show()
    getDao.instance.show()

    discountBean: bean = ioc.getBean('discount')
    discount = discountBean.instance.discount()
    priceBean: bean = ioc.getBean('payImp')
    price = priceBean.instance.price
    print(price)

    print("折后价格", discount * price)