from typing import List

from PyBean import bean
from PyBean.ioc import ApplicationContext, ElementLoader
from test.imp.bookImp import *

if __name__ == '__main__':
    actx = ApplicationContext('resource/applicationContext.xml')
    elementLoaderList: List[ElementLoader] = actx.getScanDiction()[0]
    for elementLoader in elementLoaderList:
        bean = actx.buildBean(elementLoader)
        for prop in bean.get_properties():
            print(prop.name, prop.value)
    print(actx.getBean("payImp").discount)
    print(actx.getBean("payImp").price)
    bookDaoImp: Bookdao = actx.getBean("bookImp")
    bookDaoImp2: Bookdao = actx.getBean("bookImp2")

    print("-" * 50)
    assert type(bookDaoImp.brotherImp) is type(bookDaoImp2)
    print(actx.getBean("bookImp").brotherImp)
    print(actx.getBean("bookImp2"))

