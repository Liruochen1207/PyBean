from PyBean import bean
from PyBean.ioc import Application, ElementLoader

if __name__ == '__main__':
    ioc = Application('resource/applicationContext.xml')
    elementLoader: ElementLoader = ioc.getScanDiction()[1]
    print(elementLoader)
    print(ioc.getBean())
