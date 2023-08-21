## AWS Secrets Manager Python client

The Secrets Manager Python client enables retrieving of secrets for Python applications.

## Getting Started

### Usage

Using the client consists of the following steps:

1. Instantiating the required client properties, `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` environment variable or `AWS_PROFILE`.

```python
from secrets_manager import get_secret

# Get binary secrets such as SSH keys using the AWS source
secret = get_secret(name='api', key='SSH_KEY', type='binary')

# Get secrets from AWS and fallback to environmental variables if not found
secret = get_secret(name='www', key='API_KEY').or_default(name='API_KEY', source='env')

# Get specific key from a JSON decoded secret
secret = get_secret(name='api', key='DB_PASSWORD')
