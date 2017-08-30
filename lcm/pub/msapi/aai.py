# Copyright 2017 ZTE Corporation.
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

import json
import logging
import uuid

from lcm.pub.exceptions import NSLCMException
from lcm.pub.utils import restcall
from lcm.pub.config.config import AAI_BASE_URL, AAI_USER, AAI_PASSWD

logger = logging.getLogger(__name__)


def call_aai(resource, method, content=''):
    additional_headers = {
        'X-FromAppId': 'VFC-NFVO-LCM',
        'X-TransactionId': str(uuid.uuid1())
    }
    return restcall.call_req(base_url=AAI_BASE_URL, 
        user=AAI_USER, 
        passwd=AAI_PASSWD, 
        auth_type=restcall.rest_no_auth, 
        resource=resource, 
        method=method, 
        content=content,
        additional_headers=additional_headers)


