from typing import List

from PyBean.ioc import ApplicationContext, ApplicationMode, ElementLoader

from test.imp.bookImp import *

def main():
    actx = ApplicationContext('resource/applicationContext.xml',
                              applicationMode=ApplicationMode.default)
    # actx.set__mode(ApplicationMode.development)
    print(actx.getBean("bookImp2", requiredType=BookDaoImp))
    print(type(actx.getBean("payImp85").discount))
    bookDaoImp: Bookdao = actx.getBean("bookImp")
    bookDaoImp2: Bookdao = actx.getBean("bookImp2")

    print("-" * 50)
    assert type(bookDaoImp.brotherImp) is type(bookDaoImp2)
    print(actx.getBean("bookImp").brotherImp)
    print(actx.getBean("bookImp2"))

    print("-" * 50)
    print(actx.getBeanLoaderList()[0].element.attrib)

if __name__ == '__main__':
    main()