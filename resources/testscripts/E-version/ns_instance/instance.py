# Copyright (c) 2019, CMCC Technologies Co., Ltd.
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import httplib2
import sys
inst_id = sys.argv[1]

data = {
    "additionalParamForNs": {
        "sdnControllerId": "2"
    },
    "locationConstraints": [{
        "vnfProfileId": "b1bb0ce7-2222-4fa7-95ed-4840d70a1177",
        "locationConstraints": {
            "vimId": "CloudOwner_ONAP-POD-01-Rail-07"
        }
    }]
}

headers = {'content-type': 'application/json', 'accept': 'application/json'}
http = httplib2.Http()
resp, resp_content = http.request('http://10.12.5.131:30280/api/nslcm/v1/ns/' + inst_id + '/instantiate',
                                  method="POST",
                                  body=json.dumps(data),
                                  headers=headers)
print(resp['status'], resp_content)
