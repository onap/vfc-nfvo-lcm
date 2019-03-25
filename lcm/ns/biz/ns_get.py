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

import json
import logging

from lcm.ns.const import OWNER_TYPE
from lcm.pub.utils import restcall
from lcm.pub.config.config import MSB_BASE_URL
from lcm.pub.database.models import NSInstModel, NfInstModel, VLInstModel, CPInstModel, VNFFGInstModel

logger = logging.getLogger(__name__)
NS_INSTANCE_BASE_URI = MSB_BASE_URL + '/api/nslcm/v1/ns_instances/%s'


class GetNSInfoService(object):
    def __init__(self, ns_filter=None):
        self.ns_filter = ns_filter

    def get_ns_info(self, is_sol=False):
        ns_insts = None
        if self.ns_filter and "ns_inst_id" in self.ns_filter:
            ns_inst_id = self.ns_filter["ns_inst_id"]
            ns_insts = NSInstModel.objects.filter(id=ns_inst_id)
        else:
            ns_insts = NSInstModel.objects.all()
        return [self.get_single_ns_info(ns_inst, is_sol) for ns_inst in ns_insts]

    def get_single_ns_info(self, ns_inst, is_sol=False):
        if is_sol:
            return {
                'id': ns_inst.id,
                'nsInstanceName': ns_inst.name,
                'nsInstanceDescription': ns_inst.description,
                'nsdId': ns_inst.nsd_id,
                'nsdInvariantId': ns_inst.nsd_invariant_id,
                'nsdInfoId': ns_inst.nspackage_id,
                'flavourId': ns_inst.flavour_id,
                'nsState': ns_inst.status,
                # todo 'nsScaleStatus':{}
                # todo  'additionalAffinityOrAntiAffinityRule':{}
                'vnfInstance': self.get_vnf_infos(ns_inst.id, is_sol),
                # todo 'pnfInfo': self.get_pnf_infos(ns_inst.id,is_sol),
                'virtualLinkInfo': self.get_vl_infos(ns_inst.id, is_sol),
                # todo 'vnffgInfo': self.get_vnffg_infos(ns_inst.id, ns_inst.nsd_model),
                # todo  'sapInfo':{},
                # todo  nestedNsInstanceId
                '_links': {
                    'self': {'href': NS_INSTANCE_BASE_URI % ns_inst.id},
                    'instantiate': {'href': NS_INSTANCE_BASE_URI + '/instantiate' % ns_inst.id},
                    'terminate': {'href': NS_INSTANCE_BASE_URI + '/terminate' % ns_inst.id},
                    'update': {'href': NS_INSTANCE_BASE_URI + '/update' % ns_inst.id},
                    'scale': {'href': NS_INSTANCE_BASE_URI + '/scale' % ns_inst.id},
                    'heal': {'href': NS_INSTANCE_BASE_URI + '/heal' % ns_inst.id}
                }
            }
        return {
            'nsInstanceId': ns_inst.id,
            'nsName': ns_inst.name,
            'description': ns_inst.description,
            'nsdId': ns_inst.nsd_id,
            'nsdInvariantId': ns_inst.nsd_invariant_id,
            'vnfInfo': self.get_vnf_infos(ns_inst.id, is_sol),
            'pnfInfo': self.get_pnf_infos(ns_inst.id),
            'vlInfo': self.get_vl_infos(ns_inst.id, is_sol),
            'vnffgInfo': self.get_vnffg_infos(ns_inst.id, ns_inst.nsd_model, is_sol),
            'nsState': ns_inst.status}

    @staticmethod
    def get_vnf_infos(ns_inst_id, is_sol):
        vnfs = NfInstModel.objects.filter(ns_inst_id=ns_inst_id)
        if is_sol:
            return [{
                'id': vnf.nfinstid,
                'vnfInstanceName': vnf.nf_name,
                'vnfdId': vnf.template_id,
                'vnfProvider': vnf.vendor,
                'vnfSoftwareVersion': vnf.version,
                'vnfProductName': vnf.nf_name,  # todo
                'vnfdVersion': vnf.version,  # todo
                'vnfPkgId': vnf.package_id,
                'instantiationState': vnf.status
            } for vnf in vnfs]
        return [{
            'vnfInstanceId': vnf.nfinstid,
            'vnfInstanceName': vnf.nf_name,
            'vnfProfileId': vnf.vnf_id} for vnf in vnfs]

    def get_vl_infos(self, ns_inst_id, is_sol):
        vls = VLInstModel.objects.filter(ownertype=OWNER_TYPE.NS, ownerid=ns_inst_id)
        if is_sol:
            return [
                {
                    'id': vl.vlinstanceid,
                    'nsVirtualLinkDescId': vl.vldid,
                    'nsVirtualLinkProfileId': vl.vldid,
                    'vlInstanceName': vl.vlinstancename,
                    'resourceHandle': {
                        'vimId': vl.vimId,
                        'resourceId': vl.relatednetworkid,
                        'vimLevelResourceType': vl.vltype
                    },
                    # todo 'linkPort': self.get_cp_infos(vl.vlinstanceid,is_sol),
                    'networkId': vl.relatednetworkid,
                    'subNetworkid': vl.relatedsubnetworkid
                } for vl in vls]

        return [{
            'vlInstanceId': vl.vlinstanceid,
            'vlInstanceName': vl.vlinstancename,
            'vldId': vl.vldid,
            'relatedCpInstanceId': self.get_cp_infos(vl.vlinstanceid)} for vl in vls]

    @staticmethod
    def get_cp_infos(vl_inst_id):
        cps = CPInstModel.objects.filter(relatedvl__icontains=vl_inst_id)
        return [{
            'cpInstanceId': cp.cpinstanceid,
            'cpInstanceName': cp.cpname,
            'cpdId': cp.cpdid} for cp in cps]

    def get_vnffg_infos(self, ns_inst_id, nsd_model, is_sol):
        vnffgs = VNFFGInstModel.objects.filter(nsinstid=ns_inst_id)
        return [{
            'vnffgInstanceId': vnffg.vnffginstid,
            'vnfId': self.convert_string_to_list(vnffg.vnflist),
            'pnfId': self.get_pnf_ids(nsd_model),
            'virtualLinkId': self.convert_string_to_list(vnffg.vllist),
            'cpId': self.convert_string_to_list(vnffg.cplist),
            'nfp': self.convert_string_to_list(vnffg.fplist)} for vnffg in vnffgs]

    @staticmethod
    def get_pnf_ids(nsd_model):
        context = json.loads(nsd_model)
        pnfs = context['pnfs']
        return [pnf['pnf_id'] for pnf in pnfs]

    @staticmethod
    def convert_string_to_list(detail_id_string):
        if not detail_id_string:
            return None
        return detail_id_string.split(',')

    @staticmethod
    def get_pnf_infos(ns_instance_id):
        uri = "api/nslcm/v1/pnfs?nsInstanceId=%s" % ns_instance_id
        ret = restcall.req_by_msb(uri, "GET")
        if ret[0] == 0:
            return json.loads(ret[1])
        else:
            return []
