# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
A collection of http related functions used by the CLI and its Plugins.
"""

import json
import time
import urllib2

# requests must be imported last
import requests

from mesos import util
from mesos.exceptions import (CLIException, MesosException)


DEFAULT_TIMEOUT = 5
LOGGER = util.get_logger(__name__)


def _default_is_success(status_code):
    """Returns true if the success status is between [200, 300).

    :param response_status: the http response status
    :type response_status: int
    :returns: True for success status; False otherwise
    :rtype: bool
    """

    return 200 <= status_code < 300


def _verify_ssl(verify=None):
    """Returns whether to verify ssl

    :param verify: whether to verify SSL certs or path to cert(s)
    :type verify: bool | str
    :return: whether to verify SSL certs or path to cert(s)
    :rtype: bool | str
    """

    if verify is None:
        verify = False

    return verify


def read_endpoint(addr, endpoint):
    """
    Read the specified endpoint and return the results.
    """
    try:
        url = "http://{addr}/{endpoint}".format(addr=addr, endpoint=endpoint)

        http_response = urllib2.urlopen(url).read().decode("utf-8")
    except Exception as exception:
        raise CLIException("{error}".format(error=str(exception)))

    return http_response


def get_json(addr, endpoint, condition=None, timeout=5):
    """
    Return the contents of the 'endpoint' at 'addr' as JSON data
    subject to the condition specified in 'condition'. If we are
    unable to read the data or unable to meet the condition within
    'timeout' seconds we throw an error.
    """
    start_time = time.time()

    while True:
        data = None

        try:
            data = read_endpoint(addr, endpoint)
        except Exception as exception:
            pass

        if data:
            try:
                data = json.loads(data)
            except Exception as exception:
                raise CLIException("Could not load JSON"
                                   " from '{data}': {error}"
                                   .format(data=data,
                                           error=str(exception)))

            if not condition:
                return data

            if condition(data):
                return data

        if time.time() - start_time > timeout:
            raise CLIException("Failed to get data within {seconds} seconds"
                               .format(seconds=str(timeout)))

        time.sleep(0.1)


@util.duration
def _request(method,
             url,
             timeout=DEFAULT_TIMEOUT,
             auth=None,
             verify=None,
             **kwargs):
    """Sends an HTTP request.

    :param method: method for the new Request object
    :type method: str
    :param url: URL for the new Request object
    :type url: str
    :param is_success: Defines successful status codes for the request
    :type is_success: Function from int to bool
    :param timeout: request timeout
    :type timeout: int
    :param auth: authentication
    :type auth: AuthBase
    :param verify: whether to verify SSL certs or path to cert(s)
    :type verify: bool | str
    :param kwargs: Additional arguments to requests.request
        (see http://docs.python-requests.org/en/latest/api/#requests.request)
    :type kwargs: dict
    :rtype: Response
    """

    if 'headers' not in kwargs:
        kwargs['headers'] = {'Accept': 'application/json'}

    verify = _verify_ssl(verify)

    # Silence 'Unverified HTTPS request' and 'SecurityWarning' for bad certs
    if verify is not None:
        silence_requests_warnings()

    LOGGER.info(
        'Sending HTTP [%r] to [%r]: %r',
        method,
        url,
        kwargs.get('headers'))

    try:
        response = requests.request(
            method=method,
            url=url,
            timeout=timeout,
            auth=auth,
            verify=verify,
            **kwargs)
    except requests.exceptions.SSLError as err:
        LOGGER.exception("HTTP SSL Error")
        msg = "An SSL error occurred: {0}".format(err)
        raise MesosException(msg)
    except requests.exceptions.ConnectionError as err:
        LOGGER.exception("HTTP Connection Error")
        raise MesosException('URL [{0}] is unreachable: {1}'.format(url, err))
    except requests.exceptions.Timeout:
        LOGGER.exception("HTTP Timeout")
        raise MesosException('Request to URL [{0}] timed out.'.format(url))
    except requests.exceptions.RequestException as err:
        LOGGER.exception("HTTP Exception")
        raise MesosException('HTTP Exception: {}'.format(err))

    LOGGER.info('Received HTTP response [%r]: %r',
                response.status_code,
                response.headers)

    return response


def silence_requests_warnings():
    """Silence warnings from requests.packages.urllib3.  See DCOS-1007."""
    requests.packages.urllib3.disable_warnings()
