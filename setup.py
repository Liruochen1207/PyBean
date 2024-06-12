from setuptools import setup, find_packages

setup(
    name='PyIoc',
    version='0.0.1',
    author='Archer Lee',
    author_email='liruochen01@outlook.com',
    packages=find_packages(),
    install_requires=[  # 依赖列表
        # 'dependency1',
        # 'dependency2',
    ],
    scripts=[  # 可选，如果有命令行工具
        # 'bin/script1',
        # 'bin/script2',
    ],
    url='http://pypi.python.org/pypi/PyIoc/',
    license='LICENSE.txt',
    description='An example Python IOC looks like Spring',
    long_description=open('README.txt').read(),
    long_description_content_type='text/x-textile',
)
