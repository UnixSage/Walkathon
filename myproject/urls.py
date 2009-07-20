from django.conf import settings
from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

from myproject.walk.views import MyEndPoint

urlpatterns = patterns('',
    # Example:
    # (r'^myproject/', include('myproject.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    url(r'^new/$', 'myproject.walk.views.create_walker', name='create_walker'),
    url(r'^walker/(?P<uuid>[a-z0-9\-]*)/$', 'myproject.walk.views.walker_home', name='walker_home'),
    url(r'^walker/(?P<uuid>[a-z0-9\-]*)/edit/$', 'myproject.walk.views.walker_edit', name='walker_edit'),
    url(r'^walker/(?P<uuid>[a-z0-9\-]*)/sponsors/$', 'myproject.walk.views.walker_sponsors', name='walker_sponsors'),
    url(r'^walker/(?P<uuid>[a-z0-9\-]*)/add-sponsor/$', 'myproject.walk.views.walker_add_sponsor', name='walker_add_sponsor'),
    url(r'^walker/(?P<uuid>[a-z0-9\-]*)/edit-sponsor/(?P<id>\d+)/$', 'myproject.walk.views.walker_edit_sponsor', name='walker_edit_sponsor'),
    url(r'^walker/(?P<uuid>[a-z0-9\-]*)/delete-sponsor/$', 'myproject.walk.views.walker_delete_sponsor', name='walker_delete_sponsor'),
    (r'^paypal/872a9fcb-9a57-485c-853f-e581a3a0d277/$', MyEndPoint()),
    
    # I'm guessing this is temporary - likely to be replaced with a Flatpage or something
    (r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'home.html'}),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
