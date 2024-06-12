from PyBean import bean
from PyBean.ioc import Application


if __name__ == '__main__':
    ioc = Application('resource/applicationContext.xml')
    print(ioc.getBeanList())
    bookDao: bean = ioc.getBean('bookDao')
    bookImp: bean = ioc.getBean('bookImp')

    getDao: bean = ioc.matchBean('dao', bookImp)

    bookImp.instance.show()
    getDao.instance.show()
    # bookDao.instance.show()