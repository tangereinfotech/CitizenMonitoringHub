from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
import cmh
admin.autodiscover()

urlpatterns = patterns('',
                       (r'^user/', include ('cmh.PeopleMgr.urls')),
                       (r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       (r'^admin/', include(admin.site.urls)),
                       (r'^complaint/', include ('cmh.ComplaintMgr.urls')),
                       url(r'^captcha/', include('cmh.captcha.urls')),

                       )

if settings.DEBUG:
    urlpatterns += patterns ('',
                             (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root' : settings.CMH_APP_DIR + '/static/'}),
                             )


urlpatterns += patterns ("", (r'^$', 'cmh.views.index'))

