from distutils.core import setup

requirements = [
    'boto3==1.4.1',
    'google.cloud== 0.32.0'
]

setup(
    install_requires=requirements,
    extras_require={
        'dev': [
            'flake8',
            'flake8-quotes',
            'autopep8'
        ]
    }
)
