import logging
import base64
import boto3
import json
import os

from aws_secretsmanager_caching import SecretCache, SecretCacheConfig
from cachetools import func


logger = logging.getLogger(__name__)


class Secret:

    def __init__(
            self,
            name: str,
            source: str = 'aws',
            key: str = None,
            type: str = 'string',
            default: object = None,
            raises: bool = False):
        self._name = name
        self._source = source
        self._key = key
        self._type = type
        self._default = default
        self._raises = raises

    def get(self):
        func = secrets_manager_factory(self._source)
        try:
            secret = func(self._name, self._key, self._type)
        except Exception as e:
            if self._raises is True:
                raise e
            return self._default
        else:
            return secret

    def or_else(
            self,
            name: str,
            source: str = 'aws',
            key: str = None,
            type: str = 'string',
            default: object = None,
            raises: bool = False):
        return self if self.get() else Secret(
            name, source, key, type, default, raises)


def get_secret(
        name: str, source: str = 'aws', key: str = None,
        type: str = 'string', default: object = None,
        raises: bool = False):
    return Secret(name, source, key, type, default, raises)


def secrets_manager_factory(source: str):
    if source == 'aws':
        return get_aws_secret
    return get_env_secret


def get_aws_secret(
        name: str, key: str = None, type: str = 'string'):
    client = _get_secrets_manager_client()

    if type == 'binary':
        assert key is None, 'key argument not supported'
        secret = client.get_secret_binary(name)
        return base64.b64decode(secret)

    secret = client.get_secret_string(name)
    if not key:
        return secret

    decoded = json.loads(secret)
    return decoded[key]


def get_env_secret(
        name: str, key: str = None, type: str = 'string'):
    secret = os.environ[name]
    if type == 'binary':
        assert key is None, 'key argument not supported'
        return base64.b64decode(secret)

    if not key:
        return secret

    decoded = json.loads(secret)
    return decoded


@func.ttl_cache(ttl=60*60)
def _get_secrets_manager_client():
    client = boto3.client('secretsmanager')
    cache_config = SecretCacheConfig(secret_refresh_interval=60*60)
    return SecretCache(config=cache_config, client=client)
