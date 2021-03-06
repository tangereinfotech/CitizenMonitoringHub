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
                        (r'^metrics/$', 'metrics'),
                        (r'^all_issues/$', 'all_issues'),
                        (r'^all_issues/(?P<mode>all|rem)/$', 'all_mode_issues'),
                        (r'^all_issues_list/$', 'all_issues_list'),
                        (r'^accept/$', 'accept'),
                        (r'^locations/$', 'locations'),
                        (r'^categories/$', 'categories'),
                        (r'^track/$', 'track'),
                        (r'^my_issues/$', 'my_issues'),
                        (r'^my_issues/(?P<mode>all|rem)/$', 'my_mode_issues'),
                        (r'^my_issues_list/$', 'my_issues_list'),
                        (r'^get_category_map_update/$', 'get_category_map_update'),
                        (r'^update/(?P<complaintno>[\d\.]+)/$', 'update'),
                        (r'^track/(?P<complaintno>[\d\.]+)/$', 'track_issues'),
                        (r'^hot_complaints/', 'hot_complaints'),
                        (r'^report/$','report'),
                        (r'^getstats/$', 'getstats'),
                        (r'^storedata/(?P<repdataid>\d+)/(?P<identifier>\w+)/(?P<codea>\d+)/(?P<codeb>\d+)/(?P<codec>\d+)/$','storedata'),
                        (r'^removedata/(?P<repdataid>\d+)/(?P<identifier>\w+)/(?P<codea>\d+)/(?P<codeb>\d+)/(?P<codec>\d+)/$','removedata'),
                        (r'^data/(?P<repdataid>\d+)/(?P<cat>\w+)/(?P<idval>\d+)/$','data'),
                        (r'^initial_report/$', 'initial_report'),
                        (r'^edit_report/$', 'edit_report'),
                        (r'^evidences/(?P<filename>.*)$', 'get_evidence'),
                        (r'^set_reminder/(?P<complaintno>[\d\.]+)/$', 'set_reminder'),
                        (r'^del_reminder/(?P<complaintno>[\d\.]+)/$', 'del_reminder'),
                        (r'^file_sms/$', 'file_sms'),
                        (r'^file_phone/$', 'file_phone'),
                        )
