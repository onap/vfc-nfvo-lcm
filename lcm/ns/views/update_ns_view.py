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

import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

from lcm.ns.biz.ns_update import NSUpdateService
from lcm.ns.serializers.ns_serializers import NsOperateJobSerializer
from lcm.ns.serializers.update_serializers import UpdateNsReqSerializer
from lcm.pub.exceptions import NSLCMException
from lcm.pub.utils.jobutil import JobUtil, JOB_TYPE

logger = logging.getLogger(__name__)


class NSUpdateView(APIView):
    @swagger_auto_schema(
        request_body=UpdateNsReqSerializer(),
        responses={
            status.HTTP_202_ACCEPTED: NsOperateJobSerializer(),
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Inner error"
        }
    )
    def post(self, request, ns_instance_id):
        try:
            logger.debug("Enter UpdateNSView::post %s, %s", request.data, ns_instance_id)
            req_serializer = UpdateNsReqSerializer(data=request.data)
            if not req_serializer.is_valid():
                raise NSLCMException(req_serializer.errors)

            job_id = JobUtil.create_job("NS", JOB_TYPE.UPDATE_NS, ns_instance_id)
            NSUpdateService(ns_instance_id, request.data, job_id).start()

            resp_serializer = NsOperateJobSerializer(data={'jobId': job_id})
            if not resp_serializer.is_valid():
                raise NSLCMException(resp_serializer.errors)

            logger.debug("Leave UpdateNSView::post ret=%s", resp_serializer.data)
            return Response(data=resp_serializer.data, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            logger.error("Exception in UpdateNSView: %s", e.message)
            return Response(data={'error': e.message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
