"""
Stack-In-A-Box: Python httpx/respx Support 
"""
from __future__ import absolute_import

import logging
import re

import httpx
import respx 

from stackinabox.stack import StackInABox
from stackinabox.util import deprecator
from stackinabox.util.tools import CaseInsensitiveDict


logger = logging.getLogger(__name__)

def respx_callback(request):
    """Respx Request Handler

    Converts a call intercepted by respx to
    the Stack-In-A-Box infrastructure

    :param request: httpx request object

    :returns: httpx response object for handled requests, otherwise None
    """
    method = request.method
    headers = CaseInsensitiveDict()
    request_headers = CaseInsensitiveDict()
    request_headers.update(request.headers)
    request.headers = request_headers
    uri = request.url
    
    response_status, response_headers, response_data = StackInABox.call_into(
        method,
        request,
        uri,
        headers,
    )
    return httpx.Response(
        response_status,
        headers=response_headers,
        content=response_data,
    )

def registration(uri):
    """Respx handler registration.

    Registers a handler for a given URI with Respx 
    so that it can be intercepted and handed to
    Stack-In-A-Box.

    :param uri: URI used for the base of the HTTP requests

    :returns: n/a
    """

    # log the URI that is used to access the Stack-In-A-Box services
    logger.debug('Registering Stack-In-A-Box at {0} under Python Responses'
                 .format(uri))
    # tell Stack-In-A-Box what URI to match with
    StackInABox.update_uri(uri)

    # Build the regex for the URI and register all HTTP verbs
    # with Responses
    regex = re.compile(r'(http)?s?(://)?{0}:?(\d+)?/'.format(uri),
                       re.I)
    route = respx.route(url__regex=regex)
    route.side_effect = respx_callback
    return route
