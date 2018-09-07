# Copyright 2017-2018 Intel Corporation.
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
import json

from lcm.pub.database.models import OOFDataModel

logger = logging.getLogger(__name__)


class PlaceVnfs(object):
    def __init__(self, data):
        self.data = data
        self.placements = ""

    def validateCallbackResponse(self):
        if self.data == "":
            logger.error("Error occurred in Homing: OOF Async Callback Response is empty")
            return False
        if self.data.get('requestStatus') == "completed":
            if self.data.get("solutions").get("placementSolutions"):
                self.placements = self.data.get("solutions").get("placementSolutions")
                logger.debug("Got placement solutions in OOF Async Callback response")
                return True
            else:
                logger.error("Error occurred in Homing: OOF Async Callback Response "
                             "does not contain placement solution")
                return False
        else:
            logger.error(
                "Error occurred in Homing: Request has not been completed, the request status is %s" % self.data.get(
                    'requestStatus'))
            if self.data.get("statusMessage"):
                logger.debug("StatusMessage for the request is %s" % self.data.get("statusMessage"))
            return False

    def extract(self):
        params = ["locationId", "vimId", "oofDirectives"]
        vim_info = {}
        if not self.validateCallbackResponse():
            logger.error("OOF request Failed")
            return
        for item in self.placements:
            if not item:
                logger.debug("No solution found for request %s " % self.data.get("requestId"))
                OOFDataModel.objects.filter(request_id=self.data.get("requestId"),
                                            transaction_id=self.data.get("transactionId")).update(
                    request_status=self.data.get("requestStatus"),
                    vim_id="no-solution",
                    cloud_owner="no-solution",
                    cloud_region_id="no-solution",
                    vduinfo="no-solution")
                return
            for placement in item:
                assignmentInfo = placement.get("assignmentInfo")
                if not assignmentInfo:
                    logger.debug(
                        "No assignment info inside Homing response for request %s" % self.data.get("requestId"))
                    OOFDataModel.objects.filter(request_id=self.data.get("requestId"),
                                                transaction_id=self.data.get("transactionId")).update(
                        request_status=self.data.get("requestStatus"),
                        vim_id="none",
                        cloud_owner="none",
                        cloud_region_id="none",
                        vduinfo="none"
                    )
                    return
                for info in assignmentInfo:
                    if info.get('key') in params:
                        vim_info[info.get('key')] = info.get('value')
                    if not vim_info.get("oofDirectives"):
                        logger.warn("Missing flavor info as no directive found in response")
                    vduinfo = self.get_info_from_directives(
                        vim_info['oofDirectives'])
                    if vduinfo:
                        OOFDataModel.objects.filter(request_id=self.data.get("requestId"),
                                                    transaction_id=self.data.get(
                                                        "transactionId")).update(
                            request_status=self.data.get("requestStatus"),
                            vim_id=vim_info['vimId'],
                            cloud_owner=placement.get("solution").get("cloudOwner"),
                            cloud_region_id=vim_info['locationId'],
                            vduinfo=vduinfo
                        )
                        logger.debug(
                            "Placement solution has been stored for request %s " % self.data.get(
                                "requestId"))
                        return "Done"

    def get_info_from_directives(self, directives):
        vduinfo = []
        for directive in directives:
            if directive.get("type") == "tocsa.nodes.nfv.Vdu.Compute":
                vdu = {'vduName': directive.get("id")}
                other_directives = []
                for item in directive.get("directives"):
                    if item.get("type") == "flavor_directive":
                        for attribute in item.get("attributes"):
                            vdu['flavorName'] = attribute.get("attribute_value")
                    else:
                        other_directives.append(item)
                if other_directives:
                    other_directives = json.dumps(other_directives)
                vdu['directive'] = other_directives
                vduinfo.append(vdu)
            else:
                logger.warn("Find unrecognized type %s " % directive.get("type"))
        if vduinfo:
            vduinfo = json.dumps(vduinfo)
            return vduinfo
        else:
            logger.warn("No OOF directive for VDU")
            return None
