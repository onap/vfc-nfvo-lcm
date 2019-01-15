# Copyright (c) 2018, CMCC Technologies Co., Ltd.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from rest_framework import serializers

from lcm.ns.serializers.pub_serializers import IpOverEthernetAddressDataSerializer
from lcm.ns.serializers.update_serializers import AddPnfDataSerializer, VnfInstanceDataSerializer


class CpProtocolDataSerializer(serializers.Serializer):
    layerProtocol = serializers.ChoiceField(help_text="Identifier of layer(s) and protocol(s)",
                                            choices=["IP_OVER_ETHERNET"], required=True)
    ipOverEthernet = IpOverEthernetAddressDataSerializer(help_text="Network address data for IP over Ethernet"
                                                                   "to assign to the extCP instance.",
                                                         required=False, allow_null=True)


class SapDataSerializer(serializers.Serializer):
    sapdId = serializers.CharField(help_text="Reference to the SAPD for this SAP.", required=True)
    sapName = serializers.CharField(help_text="Human readable name for the SAP.", required=True)
    description = serializers.CharField(help_text="Human readable description for the SAP.", required=True)
    sapProtocolData = CpProtocolDataSerializer(help_text="Parameters for configuring the network protocols"
                                                         " on the SAP.",
                                               required=False, allow_null=True, many=True)


class civicAddressElementSerializer(serializers.Serializer):
    caType = serializers.CharField(help_text="Describe the content type of caValue.", required=True)
    caValue = serializers.CharField(help_text="Content of civic address element corresponding to the"
                                              "aType.", required=True)


class LocationConstraintsSerializer(serializers.Serializer):
    countryCode = serializers.CharField(help_text="The two-letter ISO 3166 [29] country code in capital"
                                                  "letters.", required=True)
    civicAddressElement = civicAddressElementSerializer(help_text="Zero or more elements comprising the civic"
                                                                  "address.",
                                                        required=False, allow_null=True, many=True)


class VnfLocationConstraintSerializer(serializers.Serializer):
    vnfProfileId = serializers.CharField(help_text="ID of VNF profile", required=False, allow_null=True)
    locationConstraints = LocationConstraintsSerializer(help_text="Defines the location constraints for the"
                                                                  "VNF instance to be created based on the"
                                                                  "VNF profile.",
                                                        required=False, allow_null=True)


class ParamsForVnfSerializer(serializers.Serializer):
    vnfProfileId = serializers.CharField(help_text="Identifier of (reference to) a vnfProfile to which the"
                                                   "additional parameters apply", required=True)
    additionalParams = serializers.DictField(help_text="Content of civic address element corresponding to the"
                                                       "caType",
                                             child=serializers.CharField(help_text="KeyValue Pairs",
                                                                         allow_blank=True),
                                             required=False, allow_null=True)


class AffinityOrAntiAffinityRuleSerializer(serializers.Serializer):
    vnfdId = serializers.ListField(help_text="Reference to a VNFD.", required=False, allow_null=True)
    vnfProfileId = serializers.ListField(help_text="Reference to a vnfProfile defined in the NSD.",
                                         required=True)
    vnfInstanceId = serializers.ListField(help_text="Reference to the existing VNF instance as the subject of"
                                                    "the affinity or anti-affinity rule.",
                                          required=False, allow_null=True)
    affinityOrAntiAffiinty = serializers.ChoiceField(help_text="The type of the constraint.",
                                                     choices=["AFFINITY", "ANTI_AFFINITY"], required=True)
    scope = serializers.ChoiceField(help_text="Specifies the scope of the rule where the placement constraint"
                                              "applies.", choices=["NFVI_POP", "ZONE", "ZONE_GROUP",
                                                                   "NFVI_NODE"], required=True)


class InstantNsReqSerializer(serializers.Serializer):
    nsFlavourId = serializers.CharField(help_text="Identifier of the NS deployment flavour to be"
                                                  "instantiated.", required=True)
    sapData = SapDataSerializer(help_text="Create data concerning the SAPs of this NS",
                                required=False, allow_null=True, many=True)
    addpnfData = AddPnfDataSerializer(help_text="Information on the PNF(s) that are part of this NS.",
                                      required=False, allow_null=True, many=True)
    vnfInstanceData = VnfInstanceDataSerializer(help_text="Specify an existing VNF instance to be used in "
                                                          "the NS.",
                                                required=False, allow_null=True, many=True)
    nestedNsInstanceId = serializers.ListField(help_text="Specify an existing NS instance to be used as a "
                                                         "nested NS within the NS",
                                               required=False, allow_null=True)
    localizationLanguage = VnfLocationConstraintSerializer(help_text="Defines the location constraints for "
                                                                     "the VNF to be instantiated as part of"
                                                                     " the NS instantiation.",
                                                           required=False, allow_null=True, many=True)
    additionalParamForNs = serializers.DictField(
        help_text="Allows the OSS/BSS to provide additional parameters at the NS level ",
        child=serializers.CharField(help_text="KeyValue Pairs", allow_blank=True),
        required=False,
        allow_null=True
    )
    additionalParamsForVnf = ParamsForVnfSerializer(help_text="Allows the OSS/BSS to provide additional "
                                                              "parameter(s)per VNF instance",
                                                    required=False, allow_null=True, many=True)
    startTime = serializers.DateTimeField(help_text="Timestamp indicating the earliest time to instantiate"
                                                    "the NS.", required=False, allow_null=True)
    nsInstantiationLevelId = serializers.CharField(help_text="Identifies one of the NS instantiation levels"
                                                             "declared in the DF applicable to this NS "
                                                             "instance", required=False, allow_null=True)
    additionalAffinityOrAntiAffiniityRule = AffinityOrAntiAffinityRuleSerializer(
        help_text="Specifies additional affinity or anti-affinity constraint for the VNF instances to be"
                  " instantiated as part of the NS instantiation.",
        required=False, allow_null=True, many=True)


class InstNsPostDealReqSerializer(serializers.Serializer):
    status = serializers.CharField(help_text="Status of NS Inst", required=True)
