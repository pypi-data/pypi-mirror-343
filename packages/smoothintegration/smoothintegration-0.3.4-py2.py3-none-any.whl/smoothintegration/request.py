import uuid
from typing import Literal, TypedDict, cast, Optional

import requests

from smoothintegration import _http


def make_request(
    connection_id: uuid.UUID,
    **kwargs,
) -> requests.Response:
    """
    Make a HTTP request directly to the third party API. This is used as you would the Python requests library.
    All Authorization is handled by SmoothIntegration, so do not pass any Authorization headers like "Authorization" or "Xero-Tenant-Id".

    Example:

    >>> smoothintegration.request.make_request(
    >>>     uuid.UUID("3a739c6e-d4bc-4b40-ae52-bc8b01bb9973"),
    >>>     method="POST",
    >>>     json={'foo': 'bar'},
    >>>     # any other kwargs are passed to the requests library like "headers" or "params"
    >>> )

    :returns: The Response from the third party API as is.
    :raises SIError: if there was an issue preparing the authorization.
    """
    return _http._raw_request("/v1/request/" + str(connection_id), **kwargs)
