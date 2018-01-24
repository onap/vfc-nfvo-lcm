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


class ContextSerializer(serializers.Serializer):
    globalCustomerId = serializers.CharField(help_text="Global customer ID", required=False, allow_null=True)
    serviceType = serializers.CharField(help_text="Service type", required=False, allow_null=True)


class CreateNsReqSerializer(serializers.Serializer):
    csarId = serializers.CharField(help_text="Package ID of NS", required=True)
    nsName = serializers.CharField(help_text="Name of NS", required=False, allow_null=True)
    description = serializers.CharField(help_text="Description of NS", required=False, allow_null=True)
    context = ContextSerializer(help_text="Context of NS", required=False)


class CreateNsRespSerializer(serializers.Serializer):
    nsInstanceId = serializers.CharField(help_text="ID of NS instance", required=True)
