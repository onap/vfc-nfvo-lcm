# Copyright 2016 ZTE Corporation.
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

from django.conf.urls import include, url
from drf_yasg import openapi

from lcm.pub.config.config import REG_TO_MSB_WHEN_START, REG_TO_MSB_REG_URL, REG_TO_MSB_REG_PARAM
from lcm.pub.config.config import DEPLOY_WORKFLOW_WHEN_START

swagger_info = openapi.Info(
    title="vfc-nfvo-lcm API",
    default_version='v1',
    description="""

The `swagger-ui` view can be found [here](/cached/swagger).
The `ReDoc` view can be found [here](/cached/redoc).
The swagger YAML document can be found [here](/cached/swagger.yaml)."""
)

urlpatterns = [
    url(r'^', include('lcm.samples.urls')),
    url(r'^', include('lcm.packages.urls')),
    url(r'^', include('lcm.ns.vnfs.urls')),
    url(r'^', include('lcm.ns.vls.urls')),
    url(r'^', include('lcm.ns.sfcs.urls')),
    url(r'^', include('lcm.ns.urls')),
    url(r'^', include('lcm.jobs.urls')),
    url(r'^', include('lcm.workflows.urls')),
    url(r'^', include('lcm.swagger.urls')),
    url(r'^', include('lcm.v2.urls')),
]

# regist to MSB when startup
if REG_TO_MSB_WHEN_START:
    import json
    from lcm.pub.utils.restcall import req_by_msb
    req_by_msb(REG_TO_MSB_REG_URL, "POST", json.JSONEncoder().encode(REG_TO_MSB_REG_PARAM))

# deploy workflow when startup
if DEPLOY_WORKFLOW_WHEN_START:
    from lcm.workflows import auto_deploy
    auto_deploy.deploy_workflow_on_startup()
