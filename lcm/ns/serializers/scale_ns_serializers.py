# Copyright (c) 2019, CMCC Technologies Co., Ltd.

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
from lcm.ns.serializers.update_serializers import VnfInstanceDataSerializer
from lcm.ns.serializers.create_ns_serializers import NsScaleInfoSerializer
from lcm.ns.serializers.inst_ns_serializers import VnfLocationConstraintSerializer, ParamsForVnfSerializer


# class VnfInstanceDataSerializer(serializers.Serializer):
#     vnfInstanceId = serializers.CharField(help_text="Identifier of the existing VNF instance to be used in"
#                                                     "the NS. ", required=True)
#     vnfProfileId = serializers.CharField(help_text="Identifier of (Reference to) a vnfProfile defined in the "
#                                                    "NSD which the existing VNF instance shall be matched "
#                                                    "with. If not present", required=False, allow_null=True)


class ScaleNsByStepsDataSerializer(serializers.Serializer):
    scalingDirection = serializers.ChoiceField(help_text="The scaling direction",
                                               choices=["SCALE_IN", "SCALE_OUT"], required=True)
    aspectId = serializers.CharField(help_text="The aspect of the NS that is requested to be scaled, as "
                                               "declared in the NSD. ", required=True)
    numberOfSteps = serializers.CharField(help_text="The number of scaling steps to be performed. Defaults "
                                                    "to 1. ", required=False, allow_null=True)


# class NsScaleInfoSerializer(serializers.Serializer):
#     nsScalingAspectId = serializers.CharField(help_text="Identifier of the NS scaling aspect.", required=True)
#     nsScaleLevelId = serializers.CharField(help_text="Identifier of the NS scale level.", required=True)


class ScaleNsToLevelDataSerializer(serializers.Serializer):
    nsInstantiationLevel = serializers.CharField(help_text="Identifier of the target NS instantiation level "
                                                           "of the current DF to which the NS instance is "
                                                           "requested to be scaled.",
                                                 required=False, allow_null=True)
    nsScaleInfo = serializers.ListField(help_text="For each NS scaling aspect of the current DF",
                                        child=NsScaleInfoSerializer(
                                            help_text="This type represents the target NS Scale level for "
                                                      "each NS scaling aspect of the current deployment "
                                                      "flavour.", required=True),
                                        required=False, allow_null=True)


# class ParamsForVnfSerializer(serializers.Serializer):
#     vnfProfileId = serializers.CharField(help_text="Identifier of (reference to) a vnfProfile to which the "
#                                                    "additional parameters apply.", required=True)
#     additionalParams = serializers.DictField(help_text="Additional parameters that are applied for the VNF "
#                                                        "instance to be created.",
#                                              child=serializers.CharField(help_text="KeyValue Pairs",
#                                                                          allow_blank=True),
#                                              required=False, allow_null=True)


# class LocationConstraintsSerializer(serializers.Serializer):
#     countryCode = serializers.CharField(help_text="The two-letter ISO 3166 [29] country code in capital "
#                                                   "letters", required=True)
#     civicAddressElement = serializers.ListField(help_text="Zero or more elements comprising the civic "
#                                                           "address.", required=False, allow_null=True)


# class VnfLocationConstraintSerializer(serializers.Serializer):
#     vnfProfileId = serializers.CharField(help_text="Identifier (reference to) of a VnfProfile in the NSD used "
#                                                    "to manage the lifecycle of the VNF instance.",
#                                          required=True)
#
#     locationConstraints = LocationConstraintsSerializer(help_text="This type represents location constraints "
#                                                                   "for a VNF to be instantiated. The location"
#                                                                   " constraints shall be presented as a "
#                                                                   "country code", required=True)


class ScaleNsDataSerializer(serializers.Serializer):
    vnfInstanceToBeAdded = serializers.ListField(help_text="An existing VNF instance to be added to the NS "
                                                           "instance as part of the scaling operation. ",
                                                 child=VnfInstanceDataSerializer(
                                                     help_text="This type specifies an existing VNF instance "
                                                               "to be used in the NS instance and if needed",
                                                     required=True), required=False, allow_null=True)
    vnfInstanceToBeRemoved = serializers.ListField(help_text="The VNF instance to be removed from the NS "
                                                             "instance as part of the scaling operation",
                                                   required=False, allow_null=True)
    scaleNsByStepsData = ScaleNsByStepsDataSerializer(help_text="The information used to scale an NS "
                                                                "instance by one or more scaling steps",
                                                      required=False, allow_null=True)
    scaleNsToLevelData = ScaleNsToLevelDataSerializer(help_text="The information used to scale an NS instance"
                                                                " to a target size. ",
                                                      required=False, allow_null=True)
    additionalParamsForNs = serializers.DictField(help_text="Allows the OSS/BSS to provide additional "
                                                            "parameter(s) at the NS level necessary for the "
                                                            "NS scaling ",
                                                  child=serializers.CharField(help_text="KeyValue Pairs",
                                                                              allow_blank=True),
                                                  required=False, allow_null=True)
    additionalParamsForVnf = serializers.ListField(help_text="Allows the OSS/BSS to provide additional "
                                                             "parameter(s) per VNF instance",
                                                   child=ParamsForVnfSerializer(
                                                       help_text="This type defines the additional parameters"
                                                                 " for the VNF instance to be created "
                                                                 "associated with an NS instance.",
                                                       required=True), required=False, allow_null=True)
    locationConstraints = serializers.ListField(help_text="The location constraints for the VNF to be "
                                                          "instantiated as part of the NS scaling.",
                                                child=VnfLocationConstraintSerializer(
                                                    help_text="This type represents the association of "
                                                              "location constraints to a VNF instance to"
                                                              "be created according to a specific VNF "
                                                              "profile", required=True),
                                                required=False, allow_null=True)


class VnfScaleInfoSerializer(serializers.Serializer):
    aspectlId = serializers.Serializer(help_text="The scaling aspect", required=True)
    scaleLevel = serializers.Serializer(help_text="The scale level for that aspect", required=True)


class ScaleToLevelDataSerializer(serializers.Serializer):
    vnfInstantiationLevelId = serializers.CharField(help_text="Identifier of the target instantiation level "
                                                              "of the current deployment flavour to which "
                                                              "the VNF is requested to be scaled.",
                                                    required=False, allow_null=True)
    vnfScaleInfo = serializers.ListField(help_text="For each scaling aspect of the current deployment "
                                                   "flavour",
                                         child=VnfScaleInfoSerializer(help_text="This type describes the "
                                                                                "provides information about"
                                                                                " the scale level of a VNF"
                                                                                " instance with respect to "
                                                                                "one scaling aspect",
                                                                      required=True),
                                         required=False, allow_null=True)

    additionalParams = serializers.DictField(help_text="Additional parameters passed by the NFVO as input to "
                                                       "the scaling process", required=False, allow_null=True)


class ScaleByStepDataSerializer(serializers.Serializer):
    aspectId = serializers.CharField(help_text="Identifier of (reference to) the aspect of the VNF that is "
                                               "requested to be scaled", required=True)
    numberOfSteps = serializers.CharField(help_text="Number of scaling steps.",
                                          required=False, allow_null=True)
    additionalParams = serializers.DictField(help_text="Additional parameters passed by the NFVO as input to"
                                                       "he scaling process", required=False, allow_null=True)


class ScaleVnfDataSerializer(serializers.Serializer):
    vnfInstanceid = serializers.CharField(help_text="Identifier of the VNF instance being scaled.",
                                          required=True)

    scaleVnfType = serializers.ChoiceField(help_text="Type of the scale VNF operation requested.",
                                           choices=["SCALE_OUT", "SCALE_IN", "SCALE_TO_INSTANTIATION_LEVEL",
                                                    "SCALE_TO_SCALE_LEVEL(S)"], required=True)

    scaleToLevelData = ScaleToLevelDataSerializer(help_text="The information used for scaling to a "
                                                            "given level.", required=False)

    scaleByStepData = ScaleByStepDataSerializer(help_text="The information used for scaling by steps",
                                                required=False)


class ScaleNsRequestSerializer(serializers.Serializer):
    scaleType = serializers.ChoiceField(help_text="Indicates the type of scaling to be performed",
                                        choices=["SCALE_NS ", "SCALE_VNF"], required=True)
    scaleNsData = ScaleNsDataSerializer(help_text="The necessary information to scale the referenced NS "
                                                  "instance. ", required=False, allow_null=True)
    scaleVnfData = serializers.ListField(help_text="Timestamp indicating the scale time of the NS",
                                         child=ScaleVnfDataSerializer(help_text="This type represents defines"
                                                                                "the information to scale a "
                                                                                "VNF instance to a given "
                                                                                "level", required=True),
                                         required=False, allow_null=True)
    scaleTime = serializers.CharField(help_text="Timestamp indicating the scale time of the NS",
                                      required=False, allow_null=True)


class ManualScaleNsReqSerializer(serializers.Serializer):
    scaleType = serializers.CharField(help_text="Type of NS Scale", required=True)
    scaleNsData = ScaleNsDataSerializer(help_text="Scale NS data", many=True)
