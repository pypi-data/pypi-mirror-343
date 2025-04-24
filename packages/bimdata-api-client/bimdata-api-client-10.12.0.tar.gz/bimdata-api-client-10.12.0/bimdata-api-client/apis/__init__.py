
# flake8: noqa

# Import all APIs into this package.
# If you have many APIs here with many many models used in each API this may
# raise a `RecursionError`.
# In order to avoid this, import only the API that you directly need like:
#
#   from .api.bcf_api import BcfApi
#
# or import this package, but before doing it, use:
#
#   import sys
#   sys.setrecursionlimit(n)

# Import APIs into API package:
from bimdata-api-client.api.bcf_api import BcfApi
from bimdata-api-client.api.collaboration_api import CollaborationApi
from bimdata-api-client.api.model_api import ModelApi
from bimdata-api-client.api.sso_api import SsoApi
from bimdata-api-client.api.webhook_api import WebhookApi
