

# PyBean



## 1. What is this?
This is a Python module implementation of IOC container management.

You can read your XML files and dynamically manage your Python classes through the "Application Context" class. In order to help those familiar with Java Spring understand quickly, I plan to try to adapt to the rules in Spring as much as possible in the future.


## 2.How to use?
For Developers, ensure that Python is installed on your device and that the environment is ready.

Download in shell by pip:
```shell
pip install pyBean
```
or
```shell
pip3 install pyBean
```


File structure
```
project
  +-- dao
  |    +-- __init__.py
  |    +-- person.py
  |  
  +-- resource
  |     +-- applicationContext.xml
  +-- main.py
```

Prepare the classes you want to inject


```
# person.py
class PersonDao:
    def __init__(self, name):
        self.name = name
        self.home = ""

    def greet(self):
        sentence = f"Hey {self.name}!"
        if self.home:
            sentence += f" {self.home} is a good place!"
        print(sentence)
```
Prepare the XML file, named applicationContext.xml
```
<?xml version="1.0" encoding="UTF-8"?>

<beans resource="https://pypi.org/project/pyBean/">
    <bean id="me" class="dao.person.PersonDao">
        <!--person name-->
        <constructor-arg value="Lee"/>
        
        <!--you can change it to your region here.-->
        <property name="home" value="China"/>
        
    </bean>
    
</beans>
```


In your python file:
```
# main.py

from PyBean.ioc import ApplicationContext


if __name__ == '__main__':
    actx = ApplicationContext('resource/applicationContext.xml')
    personGet = actx.getBean("me")
    personGet.greet()
    
```

Run it.
```shell
python main.py
```
or
```shell
python3 main.py
```

> Hey Lee! China is a good place!




#### website: https://space.bilibili.com/178065252
#### pypi: https://pypi.org/project/pyBean/
#### repository: https://github.com/Liruochen1207/PyBean