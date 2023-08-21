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
        'boto3~=1.20.35',
        'aws-secretsmanager-caching~=1.1.1.4',
        'cachetools~=4.1.1'
    ],
    include_package_data=True
)
