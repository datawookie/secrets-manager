import logging
import boto3
import json
import os

from aws_secretsmanager_caching import SecretCache, SecretCacheConfig


logger = logging.getLogger(__name__)

# CLIENT ------------------------------------------------------------------------------------------

CACHE_CONFIG = SecretCacheConfig(secret_refresh_interval=60 * 60)


def _get_secrets_manager_client():
    client = boto3.client('secretsmanager')
    return SecretCache(config=CACHE_CONFIG, client=client)

# FUNCTIONS ---------------------------------------------------------------------------------------


def get_secret(name: str, key: str = None):
    client = _get_secrets_manager_client()

    secret = client.get_secret_string(name)
    secret = json.loads(secret)

    if key:
        return secret[key]
    else:
        return secret


# -------------------------------------------------------------------------------------------------


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


def secrets_manager_factory(source: str):
    if source == 'aws':
        return get_aws_secret
    return get_env_secret
