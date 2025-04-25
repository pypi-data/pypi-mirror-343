# AWS SSO Lite

AWS SSO Lite is a lightweight Python library that allows users to authenticate with AWS Single Sign-On (SSO) without requiring the AWS CLI. This library simplifies the process of obtaining temporary AWS credentials using SSO, making it easier to integrate SSO authentication into your Python applications.

## Features

- **SSO Authentication**: Authenticate with AWS SSO without needing the AWS CLI.
- **Temporary Credentials**: Retrieve temporary AWS credentials for use in your Python applications.
- **Simple Integration**: Easily integrate AWS SSO authentication into your Python scripts or tools.

## Installation

You can install the library from PyPI using `pip`:

```bash
pip install aws-sso-lite
```

## Usage
```python
from aws_sso_lite import get_sso_token_by_start_url, do_sso_login
import botocore

start_url = "http://some-start-url.awsapps.com/start"
sso_token = get_sso_token_by_start_url(start_url)

botocore_session = botocore.session.Session()
region = 'eu-west-1'

do_sso_login(botocore_session, region, start_url)
```