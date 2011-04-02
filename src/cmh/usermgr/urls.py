from django.conf.urls.defaults import *

urlpatterns = patterns ('cmh.PeopleMgr.views',
                        (r'^login/$',             'dologin'),
                        (r'^logout/$',            'dologout'),
                        (r'^register/$',           'doregister'),
                        #(r'^forgot/$',            'forgot'),
                        #(r'^process_forgot/$',    'process_forgot'),

                        )
