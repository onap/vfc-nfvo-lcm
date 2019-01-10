# Copyright 2018 ZTE Corporation.
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

from rest_framework import serializers
from lcm.ns_pnfs.serializers.pnf_serializer import PnfInstanceSerializer
<<<<<<< HEAD
=======
from lcm.ns.serializers.pub_serializers import IpOverEthernetAddressDataSerializer
>>>>>>> separate ns-inst


class VnfInstSerializer(serializers.Serializer):
    vnfInstanceId = serializers.CharField(help_text="ID of VNF instance", required=True)
    vnfInstanceName = serializers.CharField(help_text="Name of VNF instance", required=False, allow_null=True, allow_blank=True)
    vnfdId = serializers.CharField(help_text="ID of VNFD", required=False, allow_null=True, allow_blank=True)


class CpInstInfoSerializer(serializers.Serializer):
    cpInstanceId = serializers.CharField(help_text="ID of CP instance", required=True)
    cpInstanceName = serializers.CharField(help_text="Name of CP instance", required=False, allow_null=True, allow_blank=True)
    cpdId = serializers.CharField(help_text="ID of CPD", required=False, allow_null=True, allow_blank=True)


class VlInstSerializer(serializers.Serializer):
    vlInstanceId = serializers.CharField(help_text="ID of VL instance", required=True)
    vlInstanceName = serializers.CharField(help_text="Name of VL instance", required=False, allow_null=True, allow_blank=True)
    vldId = serializers.CharField(help_text="ID of VLD", required=False, allow_null=True, allow_blank=True)
    relatedCpInstanceId = CpInstInfoSerializer(help_text="Related CP instances", many=True)


class VnffgInstSerializer(serializers.Serializer):
    vnffgInstanceId = serializers.CharField(help_text="ID of VNFFG instance", required=True)
    vnfdId = serializers.CharField(help_text="ID of VNFD", required=False, allow_null=True, allow_blank=True)
    pnfId = serializers.CharField(help_text="ID of PNF", required=False, allow_null=True, allow_blank=True)
    virtualLinkId = serializers.CharField(help_text="ID of virtual link", required=False, allow_null=True, allow_blank=True)
    cpdId = serializers.CharField(help_text="ID of CPD", required=False, allow_null=True, allow_blank=True)
    nfp = serializers.CharField(help_text="nfp", required=False, allow_null=True, allow_blank=True)


class QueryNsRespSerializer(serializers.Serializer):
    nsInstanceId = serializers.CharField(help_text="ID of NS instance", required=True)
    nsName = serializers.CharField(help_text="Name of NS instance", required=False, allow_null=True, allow_blank=True)
    description = serializers.CharField(help_text="Description of NS instance", required=False, allow_null=True, allow_blank=True)
    nsdId = serializers.CharField(help_text="ID of NSD", required=True)
    vnfInfo = VnfInstSerializer(help_text="VNF instances", many=True, required=False, allow_null=True)
    pnfInfo = PnfInstanceSerializer(help_text="PNF instances", many=True, required=False, allow_null=True)
    vlInfo = VlInstSerializer(help_text="VL instances", many=True, required=False, allow_null=True)
    vnffgInfo = VnffgInstSerializer(help_text="VNFFG instances", many=True, required=False, allow_null=True)
    nsState = serializers.CharField(help_text="State of NS instance", required=False, allow_null=True, allow_blank=True)


class VnfLocationSerializer(serializers.Serializer):
    vimId = serializers.CharField(help_text="ID of VIM", required=False, allow_null=True, allow_blank=True)


class LocationConstraintSerializer(serializers.Serializer):
    vnfProfileId = serializers.CharField(help_text="ID of VNF profile", required=False, allow_null=True, allow_blank=True)
    locationConstraints = VnfLocationSerializer(help_text="Location constraint", required=False, allow_null=True)


class AddressRange(serializers.Serializer):
    minAddress = serializers.IPAddressField(help_text="Lowest IP address belonging to the range.", required=True)
    maxAddress = serializers.IPAddressField(help_text="Highest IP address belonging to the range.", required=True)


# class IpOverEthernetSerializer(serializers.Serializer):
#     macAddress = serializers.CharField(help_text="MAC address.", required=False, allow_null=True, allow_blank=True)
#     ipAddresses = IpAddress(help_text="List of IP addresses to assign to the extCP instance.", required=False, many=True)


class CpProtocolInfoSerializer(serializers.Serializer):
    layerProtocol = serializers.ChoiceField(
        help_text="The identifier of layer(s) and protocol(s) associated to the network address information.",
        choices=["IP_OVER_ETHERNET"],
        required=True,
        allow_null=False)
    ipOverEthernet = IpOverEthernetAddressDataSerializer(
        help_text="IP addresses over Ethernet to assign to the extCP instance.",
        required=False,
        allow_null=True)


class PnfExtCpData(serializers.Serializer):
    cpInstanceId = serializers.CharField(help_text="Identifier of the CP", required=False, allow_null=True, allow_blank=True)
    cpdId = serializers.CharField(help_text="Identifier of the Connection Point Descriptor", required=False, allow_null=True, allow_blank=True)
    cpProtocolData = CpProtocolInfoSerializer(help_text="Address assigned for this CP", required=True, allow_null=False, many=True)


class AddPnfData(serializers.Serializer):
    pnfId = serializers.CharField(help_text="Identifier of the PNF", required=True, allow_null=False, allow_blank=True)
    pnfName = serializers.CharField(help_text="Name of the PNF", required=True, allow_null=True, allow_blank=True)
    pnfdId = serializers.CharField(help_text="Identifier of the PNFD", required=True, allow_null=False, allow_blank=True)
    pnfProfileId = serializers.CharField(help_text="Identifier of related PnfProfile in the NSD", required=True, allow_null=False, allow_blank=True)
    cpData = PnfExtCpData(help_text="Address assigned for the PNF external CP", required=False, many=True)


class InstantNsReqSerializer(serializers.Serializer):
    locationConstraints = LocationConstraintSerializer(help_text="Location constraints", required=False, many=True)
    additionalParamForNs = serializers.DictField(
        help_text="Additional param for NS",
        child=serializers.CharField(help_text="KeyValue Pairs", allow_blank=True),
        required=False,
        allow_null=True
    )
    addpnfData = AddPnfData(help_text="Information on the PNF", required=False, many=True)


class NsOperateJobSerializer(serializers.Serializer):
    jobId = serializers.CharField(help_text="ID of NS operate job", required=True)


class TerminateNsReqSerializer(serializers.Serializer):
    terminationType = serializers.CharField(help_text="Type of NS termination", required=False, allow_null=True, allow_blank=True)
    gracefulTerminationTimeout = serializers.CharField(help_text="Timeout of NS graceful termination", required=False, allow_null=True, allow_blank=True)


class InstNsPostDealReqSerializer(serializers.Serializer):
    status = serializers.CharField(help_text="Status of NS Inst", required=True)


class ScaleNsByStepsSerializer(serializers.Serializer):
    aspectId = serializers.CharField(help_text="ID of aspect", required=True)
    numberOfSteps = serializers.CharField(help_text="Number of steps", required=True)
    scalingDirection = serializers.CharField(help_text="Scaling direction", required=True)


class ScaleNsDataSerializer(serializers.Serializer):
    scaleNsByStepsData = ScaleNsByStepsSerializer(help_text="Scale NS by steps data", many=True)


class ManualScaleNsReqSerializer(serializers.Serializer):
    scaleType = serializers.CharField(help_text="Type of NS Scale", required=True)
    scaleNsData = ScaleNsDataSerializer(help_text="Scale NS data", many=True)
