# encoding: utf-8
# Copyright 2011, Tangere Infotech Pvt Ltd [http://tangere.in]
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.conf.urls.defaults import *

urlpatterns = patterns ('cmh.issuemgr.views',
                        (r'^$', 'index'),
                        (r'^accept/$', 'accept'),
                        (r'^locations/$', 'locations'),
                        (r'^categories/$', 'categories'),
                        (r'^departments/$', 'departments'),
                        (r'^track/$', 'track'),
                        (r'^my_issues/', 'my_issues'),
                        (r'^get_category_map_update/(?P<category>.*)/$', 'get_category_map_update'),
                        (r'^update/(?P<complaintno>[\d\.]+)/(?P<complaintid>\d+)/$', 'update'),
                        (r'^track/(?P<complaintno>[\d\.]+)/(?P<complaintid>\d+)/$', 'track_issues'),
                        (r'^hot_complaints/', 'hot_complaints'),
                        )
