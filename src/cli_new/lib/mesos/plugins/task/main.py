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
The task plugin.
"""

from mesos.plugins import PluginBase
from mesos.client import MesosClient, Master

PLUGIN_CLASS = "Task"
PLUGIN_NAME = "task"

VERSION = "Mesos CLI Task Plugin 0.1"

SHORT_HELP = "Task specific commands for the Mesos CLI"


class Task(PluginBase):
    """
    The task plugin.
    """

    COMMANDS = {
        "list" : {
            "arguments" : [],
            "flags" : {
                "--master=<addr>" : "IP and port of master " + \
                                    "[default: {master_ip}:{master_port}]"
            },
            "short_help" : "List all running tasks on an master",
            "long_help"  : """\
                Lists all running tasks on an master.
                """
        },
        "exec" : {
            "alias": "execute",
            "arguments" : ["<task-id>", "<command>..."],
            "flags" : {
                "--master=<addr>" : "IP and port of master " + \
                                   "[default: {master_ip}:{master_port}]"
            },
            "short_help" : "Execute a command within the specified task",
            "long_help"  : """\
                Runs the provided command within the task specified
                by <task-id>. Only supports the Mesos Taskizer.
                """
        },
    }

    def list(self, argv):
        """
        Lists all tasks on a master.
        """
        cli = MesosClient(argv["--master"], 120)
        tasks = Master(cli.get_master_state()).tasks()
        for tsk in tasks:
            print tsk.dict()

    def execute(self, argv, redirect_io=False):
        """
        Executes a command within a task.
        Works only for the mesos taskizer.
        """
        print "execute: argv=%s, redirect_io=%s" % (argv, redirect_io)
