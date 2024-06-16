from PyBean import bean
from PyBean.ioc import ApplicationContext, ElementLoader

if __name__ == '__main__':
    actx = ApplicationContext('resource/applicationContext.xml')
    elementLoader: ElementLoader = actx.getScanDiction()[1]
    # print(elementLoader)
    print(actx.getBean("payImp").discount)
    print(actx.getBean("payImp").price)
    print(actx.getBean("bookImp"))
    print(actx.getBean("bookImp").brotherImp)
    print(actx.getBean("bookImp").bookName)
    print(actx.getBean("bookImp").brotherImp.bookName)
