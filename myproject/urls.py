from django.conf import settings
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
    url(r'^new/$', 'myproject.walk.views.create_walker', name='create_walker'),
    url(r'^walker/(?P<uuid>[a-z0-9\-]*)/$', 'myproject.walk.views.walker_private', name='walker_private'),
    url(r'^walker/(?P<uuid>[a-z0-9\-]*)/add-sponsor/$', 'myproject.walk.views.walker_add_sponsor', name='walker_add_sponsor'),
    url(r'^walker/(?P<uuid>[a-z0-9\-]*)/edit-sponsor/(?P<id>\d+)/$', 'myproject.walk.views.walker_edit_sponsor', name='walker_edit_sponsor'),
    url(r'^walker/(?P<uuid>[a-z0-9\-]*)/delete-sponsor/$', 'myproject.walk.views.walker_delete_sponsor', name='walker_delete_sponsor'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
