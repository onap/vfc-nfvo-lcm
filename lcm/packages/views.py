# Copyright 2016-2017 ZTE Corporation.
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
import uuid

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from lcm.pub.utils.values import ignore_case_get
from lcm.pub.utils.syscomm import fun_name
from lcm.packages import ns_package, nf_package, sdc_ns_package, sdc_nf_package

logger = logging.getLogger(__name__)

@api_view(http_method_names=['POST', 'GET'])
def ns_distribute_get(request, *args, **kwargs):
    logger.debug("Enter %s, method is %s", fun_name(), request.method)
    ret, normal_status = None, None
    if request.method == 'GET':
        ret = sdc_ns_package.SdcNsPackage().get_csars()
        normal_status = status.HTTP_200_OK
    else:
        csar_id = ignore_case_get(request.data, "csarId")
        logger.debug("csar_id is %s", csar_id)
        ret = sdc_ns_package.ns_on_distribute(csar_id)      
        normal_status = status.HTTP_202_ACCEPTED
    logger.debug("Leave %s, Return value is %s", fun_name(), ret)
    if ret[0] != 0:
        return Response(data={'error': ret[1]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(data=ret[1], status=normal_status)

@api_view(http_method_names=['GET', 'DELETE'])
def ns_rd_csar(request, *args, **kwargs):
    csar_id = ignore_case_get(kwargs, "csarId")
    logger.info("Enter %s, method is %s, csar_id is %s", fun_name(), request.method, csar_id)
    ret, normal_status = None, None
    if request.method == 'GET':
        ret = sdc_ns_package.ns_get_csar(csar_id)
        normal_status = status.HTTP_200_OK
    else:
        force_delete = csar_id.endswith("force")
        if force_delete:
            csar_id = csar_id[:-5]
        ret = sdc_ns_package.ns_delete_csar(csar_id, force_delete)
        normal_status = status.HTTP_202_ACCEPTED
    logger.info("Leave %s, Return value is %s", fun_name(), str(ret))
    if ret[0] != 0:
        return Response(data={'error': ret[1]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(data=ret[1], status=normal_status)

####################################################################################################    

@api_view(http_method_names=['POST', 'GET'])
def nf_distribute_get(request, *args, **kwargs):
    logger.debug("Enter %s%s, method is %s", fun_name(), request.data, request.method)
    ret, normal_status = None, None
    if request.method == 'GET':
        ret = sdc_nf_package.nf_get_csars()
        normal_status = status.HTTP_200_OK
    else:
        csar_id = ignore_case_get(request.data, "csarId")
        vim_ids = ignore_case_get(request.data, "vimIds")
        lab_vim_id = ignore_case_get(request.data, "labVimId")
        job_id = str(uuid.uuid4())
        sdc_nf_package.SdcNfDistributeThread(csar_id, vim_ids, lab_vim_id, job_id).start()
        ret = [0, {"jobId": job_id}]
        normal_status = status.HTTP_202_ACCEPTED
    logger.debug("Leave %s, Return value is %s", fun_name(), ret)
    if ret[0] != 0:
        return Response(data={'error': ret[1]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(data=ret[1], status=normal_status)

@api_view(http_method_names=['GET', 'DELETE'])
def nf_rd_csar(request, *args, **kwargs):
    csar_id = ignore_case_get(kwargs, "csarId")
    logger.info("Enter %s, method is %s, csar_id is %s", fun_name(), request.method, csar_id)
    ret, normal_status = None, None
    if request.method == 'GET':
        ret = sdc_nf_package.nf_get_csar(csar_id)
        normal_status = status.HTTP_200_OK
    else:
        force_delete = csar_id.endswith("force")
        if force_delete:
            csar_id = csar_id[:-5]
        ret = sdc_nf_package.nf_delete_csar(csar_id, force_delete)
        normal_status = status.HTTP_202_ACCEPTED
    logger.info("Leave %s, Return value is %s", fun_name(), str(ret))
    if ret[0] != 0:
        return Response(data={'error': ret[1]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(data=ret[1], status=normal_status)

####################################################################################################    

@api_view(http_method_names=['POST'])
def ns_on_boarding(request, *args, **kwargs):
    csar_id = ignore_case_get(request.data, "csarId")
    logger.info("Enter %s, method is %s, csar_id is %s", fun_name(), request.method, csar_id)
    ret = ns_package.ns_on_boarding(csar_id)
    logger.info("Leave %s, Return value is %s", fun_name(), str(ret))
    if ret[0] != 0:
        return Response(data={'error': ret[1]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(data=ret[1], status=status.HTTP_202_ACCEPTED)


@api_view(http_method_names=['GET', 'DELETE'])
def ns_access_csar(request, *args, **kwargs):
    csar_id = ignore_case_get(kwargs, "csarId")
    logger.info("Enter %s, method is %s, csar_id is %s", fun_name(), request.method, csar_id)
    ret, normal_status = None, None
    if request.method == 'GET':
        ret = ns_package.ns_get_csar(csar_id)
        normal_status = status.HTTP_200_OK
    else:
        ret = ns_package.ns_delete_csar(csar_id)
        normal_status = status.HTTP_202_ACCEPTED
    logger.info("Leave %s, Return value is %s", fun_name(), str(ret))
    if ret[0] != 0:
        return Response(data={'error': ret[1]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(data=ret[1], status=normal_status)


@api_view(http_method_names=['DELETE'])
def ns_delete_pending_csar(request, *args, **kwargs):
    csar_id = ignore_case_get(kwargs, "csarId")
    logger.info("Enter %s, method is %s, csar_id is %s", fun_name(), request.method, csar_id)
    ret = ns_package.ns_delete_pending_csar(csar_id)
    logger.info("Leave %s, Return value is %s", fun_name(), str(ret))
    if ret[0] != 0:
        return Response(data={'error': ret[1]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(data=ret[1], status=status.HTTP_202_ACCEPTED)


@api_view(http_method_names=['PUT'])
def ns_set_state_csar(request, *args, **kwargs):
    csar_id = ignore_case_get(kwargs, "csarId")
    operation = ignore_case_get(kwargs, "operation")
    logger.info("Enter %s, method is %s, csar_id is %s, operation is %s", fun_name(), request.method, csar_id, operation)
    ret = ns_package.ns_set_state_csar(csar_id, operation)
    logger.info("Leave %s, Return value is %s", fun_name(), str(ret))
    if ret[0] != 0:
        return Response(data={'error': ret[1]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(data=ret[1], status=status.HTTP_202_ACCEPTED)

#################################################################################################################
@api_view(http_method_names=['POST', 'GET'])
def nf_on_boarding(request, *args, **kwargs):
    logger.info("Enter %s%s, method is %s", fun_name(), request.data, request.method)
    if request.method == 'GET':
        ret = nf_package.NfPackage().get_csars()
        logger.debug("csars=%s", str(ret))
        return Response(data=ret, status=status.HTTP_200_OK)
    csar_id = ignore_case_get(request.data, "csarId")
    vim_ids = ignore_case_get(request.data, "vimIds")
    lab_vim_id = ignore_case_get(request.data, "labVimId")
    job_id = str(uuid.uuid4())
    nf_package.NfOnBoardingThread(csar_id, vim_ids, lab_vim_id, job_id).start()
    ret = {"jobId": job_id}
    logger.info("Leave %s, Return value is %s", fun_name(), str(ret))
    return Response(data=ret, status=status.HTTP_202_ACCEPTED)


@api_view(http_method_names=['GET', 'DELETE'])
def nf_access_csar(request, *args, **kwargs):
    logger.info("Enter %s%s, method is %s", fun_name(), args, request.method)
    csar_id = ignore_case_get(kwargs, "csarId")
    if request.method == 'GET':
        ret = nf_package.NfPackage().get_csar(csar_id)
        logger.info("Leave %s, Return value is %s", fun_name(), str(ret))
        if ret[0] != 0:
            return Response(data={'error': ret[1]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data=ret[1], status=status.HTTP_200_OK)
    # NF package deleting
    job_id = str(uuid.uuid4())
    nf_package.NfPkgDeleteThread(csar_id, job_id).start()
    ret = {"jobId": job_id}
    logger.info("Leave %s, Return value is %s", fun_name(), str(ret))
    return Response(data=ret, status=status.HTTP_202_ACCEPTED)


@api_view(http_method_names=['DELETE'])
def nf_delete_pending_csar(request, *args, **kwargs):
    logger.info("Enter %s%s, method is %s", fun_name(), args, request.method)
    csar_id = ignore_case_get(kwargs, "csarId")
    job_id = str(uuid.uuid4())
    nf_package.NfPkgDeletePendingThread(csar_id, job_id).start()
    ret = {"jobId": job_id}
    logger.info("Leave %s, Return value is %s", fun_name(), str(ret))
    return Response(data=ret, status=status.HTTP_202_ACCEPTED)