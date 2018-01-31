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


class CreateSfcReqSerializer(serializers.Serializer):
    fpindex = serializers.CharField(help_text="Index of FP", required=True)
    nsInstanceId = serializers.CharField(help_text="ID of NS instance", required=False, allow_null=True)
    context = serializers.CharField(help_text="Context of NS instance", required=False, allow_null=True)
    sdnControllerId = serializers.CharField(help_text="ID of SDN controller", required=False, allow_null=True)
