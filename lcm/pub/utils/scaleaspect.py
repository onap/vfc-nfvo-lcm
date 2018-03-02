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

import json
import logging
import os
import copy
from lcm.pub.database.models import NfInstModel
from lcm.ns.vnfs.const import VNF_STATUS
from lcm.pub.msapi import catalog


logger = logging.getLogger(__name__)
SCALE_TYPE = ("SCALE_NS", "SCALE_VNF")

scale_vnf_data_mapping = {
    "vnfInstanceId": "",
    "scaleByStepData": [
        {
            "type": "",
            "aspectId": "",
            "numberOfSteps": ""
        }
    ]
}


def ignorcase_get(args, key):
    if not key:
        return ""
    if not args:
        return ""
    if key in args:
        return args[key]
    for old_key in args:
        if old_key.upper() == key.upper():
            return args[old_key]
    return ""


def mapping_conv(keyword_map, rest_return):
    resp_data = {}
    for param in keyword_map:
        if keyword_map[param]:
            if isinstance(keyword_map[param], dict):
                resp_data[param] = mapping_conv(
                    keyword_map[param], ignorcase_get(
                        rest_return, param))
            else:
                resp_data[param] = ignorcase_get(rest_return, param)
    return resp_data


def get_vnf_scale_info(filename, ns_instanceId, aspect, step):
    json_data = get_json_data(filename)
    scale_options = ignorcase_get(json_data, "scale_options")
    for i in range(scale_options.__len__()):
        ns_scale_option = scale_options[i]
        if (ignorcase_get(ns_scale_option, "ns_instanceId") == ns_instanceId) \
                and (ignorcase_get(ns_scale_option, "ns_scale_aspect") == aspect):
            ns_scale_info_list = ignorcase_get(
                ns_scale_option, "ns_scale_info_list")
            for j in range(ns_scale_info_list.__len__()):
                ns_scale_info = ns_scale_info_list[j]
                if ns_scale_info["step"] == step:
                    return ns_scale_info["vnf_scale_list"]

    return None


# Get the vnf scaling info according to the ns package id.
def get_vnf_scale_info_package(scalingmap_json, nsd_id, aspect, step):
    scale_options = ignorcase_get(scalingmap_json, "scale_options")
    for i in range(scale_options.__len__()):
        ns_scale_option = scale_options[i]
        if (ignorcase_get(ns_scale_option, "nsd_id") == nsd_id) and (
                ignorcase_get(ns_scale_option, "ns_scale_aspect") == aspect):
            ns_scale_info_list = ignorcase_get(
                ns_scale_option, "ns_scale_info")
            for j in range(ns_scale_info_list.__len__()):
                ns_scale_info = ns_scale_info_list[j]
                if ns_scale_info["step"] == step:
                    vnf_scale_info_list = ns_scale_info["vnf_scale_list"]

                    return vnf_scale_info_list

    return None


# Gets the vnf instance id according to the vnfd_id and modify the list of
# scaling vnf info accrodingly.
def del_vnf_scale_info(vnf_scale_info_list):
    result = list()
    for i in range(vnf_scale_info_list.__len__()):
        vnf_scale_info = vnf_scale_info_list[i]
        vnfd_id = vnf_scale_info["vnfd_id"]
        vnf_instance_id_list = get_vnf_instance_id_list(vnfd_id)
        copy_vnf_scale_info = copy.deepcopy(vnf_scale_info)
        copy_vnf_scale_info.pop("vnfd_id")
        index = 0
        while index < vnf_instance_id_list.__len__():
            copy_vnf_scale_info["vnfInstanceId"] = vnf_instance_id_list[index]
            index += 1
            result.append(copy_vnf_scale_info)

    return result


def get_vnf_instance_id_list(vnfd_id):
    kwargs = {}
    kwargs['package_id'] = vnfd_id
    kwargs['status'] = VNF_STATUS.ACTIVE

    nf_model_list = NfInstModel.objects.filter(**kwargs)
    vnf_instance_id_list = list()
    for i in range(nf_model_list.__len__()):
        vnf_instance_id_list.append(nf_model_list[i]["nfinstid"])
    return vnf_instance_id_list


def get_json_data(filename):
    f = open(filename)
    json_str = f.read()
    data = json.JSONDecoder().decode(json_str)
    f.close()
    return data


def check_scale_list(vnf_scale_list, ns_instanceId, aspect, step):
    if vnf_scale_list is None:
        logger.debug(
            "The scaling option[ns=%s, aspect=%s, step=%s] does not exist. Pls check the config file." %
            (ns_instanceId, aspect, step))
        raise Exception(
            "The scaling option[ns=%s, aspect=%s, step=%s] does not exist. Pls check the config file." %
            (ns_instanceId, aspect, step))
    else:
        return vnf_scale_list


def set_scaleVnfData_type(vnf_scale_list, scale_type):
    logger.debug(
        "vnf_scale_list = %s, type = %s" %
        (vnf_scale_list, scale_type))
    scaleVnfDataList = []
    if vnf_scale_list is not None:
        for i in range(vnf_scale_list.__len__()):
            scaleVnfData = scale_vnf_data_mapping
            scaleVnfData["vnfInstanceId"] = get_vnfInstanceIdByName(
                vnf_scale_list[i]["vnfInstanceId"])
            scaleVnfData["scaleByStepData"][0]["type"] = scale_type
            scaleVnfData["scaleByStepData"][0]["aspectId"] = vnf_scale_list[i]["vnf_scaleAspectId"]
            scaleVnfData["scaleByStepData"][0]["numberOfSteps"] = vnf_scale_list[i]["numberOfSteps"]
            scaleVnfDataList.append(scaleVnfData)
    logger.debug("scaleVnfDataList = %s" % scaleVnfDataList)
    return scaleVnfDataList


def get_vnfInstanceIdByName(name):
    return name


def get_vnf_data(filename, ns_instanceId, aspect, step, scale_type):

    vnf_scale_list = get_vnf_scale_info(filename, ns_instanceId, aspect, step)
    check_scale_list(vnf_scale_list, ns_instanceId, aspect, step)
    scaleVnfDataList = set_scaleVnfData_type(vnf_scale_list, scale_type)
    logger.debug("scaleVnfDataList = %s" % scaleVnfDataList)
    return scaleVnfDataList

    # return Response(data={'error': e.message},status=status.HTTP_204_NO_CONTENT)
    # return Response(data={'success': 'success'},status=status.HTTP_200_OK)


# Get scaling data of vnf according to the package
def get_vnf_data_package(
        scalingmap_json,
        ns_instanceId,
        aspect,
        step,
        scale_type):
    nsd_id = get_nsdId(ns_instanceId)
    vnf_scale_list = get_vnf_scale_info_package(
        scalingmap_json, nsd_id, aspect, step)
    check_scale_list(vnf_scale_list, ns_instanceId, aspect, step)
    scaleVnfDataList = set_scaleVnfData_type(vnf_scale_list, scale_type)
    logger.debug("scaleVnfDataList = %s" % scaleVnfDataList)

    return scaleVnfDataList


# Get the nsd id according to the ns instance id.
def get_nsdId(ns_instanceId):
    return None


def get_and_check_params(scaleNsData, ns_InstanceId):

    if scaleNsData is None:
        pass
        # raise NSLCMException("Error! scaleNsData in the request is Empty!")

    scaleNsByStepsData = scaleNsData[0]["scaleNsByStepsData"]
    if scaleNsByStepsData is None:
        pass
        # raise NSLCMException("Error! scaleNsByStepsData in the request is Empty!")

    aspect = scaleNsByStepsData[0]["aspectId"]
    numberOfSteps = scaleNsByStepsData[0]["numberOfSteps"]
    scale_type = scaleNsByStepsData[0]["scalingDirection"]

    return ns_InstanceId, aspect, numberOfSteps, scale_type


def get_scale_vnf_data(scaleNsData, ns_InstanceId):
    curdir_path = os.path.dirname(
        os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__))))
    filename = curdir_path + "/ns/data/scalemapping.json"
    logger.debug("filename = %s" % filename)
    ns_InstanceId, aspect, numberOfSteps, scale_type = get_and_check_params(
        scaleNsData, ns_InstanceId)
    return get_vnf_data(
        filename,
        ns_InstanceId,
        aspect,
        numberOfSteps,
        scale_type)


# Get scaling vnf data according to package by the scaling map json file.
def get_scale_vnf_data_package(scaleNsData, ns_InstanceId):

    scalingmap_json = catalog.get_scalingmap_json_package(ns_InstanceId)
    logger.debug("scalingmap_json = %s" % scalingmap_json)
    ns_InstanceId, aspect, numberOfSteps, scale_type = get_and_check_params(
        scaleNsData, ns_InstanceId)
    return get_vnf_data_package(
        scalingmap_json,
        ns_InstanceId,
        aspect,
        numberOfSteps,
        scale_type)
