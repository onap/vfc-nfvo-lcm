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
from lcm.ns.const import CHANGE_TYPES, CHANGE_RESULT


CHANGE_TYPE = [
    CHANGE_TYPES.ADD,
    CHANGE_TYPES.REMOVE,
    CHANGE_TYPES.MODIFY
]


class AffectedPnfsSerializer(serializers.Serializer):
    pnfId = serializers.UUIDField(
        help_text="Identifier of the affected PNF. This identifier is allocated by the OSS/BSS. ",
        required=True
    )
    pnfdId = serializers.UUIDField(
        help_text="Identifier of the PNFD on which the PNF is based.",
        required=True
    )
    pnfProfileId = serializers.UUIDField(
        help_text="Identifier of the VNF profile of the NSD.",
        required=True
    )
    pnfName = serializers.CharField(
        help_text="Name of the PNF.",
        required=True)
    cpInstanceId = serializers.UUIDField(
        help_text="Identifier of the NS profile of the NSD.",
        required=True
    )
    changeType = serializers.ChoiceField(
        help_text="Signals the type of change",
        required=True,
        choices=CHANGE_TYPE
    )
    changeResult = serializers.ChoiceField(
        help_text="Signals the result of change identified by the 'changeType' attribute.",
        required=True,
        choices=CHANGE_RESULT
    )
