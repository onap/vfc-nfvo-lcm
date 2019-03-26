# Copyright 2019 ZTE Corporation.
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

import logging
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from lcm.ns.biz.ns_terminate import TerminateNsService
from lcm.pub.utils.jobutil import JobUtil
from lcm.pub.utils.jobutil import JOB_TYPE
from lcm.pub.utils.values import ignore_case_get
from lcm.ns.serializers.sol.terminate_ns_serializers import TerminateNsReqSerializer
from lcm.pub.exceptions import BadRequestException
from lcm.ns.const import NS_OCC_BASE_URI
from lcm.ns.serializers.sol.pub_serializers import ProblemDetailsSerializer

logger = logging.getLogger(__name__)


class TerminateNsView(APIView):

    @swagger_auto_schema(
        request_body=TerminateNsReqSerializer(),
        responses={
            status.HTTP_202_ACCEPTED: None,
            status.HTTP_500_INTERNAL_SERVER_ERROR: ProblemDetailsSerializer()
        }
    )
    def post(self, request, ns_instance_id):
        job_id = JobUtil.create_job("NS", JOB_TYPE.TERMINATE_NS, ns_instance_id)
        try:
            logger.debug("Enter TerminateNSView::post %s", request.data)
            req_serializer = TerminateNsReqSerializer(data=request.data)
            if not req_serializer.is_valid():
                logger.debug("request.data is not valid,error: %s" % req_serializer.errors)
                raise BadRequestException(req_serializer.errors)
            terminationTime = ignore_case_get(request.data, 'terminationTime')
            logger.debug("terminationTime is %s" % terminationTime)
            # todo terminationTime
            terminateNsService = TerminateNsService(ns_instance_id, job_id, request.data)
            terminateNsService.start()
            logger.debug("Location: %s" % terminateNsService.occ_id)
            response = Response(data={}, status=status.HTTP_202_ACCEPTED)
            response["Location"] = NS_OCC_BASE_URI % terminateNsService.occ_id
            logger.debug("Leave TerminateNSView")
            return response
        except BadRequestException as e:
            logger.error("Exception in TerminateNsView: %s", e.message)
            JobUtil.add_job_status(job_id, 255, 'NS termination failed: %s' % e.message)
            data = {'status': status.HTTP_400_BAD_REQUEST, 'detail': e.message}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error("Exception in TerminateNsView: %s", e.message)
            JobUtil.add_job_status(job_id, 255, 'NS termination failed: %s' % e.message)
            data = {'status': status.HTTP_400_BAD_REQUEST, 'detail': e.message}
            return Response(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
