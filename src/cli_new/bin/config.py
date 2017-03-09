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
This file defines the default configuration of the mesos-cli. It also takes
care of updating the default configuration from reading environment variables
or parsing a configuration file.
"""

import json
import os
import sys

from mesos.exceptions import CLIException


# There is no version module included in this package. However,
# when creating an executable using pyinstaller, a version.py
# file will be autogenerated and inserted into the PYTHONPATH.
# When this happens we import it to set the VERSION.
try:
    # pylint: disable=F0401,W0611
    from version import VERSION
except Exception:
    VERSION = "Development"


# The top-level directory of this project.
PROJECT_DIR = os.path.join(os.path.dirname(__file__), os.pardir)


# The builtin plugins.
PLUGINS = [
    os.path.join(PROJECT_DIR, "lib/mesos/plugins", "container"),
    os.path.join(PROJECT_DIR, "lib/mesos/plugins", "config"),
    os.path.join(PROJECT_DIR, "lib/mesos/plugins", "task"),
]


# Default agent parameters.
AGENT_IP = "127.0.0.1"
AGENT_PORT = "5051"


# Allow extra plugins to be pulled in from a configuration file.
if os.environ.get("MESOS_CLI_CONFIG_FILE"):
    try:
        CONFIG_FILE = open(os.environ["MESOS_CLI_CONFIG_FILE"])
    except Exception as exception:
        sys.exit("Unable to open configuration file '{config}': {error}"
                 .format(config=os.environ.get("MESOS_CLI_CONFIG_FILE"),
                         error=str(exception)))

    try:
        CONFIG_DATA = json.load(CONFIG_FILE)
    except Exception as exception:
        raise CLIException("Error loading config file as JSON: {error}"
                           .format(error=exception))

    for config_key in CONFIG_DATA.keys():
        config_key_upper = config_key.upper()

        if config_key_upper in globals():
            config_key_type = globals()[config_key_upper]

            if not isinstance(CONFIG_DATA[config_key], config_key_type):
                raise CLIException("'{key}' field must be a {type}"
                                   .format(key=config_key,
                                           type=config_key_type))
        else:
            raise CLIException("Unknown key in CONFIG_FILE '{key}':"
                               .format(key=config_key))


# Allow extra plugins to be pulled in from the environment.
# The `MESOS_CLI_PLUGINS` environment variable is a ":" separated
# list of paths to each plugin. All paths must be absolute.
if os.environ.get("MESOS_CLI_PLUGINS"):
    PLUGINS += filter(None, os.environ.get("MESOS_CLI_PLUGINS").split(":"))
