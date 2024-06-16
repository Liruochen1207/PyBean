from typing import List

from PyBean import bean
from PyBean.ioc import ApplicationContext, ElementLoader

if __name__ == '__main__':
    actx = ApplicationContext('resource/applicationContext.xml')
    elementLoaderList: List[ElementLoader] = actx.getScanDiction()[0]
    for elementLoader in elementLoaderList:
        bean = actx.buildBean(elementLoader)
        for prop in bean.get_properties():
            print(prop.name, prop.value)
    print(actx.getBean("payImp").discount)
    print(actx.getBean("payImp").price)
    print(actx.getBean("bookImp"))
    print(actx.getBean("bookImp").brotherImp)
    print(actx.getBean("bookImp").bookName)
    print(actx.getBean("bookImp").brotherImp.bookName)
