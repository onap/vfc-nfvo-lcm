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
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from lcm.ns.views.views import CreateNSView, NSInstView, TerminateNSView, NSDetailView, NSInstPostDealView, \
    NSManualScaleView, NSHealView, NSUpdateView

urlpatterns = [
    # API will be deprecated in the future release

    url(r'^api/nslcm/v1/ns$', CreateNSView.as_view()),
    url(r'^api/nslcm/v1/ns/(?P<ns_instance_id>[0-9a-zA-Z_-]+)/instantiate$', NSInstView.as_view()),
    url(r'^api/nslcm/v1/ns/(?P<ns_instance_id>[0-9a-zA-Z_-]+)/terminate$', TerminateNSView.as_view()),
    url(r'^api/nslcm/v1/ns/(?P<ns_instance_id>[0-9a-zA-Z_-]+)$', NSDetailView.as_view()),
    url(r'^api/nslcm/v1/ns/(?P<ns_instance_id>[0-9a-zA-Z_-]+)/postdeal$', NSInstPostDealView.as_view()),
    url(r'^api/nslcm/v1/ns/(?P<ns_instance_id>[0-9a-zA-Z_-]+)/scale$', NSManualScaleView.as_view()),
    url(r'^api/nslcm/v1/ns/(?P<ns_instance_id>[0-9a-zA-Z_-]+)/heal$', NSHealView.as_view()),

    # SOL005 URL API definition TODO

    url(r'^api/nslcm/v1/ns/(?P<ns_instance_id>[0-9a-zA-Z_-]+)/update$', NSUpdateView.as_view())

]

urlpatterns = format_suffix_patterns(urlpatterns)
