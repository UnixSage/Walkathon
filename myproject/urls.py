from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

#from myproject.walk.views import currentDatetime

urlpatterns = patterns('',
    # Example:
    # (r'^myproject/', include('myproject.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^new/', 'myproject.walk.views.createwalker'),
    (r'^walker/(?P<uuid>.*)/', 'myproject.walk.views.walker'),
)
