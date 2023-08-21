## AWS Secrets Manager Python client

The Secrets Manager Python client enables retrieving of secrets for Python applications.

## Getting Started

### Usage

1. Set up the following environment variables:

```bash
export AWS_PROFILE=
export AWS_DEFAULT_REGION=
# The name of the secret in Secrets Manager.
export AWS_SECRET_ID=
```

2. Retrieve values for specific keys.

```python
from secrets_manager import get_secret

# Get binary secrets such as SSH keys using the AWS source
secret = get_secret(name='api', key='SSH_KEY', type='binary')

# Get secrets from AWS and fallback to environmental variables if not found
secret = get_secret(name='www', key='API_KEY').or_default(name='API_KEY', source='env')

# Get specific key from a JSON decoded secret
secret = get_secret(name='api', key='DB_PASSWORD')
