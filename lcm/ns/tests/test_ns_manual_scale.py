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

import uuid

import mock
from django.test import Client
from django.test import TestCase
from rest_framework import status

from lcm.ns.const import NS_INST_STATUS
from lcm.ns.ns_manual_scale import NSManualScaleService
from lcm.pub.database.models import NSInstModel
from lcm.pub.exceptions import NSLCMException
from lcm.pub.utils import restcall
from lcm.pub.utils.jobutil import JobUtil, JOB_TYPE


class TestNsManualScale(TestCase):
    def setUp(self):
        self.nsd_id = str(uuid.uuid4())
        self.ns_package_id = str(uuid.uuid4())
        self.ns_inst_id = str(uuid.uuid4())
        self.job_id = JobUtil.create_job("NS", JOB_TYPE.MANUAL_SCALE_VNF, self.ns_inst_id)

        self.client = Client()
        NSInstModel(id=self.ns_inst_id, name="abc", nspackage_id="7", nsd_id="111").save()

    def tearDown(self):
        NSInstModel.objects.filter().delete()

    @mock.patch.object(NSManualScaleService, 'run')
    def test_ns_manual_scale(self, mock_run):
        data = {
            'nsdid': self.nsd_id,
            'nsname': 'ns',
            'description': 'description',
            "scaleNsByStepsData": [{
                "scaleNsByStepsData": [{
                    "aspectId": "1",
                    "numberOfSteps": 1,
                    "scalingDirection": "0"
                }]
            }]
        }
        response = self.client.post("/api/nslcm/v1/ns/%s/scale" % self.nsd_id, data=data)
        self.failUnlessEqual(status.HTTP_202_ACCEPTED, response.status_code)

    @mock.patch.object(restcall, 'call_req')
    def test_ns_manual_scale_thread(self, mock_call):
        data = {
            'nsdid': self.nsd_id,
            'nsname': 'ns',
            'description': 'description',
            "scaleNsByStepsData": [{
                "scaleNsByStepsData": [{
                    "aspectId": "1",
                    "numberOfSteps": 1,
                    "scalingDirection": "0"
                }]
            }]
        }
        NSManualScaleService(self.ns_inst_id, data, self.job_id).run()
        self.assertTrue(NSInstModel.objects.get(id=self.ns_inst_id).status, NS_INST_STATUS.ACTIVE)

    def test_swagger_ok(self):
        resp = self.client.get("/api/nslcm/v1/swagger.json", format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    @mock.patch.object(NSManualScaleService, 'start')
    def test_ns_manual_scale_empty_data(self, mock_start):
        mock_start.side_effect = NSLCMException("NS scale failed.")

        data = {}

        response = self.client.post("/api/nslcm/v1/ns/%s/scale" % self.nsd_id, data=data)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn("error", response.data)

    @mock.patch.object(NSManualScaleService, 'start')
    def test_ns_manual_scale_non_existing_nsd_id(self, mock_start):
        mock_start.side_effect = NSLCMException("NS scale failed.")
        nsd_id = '1111'
        data = {
            'nsdid': nsd_id,
            'nsname': 'ns',
            'description': 'description',
            "scaleNsByStepsData": [{
                "scaleNsByStepsData": [{
                    "aspectId": "1",
                    "numberOfSteps": 1,
                    "scalingDirection": "0"
                }]
            }]
        }
        response = self.client.post("/api/nslcm/v1/ns/%s/scale" % nsd_id, data=data)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn("error", response.data)
