from django.conf.urls import patterns, include, url
#from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'cmh.reports.views.home', name='home'),
    url(r'^all_issues_report/$', 'cmh.reports.views.home', name='home'),
    url(r'^my_issues_report/$', 'cmh.reports.views.my_issues', name='home'),
    url(r'^my_issues_data/$', 'cmh.reports.views.my_issues_data', name='home'),
    url(r'^all_issues_data/$', 'cmh.reports.views.all_issues_data', name='home'),
    url(r'^sms_logs_report/$', 'cmh.reports.views.sms_logs_report', name='home'),
    url(r'^sms_logs_data/$', 'cmh.reports.views.sms_logs_data', name='home'),
    # url(r'^datatables/', include('datatables.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

#urlpatterns += staticfiles_urlpatterns()
