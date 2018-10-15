# Copyright 2018 ZTE Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
from lcm.workflows.graphflow.task.sync_task import SyncTask

logger = logging.getLogger(__name__)


class SyncRestTask(SyncTask):

    STATUS_OK = (HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_202_ACCEPTED) = ('200', '201', '204', '202')
    HTTP_METHOD = (POST, GET, PUT, DELETE) = ("POST", "GET", "PUT", "DELETE")

    def __init__(self, *args):
        super(SyncRestTask, self).__init__(*args)
        self.url = self.input.get(self.URL, "")
        self.method = self.input.get(self.METHOD, "")
        self.content = self.input.get(self.CONTENT, "")

    def run(self):
        status, output = self.call_rest(self.url, self.method, self.content)
        if status in self.STATUS_OK:
            status = self.FINISHED
        else:
            status = self.ERROR
        logger.debug("SyncRestTask status %s, output %s" % (status, output))
        return status, output
        #self.update_task(status, resp_content)

    def call_rest(self, url, method, content):
        """
        :param url:
        :param method:
        :param content:
        :return: ret[0] == 0, FINISHED, else ERROR
        """
        pass
