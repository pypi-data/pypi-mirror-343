import logging
from botocore.exceptions import SSOTokenLoadError
from botocore.credentials import JSONFileCache
from botocore.utils import SSOTokenLoader
from botocore.credentials import JSONFileCache
import botocore.session
from .vendored.botocore.utils import SSOTokenFetcher
from .vendored.awscli.sso.utils import SSO_TOKEN_DIR, _sso_json_dumps

logger = logging.getLogger()

class AWSSSO:
    def __init__(self, sso_region, session=botocore.session.Session()):
        self._token_fetcher = SSOTokenFetcher(
            sso_region=sso_region,
            client_creator=session.create_client,
            cache=JSONFileCache(SSO_TOKEN_DIR, dumps_func=_sso_json_dumps)
        )
    
    def get_sso_oidc_client_registration(self):
        return self._token_fetcher._registration()
    
    def store_sso_token(self, start_url, create_token_response):
        self._token_fetcher.store_token(start_url, create_token_response)

    def is_sso_token_valid(self, start_url):
        return self._token_fetcher.is_sso_token_valid(start_url)
    
def get_sso_token_by_start_url(start_url):
    token = None
    token_loader = SSOTokenLoader(JSONFileCache(SSO_TOKEN_DIR, dumps_func=_sso_json_dumps))

    try:
        token = token_loader(start_url)
    except SSOTokenLoadError:
        logger.debug("Token not found")
    except Exception as e:
        logger.debug(e)

    return token