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
CLIException Class
"""


class CLIException(Exception):
    """
    Exceptions class to handle all CLI errors.
    """
    pass


class MesosException(Exception):
    """
    Exceptions class to handle all mesos errors
    """
    pass


class MesosHTTPException(MesosException):
    """ A wrapper around Response objects for HTTP error codes.

    :param response: requests Response object
    :type response: Response
    """
    def __init__(self, response):
        super(MesosHTTPException, self).__init__()
        self.response = response

    def status(self):
        """Return status code from response

        :return: status code
        :rtype: int
        """
        return self.response.status_code

    def __str__(self):
        return 'Error while fetching [{0}]: HTTP {1}: {2}'.format(
            self.response.request.url,
            self.response.status_code,
            self.response.reason)


class MesosAuthenticationException(MesosHTTPException):
    """A wrapper around Response objects for HTTP Authentication errors (401).
    """
    def __str__(self):
        return "Authentication failed."


class MesosUnprocessableException(MesosHTTPException):
    """ A wrapper around Response objects for HTTP 422
    error codes, Unprocessable JSON Entities.
    """
    def __str__(self):
        return 'Error while fetching [{0}]: HTTP {1}: {2}'.format(
            self.response.request.url,
            self.response.status_code,
            self.response.text)


class MesosAuthorizationException(MesosHTTPException):
    """A wrapper around Response objects for HTTP Authorization errors (403).
    """
    def __str__(self):
        return "You are not authorized to perform this operation"


class MesosBadRequest(MesosHTTPException):
    """A wrapper around Response objects for HTTP Bad Request (400).
    """
    def __str__(self):
        return "Bad request"
