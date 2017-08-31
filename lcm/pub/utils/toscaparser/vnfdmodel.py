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

import functools

from lcm.pub.utils.toscaparser import EtsiNsdInfoModel


class EtsiVnfdInfoModel(EtsiNsdInfoModel):

    def __init__(self, path, params):
        super(EtsiVnfdInfoModel, self).__init__(path, params)

    def parseModel(self, tosca):
        self.buidMetadata(tosca)
        if hasattr(tosca, 'topology_template') and hasattr(tosca.topology_template, 'inputs'):
            self.inputs = self.buildInputs(tosca.topology_template.inputs)

        nodeTemplates = map(functools.partial(self.buildNode, inputs=tosca.inputs, parsed_params=tosca.parsed_params),
                            tosca.nodetemplates)

        self.services = self._get_all_services(nodeTemplates)
        self.vcloud = self._get_all_vcloud(nodeTemplates)
        self.vcenter = self._get_all_vcenter(nodeTemplates)
        self.image_files = self._get_all_image_file(nodeTemplates)
        self.local_storages = self._get_all_local_storage(nodeTemplates)
        self.volume_storages = self._get_all_volume_storage(nodeTemplates)


    def _get_all_services(self, nodeTemplates):
        ret = []
        for node in nodeTemplates:
            if self.isService(node):
                service = {}
                service['serviceId'] = node['name']
                if 'description' in node:
                    service['description'] = node['description']
                service['properties'] = node['properties']
                service['dependencies'] = map(lambda x: self.get_requirement_node_name(x),
                                              self.getNodeDependencys(node))
                service['networks'] = map(lambda x: self.get_requirement_node_name(x), self.getVirtualLinks(node))

                ret.append(service)
        return ret

    def _get_all_vcloud(self, nodeTemplates):
        rets = []
        for node in nodeTemplates:
            if self._isVcloud(node):
                ret = {}
                if 'vdc_name' in node['properties']:
                    ret['vdc_name'] = node['properties']['vdc_name']
                else:
                    ret['vdc_name'] = ""
                if 'storage_clusters' in node['properties']:
                    ret['storage_clusters'] = node['properties']['storage_clusters']
                else:
                    ret['storage_clusters'] = []

                rets.append(ret)
        return rets

    def _isVcloud(self, node):
        return node['nodeType'].upper().find('.VCLOUD.') >= 0 or node['nodeType'].upper().endswith('.VCLOUD')

    def _get_all_vcenter(self, nodeTemplates):
        rets = []
        for node in nodeTemplates:
            if self._isVcenter(node):
                ret = {}
                if 'compute_clusters' in node['properties']:
                    ret['compute_clusters'] = node['properties']['compute_clusters']
                else:
                    ret['compute_clusters'] = []
                if 'storage_clusters' in node['properties']:
                    ret['storage_clusters'] = node['properties']['storage_clusters']
                else:
                    ret['storage_clusters'] = []
                if 'network_clusters' in node['properties']:
                    ret['network_clusters'] = node['properties']['network_clusters']
                else:
                    ret['network_clusters'] = []

                rets.append(ret)
        return rets

    def _isVcenter(self, node):
        return node['nodeType'].upper().find('.VCENTER.') >= 0 or node['nodeType'].upper().endswith('.VCENTER')

    def _get_all_image_file(self, nodeTemplates):
        rets = []
        for node in nodeTemplates:
            if self._isImageFile(node):
                ret = {}
                ret['image_file_id'] = node['name']
                if 'description' in node:
                    ret['description'] = node['description']
                ret['properties'] = node['properties']

                rets.append(ret)
        return rets

    def _isImageFile(self, node):
        return node['nodeType'].upper().find('.IMAGEFILE.') >= 0 or node['nodeType'].upper().endswith('.IMAGEFILE')

    def _get_all_local_storage(self, nodeTemplates):
        rets = []
        for node in nodeTemplates:
            if self._isLocalStorage(node):
                ret = {}
                ret['local_storage_id'] = node['name']
                if 'description' in node:
                    ret['description'] = node['description']
                ret['properties'] = node['properties']

                rets.append(ret)
        return rets

    def _isLocalStorage(self, node):
        return node['nodeType'].upper().find('.LOCALSTORAGE.') >= 0 or node['nodeType'].upper().endswith(
            '.LOCALSTORAGE')

    def _get_all_volume_storage(self, nodeTemplates):
        rets = []
        for node in nodeTemplates:
            if self._isVolumeStorage(node):
                ret = {}
                ret['volume_storage_id'] = node['name']
                if 'description' in node:
                    ret['description'] = node['description']
                ret['properties'] = node['properties']
                ret['image_file'] = map(lambda x: self.get_requirement_node_name(x),
                                        self.getRequirementByName(node, 'image_file'))

                rets.append(ret)
        return rets

    def _isVolumeStorage(self, node):
        return node['nodeType'].upper().find('.VOLUMESTORAGE.') >= 0 or node['nodeType'].upper().endswith(
            '.VOLUMESTORAGE')
