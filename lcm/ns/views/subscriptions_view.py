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

import ast
import json
import logging
import traceback

from drf_yasg.utils import swagger_auto_schema
from lcm.ns.biz.create_subscription import CreateSubscription
from lcm.ns.biz.query_subscription import QuerySubscription
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from lcm.ns.serializers.lccn_subscription_request import LccnSubscriptionRequestSerializer
from lcm.ns.serializers.lccn_subscription import LccnSubscriptionSerializer
from lcm.ns.serializers.lccn_subscriptions import LccnSubscriptionsSerializer
from lcm.ns.serializers.response import ProblemDetailsSerializer
from lcm.pub.exceptions import NSLCMException

logger = logging.getLogger(__name__)
VALID_FILTERS = ["operationTypes", "operationStates", "notificationTypes", "nsInstanceId",
                 "nsComponentTypes", "lcmOpNameImpactingNsComponent", "lcmOpOccStatusImpactingNsComponent"]


def get_problem_details_serializer(status_code, error_message):
    problem_details = {
        "status": status_code,
        "detail": error_message
    }
    problem_details_serializer = ProblemDetailsSerializer(data=problem_details)
    problem_details_serializer.is_valid()
    return problem_details_serializer


class SubscriptionsView(APIView):

    @swagger_auto_schema(
        request_body=LccnSubscriptionRequestSerializer(),
        responses={
            status.HTTP_201_CREATED: LccnSubscriptionSerializer(),
            status.HTTP_303_SEE_OTHER: ProblemDetailsSerializer(),
            status.HTTP_500_INTERNAL_SERVER_ERROR: ProblemDetailsSerializer()
        }
    )
    def post(self, request):
        logger.debug("SubscribeNotification--post::> %s" % request.data)
        try:
            lccn_subscription_request_serializer = LccnSubscriptionRequestSerializer(
                data=request.data)
            if not lccn_subscription_request_serializer.is_valid():
                raise NSLCMException(
                    lccn_subscription_request_serializer.errors)
            subscription = CreateSubscription(
                lccn_subscription_request_serializer.data).do_biz()
            lccn_notifications_filter = {
                "notificationTypes": ast.literal_eval(subscription.notification_types),
                "operationTypes": ast.literal_eval(subscription.operation_types),
                "operationStates": ast.literal_eval(subscription.operation_states),
                "nsInstanceSubscriptionFilter": json.loads(subscription.ns_instance_filter),
                "nsComponentTypes": ast.literal_eval(subscription.ns_component_types),
                "lcmOpNameImpactingNsComponent": ast.literal_eval(subscription.lcm_opname_impacting_nscomponent),
                "lcmOpOccStatusImpactingNsComponent": ast.literal_eval(subscription.lcm_opoccstatus_impacting_nscomponent)
            }
            subscription_data = {
                "id": subscription.subscription_id,
                "callbackUri": subscription.callback_uri,
                "_links": json.loads(subscription.links),
                "filter": lccn_notifications_filter
            }
            sub_resp_serializer = LccnSubscriptionSerializer(
                data=subscription_data)
            if not sub_resp_serializer.is_valid():
                raise NSLCMException(sub_resp_serializer.errors)
            return Response(data=sub_resp_serializer.data, status=status.HTTP_201_CREATED)
        except NSLCMException as e:
            logger.error(e.message)
            if "exists" in e.message:
                return Response(data={'error': '%s' % e.message}, status=status.HTTP_303_SEE_OTHER)
            return Response(data={'error': '%s' % e.message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            logger.error(e.message)
            logger.error(traceback.format_exc())
            return Response(data={'error': e.message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: LccnSubscriptionsSerializer(),
            status.HTTP_400_BAD_REQUEST: ProblemDetailsSerializer(),
            status.HTTP_500_INTERNAL_SERVER_ERROR: ProblemDetailsSerializer()
        }
    )
    def get(self, request):
        logger.debug("SubscribeNotification--get::> %s" % request.query_params)
        try:
            if request.query_params and not set(request.query_params).issubset(set(VALID_FILTERS)):
                problem_details_serializer = get_problem_details_serializer(
                    status.HTTP_400_BAD_REQUEST, "Not a valid filter")
                return Response(data=problem_details_serializer.data, status=status.HTTP_400_BAD_REQUEST)
            resp_data = QuerySubscription(request.query_params).query_multi_subscriptions()
            subscriptions_serializer = LccnSubscriptionsSerializer(data=resp_data)
            if not subscriptions_serializer.is_valid():
                raise NSLCMException(subscriptions_serializer.errors)
            logger.debug("SubscribeNotification--get::> Remove default fields if exclude_default is specified")
            return Response(data=subscriptions_serializer.data, status=status.HTTP_200_OK)
        except NSLCMException as e:
            logger.error(e.message)
            problem_details_serializer = get_problem_details_serializer(
                status.HTTP_500_INTERNAL_SERVER_ERROR, traceback.format_exc())
            return Response(data=problem_details_serializer.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            logger.error(e.message)
            logger.error(traceback.format_exc())
            problem_details_serializer = get_problem_details_serializer(
                status.HTTP_500_INTERNAL_SERVER_ERROR, traceback.format_exc())
            return Response(data=problem_details_serializer.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
