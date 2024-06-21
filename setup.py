from setuptools import setup, find_packages

with open("README.md", "r", encoding="UTF-8") as fh:
    long_description = fh.read()

setup(
    name='pyBean',
    version='0.0.23',
    author='Archer_Lee.chen',
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
    url='https://pypi.org/project/pyBean/',
    license='LICENSE.txt',
    description='An example Python IOC looks like Spring',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
