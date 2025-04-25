import datetime
import json
import logging
import os
import sys
import webbrowser
from botocore.credentials import JSONFileCache

from ....vendored.botocore.utils import SSOTokenFetcher


LOG = logging.getLogger(__name__)

SSO_TOKEN_DIR = os.path.expanduser(
    os.path.join('~', '.aws', 'sso', 'cache')
)

def _serialize_utc_timestamp(obj):
    if isinstance(obj, datetime.datetime):
        return obj.strftime('%Y-%m-%dT%H:%M:%SZ')
    return obj


def _sso_json_dumps(obj):
    return json.dumps(obj, default=_serialize_utc_timestamp)

def do_sso_login(session, sso_region, sso_start_url):
    token_fetcher = SSOTokenFetcher(
        sso_region=sso_region,
        client_creator=session.create_client,
        cache=JSONFileCache(SSO_TOKEN_DIR, dumps_func=_sso_json_dumps),
        on_pending_authorization=OpenBrowserHandler()
    )

    token_fetcher.fetch_token(
        start_url=sso_start_url,
        force_refresh=True
    )

    success_msg = 'Successfully logged into Start URL: %s\n'
    sys.stdout.write(success_msg % sso_start_url)

class OpenBrowserHandler:
    def __init__(self, outfile=None, open_browser=None):
        self._outfile = outfile
        if open_browser is None:
            open_browser = webbrowser.open_new_tab
        self._open_browser = open_browser

    def __call__(
        self, userCode, verificationUri, verificationUriComplete, **kwargs
    ):
        opening_msg = (
            f'Attempting to automatically open the SSO authorization page in '
            f'your default browser.\nIf the browser does not open or you wish '
            f'to use a different device to authorize this request, open the '
            f'following URL:\n'
            f'\n{verificationUri}\n'
            f'\nThen enter the code:\n'
            f'\n{userCode}\n'
        )
        sys.stdout.write(opening_msg)
        if self._open_browser:
            try:
                return self._open_browser(verificationUriComplete)
            except Exception:
                LOG.debug('Failed to open browser:', exc_info=True)