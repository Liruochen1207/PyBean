from typing import List

from PyBean.ioc import ApplicationContext, ApplicationMode, ElementLoader
from test.imp.bookImp import *

if __name__ == '__main__':
    actx = ApplicationContext('resource/applicationContext.xml')

    print(actx.getBean("payImp85").discount)
    print(type(actx.getBean("payImp85").discount))
    bookDaoImp: Bookdao = actx.getBean("bookImp")
    bookDaoImp2: Bookdao = actx.getBean("bookImp2")

    print("-" * 50)
    assert type(bookDaoImp.brotherImp) is type(bookDaoImp2)
    print(actx.getBean("bookImp").brotherImp)
    print(actx.getBean("bookImp2"))

    print("-" * 50)
    print(actx.getBeanLoaderList()[0].element.attrib)