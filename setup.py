import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "cloud_storage_client",
    version = "0.0.22",
    author = "Pablo Aguirre",
    author_email = "paguirrerubio@gmail.com",
    license = "MIT",
    url = "http://packages.python.org/cloud_storage_client",
    packages=['cloud_storage_client'],
    long_description=read('README.md'),
    install_requires=[
        'botocore==1.11.4',
        'boto3==1.8.4',
        'google.cloud==0.32.0',
        'azure==3.0.0',
        'pysftp==0.2.9'
    ],
)