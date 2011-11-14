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

urlpatterns = patterns ('cmh.masters.views',
                        (r'^$', 'masters'),
                        (r'^dm/$', 'process_dm'),
                        (r'^officials/$', 'officials'),
                        (r'^add_official/$', 'add_official'),
                        (r'^department_selected/$', 'department_selected'),
                        (r'^csomembers/$', 'csomembers'),
                        (r'^add_cso_user/$', 'add_cso_user'),
                        (r'^state/$','state'),
                        (r'^district/$','district'),
                        (r'^block/$','block'),
                        (r'^gp/$','gp'),
                        (r'^village/$','village'),
                        (r'^department/$','department'),
                        (r'^complainttype/$','complainttype'),
                        (r'^add_block/$','addblock'),
                        (r'^add_comp_type/$','addcomp'),
                        (r'^add_gp/$','addgp'),
                        (r'^add_dep/$','adddep'),
                        (r'^add_village/$','addvillage'),
                        (r'^getgpinblocks/$', 'getgpinblocks'),
                        (r'^getvillingps','getvillingps'),
                        (r'^getclassindep/$', 'getclassindep'),
                        (r'^add_state/$','add_state'),
                        (r'^add_district/$','add_district'),
                        (r'^gplist/$', 'gplist'),
                        (r'^deplist/$', 'deplist'),
                        (r'^villist/$','villist'),
                        (r'^clist/$','clist'),
                        (r'^blist/$','blist'),
                        (r'^officialist/$','officialist'),
                        (r'^csolist/$','csolist'),
                        (r'^edit_vill/(?P<block>\d+)/(?P<gpcode>\d+)/(?P<villcode>\d+)/$','editvill'),
                        (r'^edit_gp/(?P<block>\d+)/(?P<gpcode>\d+)/$','editgp'),
                        (r'^edit_dep/(?P<depcode>[ \w-]+)/$','editdep'),
                        (r'^edit_blk/(?P<blkcode>\d+)/$','editblk'),
                        (r'^edit_c/(?P<compcode>[\w\s]+)/(?P<depcode>[ \w-]+)/$','editc'),
                        (r'^edit_off/(?P<offid>\d+)/$','edit_off'),
                        (r'^edit_cso/(?P<csoid>\d+)/$','edit_cso')
                        )
