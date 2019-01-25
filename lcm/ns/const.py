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
from lcm.pub.utils.enumutil import enum

OWNER_TYPE = enum(VNF=0, VNFM=1, NS=2)

NS_INST_STATUS = enum(EMPTY='empty', INSTANTIATING='instantiating', TERMINATING='terminating',
                      ACTIVE='active', FAILED='failed', INACTIVE='inactive', UPDATING='updating', SCALING='scaling',
                      HEALING='healing')

SERVICE_TYPE = 'NetworkService'
SERVICE_ROLE = 'NetworkService'

# new_add
HEAL_ACTION_TYPE = enum(START="vmCreate", RESTART="vmReset")
ACTION_TYPE = enum(START=1, STOP=2, REBOOT=3)
GRANT_TYPE = enum(INSTANTIATE="INSTANTIATE", TERMINATE="TERMINATE",
                  HEAL_CREATE="Heal Create", HEAL_RESTART="Heal Restart", OPERATE="OPERATE")
VNF_STATUS = enum(NULL='null', INSTANTIATING="instantiating", INACTIVE='inactive', ACTIVE="active",
                  FAILED="failed", TERMINATING="terminating", SCALING="scaling", OPERATING="operating",
                  UPDATING="updating", HEALING="healing")

OPERATION_TYPE = enum(
    INSTANTIATE="INSTANTIATE",
    SCALE="SCALE",
    TERMINATE="TERMINATE",
    UPDATE="UPDATE",
    HEAL="HEAL",
)


LCM_NOTIFICATION_STATUS = enum(START="START", RESULT="RESULT")

OPERATION_STATE_TYPE = enum(
    STARTING="STARTING",
    PROCESSING="PROCESSING",
    COMPLETED="COMPLETED",
    FAILED_TEMP="FAILED_TEMP",
    FAILED="FAILED",
    ROLLING_BACK="ROLLING_BACK",
    ROLLED_BACK="ROLLED_BACK"
)

COMPOMENT_TYPE = enum(
    VNF="VNF",
    PNF="PNF",
    NS="NS",
)

OPName_For_Change_Notification_Type = enum(
    VNF_INSTANTIATE="VNF_INSTANTIATE",
    VNF_SCALE="VNF_SCALE",
    VNF_SCALE_TO_LEVEL="VNF_SCALE_TO_LEVEL",
    VNF_CHANGE_FLAVOUR="VNF_CHANGE_FLAVOUR",
    VNF_TERMINATE="VNF_TERMINATE",
    VNF_HEAL="VNF_HEAL",
    VNF_OPERATE="VNF_OPERATE",
    VNF_CHANGE_EXT_CONN="VNF_CHANGE_EXT_CONN",
    VNF_MODIFY_INFO="VNF_MODIFY_INFO",
    NS_INSTANTIATE="NS_INSTANTIATE",
    NS_SCALE="NS_SCALE",
    NS_UPDATE="NS_UPDATE",
    NS_TERMINATE="NS_TERMINATE",
    NS_HEAL="NS_HEAL",
)


OpOcc_Status_For_ChangeNotification_Type = enum(
    START="START",
    COMPLETED="COMPLETED ",
    PARTIALLY_COMPLETED="PARTIALLY_COMPLETED",
    FAILED="FAILED",
    ROLLED_BACK="ROLLED_BACK",
)

AUTH_TYPES = ["BASIC", "OAUTH2_CLIENT_CREDENTIALS", "TLS_CERT"]

BASIC = "BASIC"

OAUTH2_CLIENT_CREDENTIALS = "OAUTH2_CLIENT_CREDENTIALS"

# CHANGE_TYPE = enum(
#     ADDED='ADDED',
#     REMOVED='REMOVED',
#     MODIFIED='MODIFIED',
#     TEMPORARY='TEMPORARY',
#     LINK_PORT_ADDED='LINK_PORT_ADDED',
#     LINK_PORT_REMOVED='LINK_PORT_REMOVED'
# )

# RESOURCE_MAP = {'Storage': 'volumn', 'Network': 'network', 'SubNetwork': 'subnet', 'Port': 'port',
#                 'Flavour': 'flavor', 'Vm': 'vm'}

ROOT_URI = "api/nslcm/v1/subscriptions/"


LCCNNOTIFICATION = "NsLcmOperationOccurrenceNotification"

NOTIFICATION_TYPES = [
    "NsLcmOperationOccurenceNotification",
    "NsIdentifierCreationNotification",
    "NsIdentifierDeletionNotification",
    "NsChangeNotification",
]

NS_LCM_OP_TYPES = [
    OPERATION_TYPE.INSTANTIATE,
    OPERATION_TYPE.SCALE,
    OPERATION_TYPE.TERMINATE,
    OPERATION_TYPE.HEAL,
    OPERATION_TYPE.UPDATE,
]

LCM_OPERATION_STATE_TYPES = [
    OPERATION_STATE_TYPE.STARTING,
    OPERATION_STATE_TYPE.PROCESSING,
    OPERATION_STATE_TYPE.COMPLETED,
    OPERATION_STATE_TYPE.FAILED_TEMP,
    OPERATION_STATE_TYPE.FAILED,
    OPERATION_STATE_TYPE.ROLLING_BACK,
    OPERATION_STATE_TYPE.ROLLED_BACK
]

NS_COMPOMENT_TYPE = [
    COMPOMENT_TYPE.VNF,
    COMPOMENT_TYPE.PNF,
    COMPOMENT_TYPE.NS,
]


LCM_OPName_For_Change_Notification_Type = [
    OPName_For_Change_Notification_Type.VNF_INSTANTIATE,
    OPName_For_Change_Notification_Type.VNF_SCALE,
    OPName_For_Change_Notification_Type.VNF_SCALE_TO_LEVEL,
    OPName_For_Change_Notification_Type.VNF_CHANGE_FLAVOUR,
    OPName_For_Change_Notification_Type.VNF_TERMINATE,
    OPName_For_Change_Notification_Type.VNF_HEAL,
    OPName_For_Change_Notification_Type.VNF_OPERATE,
    OPName_For_Change_Notification_Type.VNF_CHANGE_EXT_CONN,
    OPName_For_Change_Notification_Type.VNF_MODIFY_INFO,
    OPName_For_Change_Notification_Type.NS_INSTANTIATE,
    OPName_For_Change_Notification_Type.NS_SCALE,
    OPName_For_Change_Notification_Type.NS_UPDATE,
    OPName_For_Change_Notification_Type.NS_TERMINATE,
    OPName_For_Change_Notification_Type.NS_HEAL,
]

LCM_OpOcc_Status_For_ChangeNotification_Type = [
    OpOcc_Status_For_ChangeNotification_Type.START,
    OpOcc_Status_For_ChangeNotification_Type.COMPLETED,
    OpOcc_Status_For_ChangeNotification_Type.PARTIALLY_COMPLETED,
    OpOcc_Status_For_ChangeNotification_Type.FAILED,
    OpOcc_Status_For_ChangeNotification_Type.ROLLED_BACK,
]
