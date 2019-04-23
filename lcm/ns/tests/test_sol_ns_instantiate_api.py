# Copyright 2019 ZTE Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import mock
import uuid

from mock import MagicMock
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from lcm.ns.biz.ns_instant import BuildInWorkflowThread
from lcm.ns.biz.ns_instant import InstantNSService
from lcm.pub.database.models import NSInstModel
from lcm.pub.utils import restcall
from lcm.pub.config import config

nsd_model = json.dumps({
    "model": json.dumps({
        "vnfs": [{
            "vnf_id": "vnf1",
            "properties": {
                "id": "vnfd1",
                "nf_type": "xgw"
            },
            "dependencies": [{
                "vl_id": "5"
            }]
        }],
        "vls": [{
            "vl_id": "5",
            "properties": {}
        }]
    })
})

nsd = json.dumps({
    "vnffgs": [
    ],
    "inputs": {
    },
    "pnfs": [
        {
            "pnf_id": "du",
            "networks": [
            ],
            "description":"",
            "properties":{
                "descriptor_id": "zte_ran_du_0001",
                "descriptor_invariant_id": "1111",
                "provider": "ZTE",
                "version": "1.0",
                "function_description": "RAN DU Function",
                "name": "ZTE RAN DU"
            }
        }
    ],
    "ns_exposed": {
        "external_cps": [
        ],
        "forward_cps": [
        ]
    },
    "graph": {
        "cucp": [
        ],
        "du": [
        ],
        "vl_flat_net": [
            "cucp",
            "cuup"
        ],
        "vl_ext_net": [
            "cucp",
            "cuup"
        ],
        "cuup": [
        ]
    },
    "basepath": "c:\\users\\10030173\\appdata\\local\\temp\\tmpvg5vto",
    "vnfs": [
        {
            "networks": [
                {
                    "key_name": "ran_ext_net",
                    "vl_id": "vl_ext_net"
                },
                {
                    "key_name": "ran_flat_net",
                    "vl_id": "vl_flat_net"
                }
            ],
            "dependencies": [
                {
                    "key_name": "ran_ext_net",
                    "vl_id": "vl_ext_net"
                },
                {
                    "key_name": "ran_flat_net",
                    "vl_id": "vl_flat_net"
                }
            ],
            "vnf_id": "cucp",
            "description": "",
            "properties": {
                "descriptor_id": "zte_ran_cucp_0001",
                "flavour_description": "default",
                "software_version": "1.0.1",
                "flavour_id": "1",
                "descriptor_version": "1.0",
                "provider": "ZTE",
                "id": "zte_ran_cucp_0001",
                "vnfm_info": [
                    "GVNFM-Driver"
                ],
                "product_name":"ran"
            }
        },
        {
            "networks": [
                {
                    "key_name": "ran_ext_net",
                    "vl_id": "vl_ext_net"
                },
                {
                    "key_name": "ran_flat_net",
                    "vl_id": "vl_flat_net"
                }
            ],
            "dependencies": [
                {
                    "key_name": "ran_ext_net",
                    "vl_id": "vl_ext_net"
                },
                {
                    "key_name": "ran_flat_net",
                    "vl_id": "vl_flat_net"
                }
            ],
            "vnf_id": "cuup",
            "description": "",
            "properties": {
                "descriptor_id": "zte_ran_cuup_0001",
                "flavour_description": "default",
                "software_version": "1.0.1",
                "flavour_id": "1",
                "descriptor_version": "1.0",
                "provider": "ZTE",
                "id": "zte_ran_cuup_0001",
                "vnfm_info": [
                    "GVNFM-Driver"
                ],
                "product_name":"ran"
            }
        }
    ],
    "fps": [
    ],
    "vls": [
        {
            "vl_id": "vl_ext_net",
            "description": "",
            "properties": {
                "connectivity_type": {
                    "layer_protocol": "ipv4"
                },
                "vl_profile": {
                    "cidr": "10.0.0.0/24",
                    "max_bit_rate_requirements": {
                        "root": 10000000,
                        "leaf": 10000000
                    },
                    "networkName": "ran_ext_net",
                    "min_bit_rate_requirements": {
                        "root": 10000000,
                        "leaf": 10000000
                    },
                    "dhcpEnabled": False
                },
                "version": "1.0.1"
            }
        },
        {
            "vl_id": "vl_flat_net",
            "description": "",
            "properties": {
                "connectivity_type": {
                    "layer_protocol": "ipv4"
                },
                "vl_profile": {
                    "cidr": "10.1.0.0/24",
                    "max_bit_rate_requirements": {
                        "root": 10000000,
                        "leaf": 10000000
                    },
                    "networkName": "ran_flat_net",
                    "min_bit_rate_requirements": {
                        "root": 10000000,
                        "leaf": 10000000
                    },
                    "dhcpEnabled": False
                },
                "version": "1.0.1"
            }
        }
    ],
    "nested_ns": [
    ],
    "metadata": {
        "template_name": "RAN-NS",
        "template_version": "1.0",
        "template_author": "ZTE"
    }
})
vnfminfo = {"vnfmId": "1"}


class TestInstantiateNsApi(TestCase):

    def setUp(self):
        self.client = APIClient()
        NSInstModel.objects.filter().delete()
        self.url = "/api/nslcm/v1/ns_instances/%s/instantiate"
        self.req_data = {
            "additionalParamForNs": {
                "location": "CPE-DC_RegionOne"
            },
            "nsFlavourId": 'default',
            "localizationLanguage": [{
                "vnfProfileId": "vnfd1",
                "locationConstraints": {
                    "countryCode": "countryCode",
                    # "vimId": "3",
                    "civicAddressElement": [
                        {"caType": "type1",
                         "caValue": 1
                         }
                    ]
                }
            }]
        }
        self.nsd_model = nsd_model
        self.updated_nsd_model = {
            "vnfs": [{
                "dependencies": [{
                    "vl_id": "5"
                }],
                "vnf_id": "vnf1",
                "properties": {
                    "nf_type": "xgw",
                    "id": "vnfd1"
                }
            }],
            "vls": [{
                "vl_id": "5",
                "properties": {
                    "location_info": {
                        "vimid": "3"
                    }
                }
            }]
        }
        self.vnfms = json.dumps({
            "esr-vnfm": [{
                "vnfm-id": "4"
            }]
        })
        self.vnfm = json.dumps({
            "type": "xgw",
            "vim-id": "3",
            "vnfm-id": "4",
            "certificate-url": "http://127.0.0.0/ztevnfm/v1/auth",
            "esr-system-info-list": {
                "esr-system-info": [{
                    "type": "xgw",
                    "vendor": "zte",
                    "version": "1.0",
                    "service-url": "http://127.0.0.0/ztevnfm/v1",
                    "user-name": "admin",
                    "password": "admin123"
                }]
            }
        })
        # NSInstModel(id="2", nspackage_id="7", nsd_id="2", status="active").save()
        self.nsInstanceId = str(uuid.uuid4())
        NSInstModel(id=self.nsInstanceId, nspackage_id="7", nsd_id="2", status="active").save()

    def tearDown(self):
        pass

    @mock.patch.object(restcall, 'call_req')
    @mock.patch('lcm.pub.msapi.sdc_run_catalog.parse_nsd', MagicMock(return_value=nsd_model))
    @mock.patch.object(BuildInWorkflowThread, 'run')
    def test_ns_instantiate_when_succeed_to_enter_workflow(self, mock_run, mock_call_req):
        config.WORKFLOW_OPTION = "buildin"
        mock_call_req.side_effect = [
            [0, self.nsd_model, '200'],
            [0, self.vnfms, '200'],
            [0, self.vnfm, '200']
        ]
        # response = self.client.post(self.url % '2', data=self.req_data, format='json')
        response = self.client.post(self.url % self.nsInstanceId, data=self.req_data, format='json')
        self.assertEqual(status.HTTP_202_ACCEPTED, response.status_code)
        self.assertIsNotNone(response['Location'])
        response = self.client.get(response['Location'], format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @mock.patch.object(InstantNSService, 'do_biz')
    def test_ns_instantiate_normal(self, mock_do_biz):
        mock_do_biz.return_value = {'occ_id': "1"}
        # resp = self.client.post(self.url % '2', data=self.req_data, format='json')
        response = self.client.post(self.url % self.nsInstanceId, data=self.req_data, format='json')
        # self.failUnlessEqual(status.HTTP_202_ACCEPTED, resp.status_code)
        self.failUnlessEqual(status.HTTP_202_ACCEPTED, response.status_code)

    @mock.patch.object(restcall, 'call_req')
    def test_ns_instantiate_when_fail_to_parse_nsd(self, mock_call_req):
        mock_call_req.return_value = [1, "Failed to parse nsd", '500']
        # resp = self.client.post(self.url % '2', data=self.req_data, format='json')
        resp = self.client.post(self.url % self.nsInstanceId, data=self.req_data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    @mock.patch('lcm.ns.biz.ns_instantiate_flow.post_deal')
    @mock.patch.object(restcall, 'call_req')
    @mock.patch('lcm.ns.biz.ns_instantiate_flow.update_job')
    @mock.patch('lcm.pub.msapi.sdc_run_catalog.parse_nsd', MagicMock(return_value=nsd))
    @mock.patch('lcm.pub.msapi.extsys.select_vnfm', MagicMock(return_value=vnfminfo))
    def test_ns_instantiate_with_pnf(self, mock_updata_job, mock_call_req, mock_post_deal):
        config.WORKFLOW_OPTION = "grapflow"
        # NSInstModel(id="1", name="test_ns", nspackage_id="1", status="created").save()
        nsInstanceId = str(uuid.uuid4())
        NSInstModel(id=nsInstanceId, name="test_ns", nspackage_id="1", status="created").save()
        ret = [0, json.JSONEncoder().encode({'jobId': "1", "responseDescriptor": {"progress": 100}}), '200']
        mock_call_req.side_effect = [ret for i in range(1, 20)]
        data = {
            "nsFlavourId": 'default',
            "additionalParamForNs": {
                "sdnControllerId": "2"
            },
            "additionalParamsForVnf": [
                {
                    "vnfProfileId": "zte_ran_cucp_0001",
                    "additionalParams": {"vimId": '{"cloud_owner": "VCPE", "cloud_regionid": "RegionOne"}'}
                },
                {
                    "vnfProfileId": "zte_ran_cuup_0001",
                    "additionalParams": {"vimId": '{"cloud_owner": "VCPE", "cloud_regionid": "RegionOne"}'}
                }
            ],
            "addpnfData": [{
                "pnfId": 1,
                "pnfName": "test_pnf",
                "pnfdId": "zte_ran_du_0001",
                "pnfProfileId": "du"
            }]
        }
        # response = self.client.post(self.url % '1', data=data, format='json')
        response = self.client.post(self.url % nsInstanceId, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertIsNotNone(response['Location'])
        response = self.client.get(response['Location'], format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_method_not_allowed(self):
        response = self.client.put(self.url % self.nsInstanceId, data=self.req_data, format='json')
        self.failUnlessEqual(status.HTTP_405_METHOD_NOT_ALLOWED, response.status_code)
        response = self.client.patch(self.url % self.nsInstanceId, data=self.req_data, format='json')
        self.failUnlessEqual(status.HTTP_405_METHOD_NOT_ALLOWED, response.status_code)
        response = self.client.delete(self.url % self.nsInstanceId, data=self.req_data, format='json')
        self.failUnlessEqual(status.HTTP_405_METHOD_NOT_ALLOWED, response.status_code)
        response = self.client.get(self.url % self.nsInstanceId, data=self.req_data, format='json')
        self.failUnlessEqual(status.HTTP_405_METHOD_NOT_ALLOWED, response.status_code)

    @mock.patch.object(restcall, 'call_req')
    @mock.patch('lcm.pub.msapi.sdc_run_catalog.parse_nsd', MagicMock(return_value=nsd_model))
    @mock.patch.object(BuildInWorkflowThread, 'run')
    def test_ns_instantiate_vcpe(self, mock_run, mock_call_req):
        config.WORKFLOW_OPTION = "buildin"
        vcpe_nsd_model = json.dumps({
            "model": json.dumps({
                "vnfs": [{
                    "vnf_id": "b1bb0ce7-2222-4fa7-95ed-4840d70a1101",
                    "properties": {
                        "id": "vnfd0",
                        "nf_type": "test"
                    },
                    "dependencies": [{
                        "vl_id": "5"
                    }]
                },
                    {
                        "vnf_id": "0408f076-e6c0-4c82-9940-272fddbb82de",
                        "properties": {
                            "id": "vnfd1",
                            "nf_type": "test"
                        },
                        "dependencies": [{
                            "vl_id": "5"
                        }]
                },
                    {
                        "vnf_id": "b1bb0ce7-2222-4fa7-95ed-4840d70a1100",
                        "properties": {
                            "id": "vnfd2",
                            "nf_type": "test"
                        },
                        "dependencies": [{
                            "vl_id": "5"
                        }]
                },
                    {
                        "vnf_id": "b1bb0ce7-2222-4fa7-95ed-4840d70a1102",
                        "properties": {
                            "id": "vnfd3",
                            "nf_type": "test"
                        },
                        "dependencies": [{
                            "vl_id": "5"
                        }]
                },
                    {
                        "vnf_id": "3fca3543-07f5-492f-812c-ed462e4f94f4",
                        "properties": {
                            "id": "vnfd4",
                            "nf_type": "test"
                        },
                        "dependencies": [{
                            "vl_id": "5"
                        }]
                },
                ],
                "vls": [{
                    "vl_id": "5",
                    "properties": {}
                }]
            })
        })
        mock_call_req.side_effect = [
            [0, vcpe_nsd_model, '200'],
            [0, self.vnfms, '200'],
            [0, self.vnfm, '200']
        ]
        req_data = {
            "nsFlavourId": 'default',
            "aditionalParamsForNs": {
                "nfvo": "vfc",
                "nf_naming": "true",
                "multi_stage_design": "false",
                "availability_zone_max_count": "1",
                "xyz": "123",
                "nsd0_providing_service_invariant_uuid": "12204a12-7da2-4ddf-8c2f-992a1a1acebf",
                "nsd0_providing_service_uuid": "5791dbeb-19d4-43e8-bf44-5b327ccf6bca"
            },
            "additionalParamsForVnf": [
                {
                    "vnfProfileId": "b1bb0ce7-2222-4fa7-95ed-4840d70a1101",
                    "additionalParams": {
                        "vimId": "CloudOwner_regionOne"
                    }
                },
                {
                    "vnfProfileId": "0408f076-e6c0-4c82-9940-272fddbb82de",
                    "additionalParams": {
                        "vimId": "CloudOwner_regionOne"
                    }
                },
                {
                    "vnfProfileId": "b1bb0ce7-2222-4fa7-95ed-4840d70a1100",
                    "additionalParams": {
                        "vimId": "CloudOwner_regionOne"
                    }
                },
                {
                    "vnfProfileId": "b1bb0ce7-2222-4fa7-95ed-4840d70a1102",
                    "additionalParams": {
                        "vimId": "CloudOwner_regionOne"
                    }
                },
                {
                    "vnfProfileId": "3fca3543-07f5-492f-812c-ed462e4f94f4",
                    "additionalParams": {
                        "vimId": "CloudOwner_regionOne"
                    }
                }
            ]
        }
        # response = self.client.post(self.url % '2', data=req_data, format='json')
        response = self.client.post(self.url % self.nsInstanceId, data=req_data, format='json')
        self.assertEqual(status.HTTP_202_ACCEPTED, response.status_code)
        self.assertIsNotNone(response['Location'])
        response = self.client.get(response['Location'], format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)