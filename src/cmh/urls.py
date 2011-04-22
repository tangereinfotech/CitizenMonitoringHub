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

import os

from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
import cmh
admin.autodiscover()

urlpatterns = patterns('',
                       (r'^user/', include ('cmh.usermgr.urls')),
                       (r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       (r'^admin/', include(admin.site.urls)),
                       (r'^complaint/', include ('cmh.issuemgr.urls')),
                       url(r'^captcha/', include('cmh.captcha.urls')),

                       )

if settings.DEBUG:
    urlpatterns += patterns ('',
                             (r'^static/(?P<path>.*)$',
                              'django.views.static.serve',
                              {'document_root' : os.path.join (settings.CMH_APP_DIR,
                                                               'cmh',
                                                               'static')}),
                             )

urlpatterns += patterns ("", (r'^$', 'cmh.views.index'))

