from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='secrets_manager',
    version='0.0.1',
    description='AWS Secrets Manager Python client',
    long_description=readme(),
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ],
    packages=[
        'secrets_manager'
    ],
    url='https://github.com/datawookie/secrets-manager',
    install_requires=[
        'boto3',
        'aws-secretsmanager-caching'
    ],
    include_package_data=True
)
