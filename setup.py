import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "cloud_storage_client",
    version = "0.0.11",
    author = "Pablo Aguirre",
    author_email = "paguirrerubio@gmail.com",
    license = "MIT",
    url = "http://packages.python.org/cloud_storage_client",
    packages=['cloud_storage_client'],
    long_description=read('README.md'),
    install_requires=[
        'boto3==1.4.1',
        'google.cloud==0.32.0',
        'azure==3.0.0',
        'pysftp==0.2.9'
    ],
)