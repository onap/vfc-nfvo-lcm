from django.test import TestCase
from lcm.pub.utils.scaleaspect import get_scale_vnf_data_package
from lcm.pub.utils.scaleaspect import get_vnf_scale_info_package
from lcm.pub.utils.scaleaspect import get_vnf_data_package
from lcm.pub.utils.scaleaspect import get_json_data
from lcm.pub.utils.scaleaspect import get_nsdId
from lcm.pub.utils.scaleaspect import deal_vnf_scale_info
from lcm.pub.database.models import NfInstModel
from lcm.pub.database.models import NSInstModel
from lcm.pub.msapi import catalog
from lcm.pub.utils.timeutil import now_time
import os
import mock


class TestScaleAspect(TestCase):

    def setUp(self):
        curdir_path = os.path.dirname(
            os.path.dirname(
                os.path.dirname(
                    os.path.abspath(__file__))))
        filename = curdir_path + "/ns/data/scalemapping.json"
        self.scaling_map_json = get_json_data(filename)

        self.initInstModel()

        self.scaleNsData = {
            "aspectId": "TIC_EDGE_IMS",
            "numberOfSteps": "1",
            "scalingDirection": "UP"
        }

    def initInstModel(self):
        self.nsd_id = "23"
        self.ns_inst_id = "1"
        self.ns_name = "ns_1"
        self.ns_package_id = "ns_zte"
        self.description = "ns_zte"
        self.global_customer_id = "global_customer_id"
        self.service_type = "service_role"

        NSInstModel(id=self.ns_inst_id,
                    name=self.ns_name,
                    nspackage_id=self.ns_package_id,
                    nsd_id=self.nsd_id,
                    description=self.description,
                    status='empty',
                    lastuptime=now_time(),
                    global_customer_id=self.global_customer_id,
                    service_type=self.service_type).save()

        self.nf_inst_id = "231"
        self.ns_inst_id = "1"
        self.nf_name = "name_1"
        self.vnf_id = "1"
        self.vnfm_inst_id = "1"
        self.package_id = "nf_zte_cscf"
        self.nf_uuid = "abc34-345a-de13-ab85-ijs9"

        NfInstModel.objects.create(
            nfinstid=self.nf_inst_id,
            nf_name=self.nf_name,
            vnf_id=self.vnf_id,
            vnfm_inst_id=self.vnfm_inst_id,
            ns_inst_id=self.ns_inst_id,
            max_cpu='14',
            max_ram='12296',
            max_hd='101',
            max_shd="20",
            max_net=10,
            status='active',
            mnfinstid=self.nf_uuid,
            package_id=self.package_id,
            vnfd_model='{"metadata": {"vnfdId": "1","vnfdName": "PGW001",'
            '"vnfProvider": "zte","vnfdVersion": "V00001","vnfVersion": "V5.10.20",'
            '"productType": "CN","vnfType": "PGW",'
            '"description": "PGW VNFD description",'
            '"isShared":true,"vnfExtendType":"driver"}}')

        # Create a second vnf instance
        self.nf_inst_id = "232"
        self.package_id = "nf_zte_hss"
        self.nf_uuid = "abc34-3g5a-de13-ab85-ijs3"

        NfInstModel.objects.create(
            nfinstid=self.nf_inst_id,
            nf_name=self.nf_name,
            vnf_id=self.vnf_id,
            vnfm_inst_id=self.vnfm_inst_id,
            ns_inst_id=self.ns_inst_id,
            max_cpu='14',
            max_ram='12296',
            max_hd='101',
            max_shd="20",
            max_net=10,
            status='active',
            mnfinstid=self.nf_uuid,
            package_id=self.package_id,
            vnfd_model='{"metadata": {"vnfdId": "1","vnfdName": "PGW001",'
                       '"vnfProvider": "zte","vnfdVersion": "V00001","vnfVersion": "V5.10.20",'
                       '"productType": "CN","vnfType": "PGW",'
                       '"description": "PGW VNFD description",'
                       '"isShared":true,"vnfExtendType":"driver"}}')

    def tearDown(self):
        NSInstModel().clean()
        NfInstModel().clean()

    def test_get_vnf_data_package(self):
        vnf_data_package = get_vnf_data_package(
            self.scaling_map_json, "1", "TIC_EDGE_IMS", "1", "IN")
        self.assertIsNotNone(vnf_data_package)
        self.assertEqual(2, vnf_data_package.__len__())

    def test_get_vnf_scale_info_package(self):
        scale_vnf_info_list = get_vnf_scale_info_package(
            self.scaling_map_json, "23", "TIC_EDGE_IMS", "1")
        self.assertIsNotNone(scale_vnf_info_list)
        self.assertEqual(2, scale_vnf_info_list.__len__())

    @mock.patch.object(catalog, 'get_scalingmap_json_package')
    def test_get_scale_vnf_data_package(
            self, mock_get_scalingmap_json_package):
        mock_get_scalingmap_json_package.return_value = self.scaling_map_json

        scale_vnf_data = get_scale_vnf_data_package(self.scaleNsData, "1")
        self.assertIsNotNone(scale_vnf_data)
        self.assertEqual(2, scale_vnf_data.__len__())

    def test_deal_vnf_scale_info(self):
        vnf_scale_info_list = [
            {
                "vnfd_id": "nf_zte_cscf",
                "vnf_scaleAspectId": "mpu",
                "numberOfSteps": "1"
            },
            {
                "vnfd_id": "nf_zte_hss",
                "vnf_scaleAspectId": "mpu",
                "numberOfSteps": "1"
            }
        ]
        result = deal_vnf_scale_info(vnf_scale_info_list)
        self.assertEqual(result[0]["numberOfSteps"], vnf_scale_info_list[0]["numberOfSteps"])
        self.assertEqual(result[0]["vnf_scaleAspectId"], vnf_scale_info_list[0]["vnf_scaleAspectId"])
        self.assertEqual(result[1]["numberOfSteps"], vnf_scale_info_list[0]["numberOfSteps"])
        self.assertEqual(result[1]["vnf_scaleAspectId"], vnf_scale_info_list[0]["vnf_scaleAspectId"])
        self.assertEqual("231", result[0]["vnfInstanceId"])
        self.assertEqual("232", result[1]["vnfInstanceId"])
        self.assertNotIn("vnfd_id", result[0])
        self.assertNotIn("vnfd_id", result[1])

    def test_get_nsdId(self):
        nsd_id = get_nsdId("1")
        self.assertEqual("23", nsd_id)
