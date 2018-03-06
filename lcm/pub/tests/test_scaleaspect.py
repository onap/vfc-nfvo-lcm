from django.test import TestCase
from lcm.pub.utils.scaleaspect import get_json_data
from lcm.pub.utils.scaleaspect import get_nsdId
from lcm.pub.database.models import NfInstModel
from lcm.pub.database.models import NSInstModel
from lcm.pub.utils.timeutil import now_time
import os


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

    def test_get_nsdId(self):
        nsd_id = get_nsdId("1")
        self.assertEqual("23", nsd_id)
