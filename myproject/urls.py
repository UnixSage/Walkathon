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
    url(r'^new/$', 'walk.views.create_walker', name='create_walker'),
    url(r'^walker/edit/$', 'walk.views.walker_edit', name='walker_edit'),
    url(r'^walker/sponsors/$', 'walk.views.walker_sponsors', name='walker_sponsors'),
    url(r'^walker/add-sponsor/$', 'walk.views.walker_add_sponsor', name='walker_add_sponsor'),
    url(r'^walker/edit-sponsor/(?P<id>\d+)/$', 'walk.views.walker_edit_sponsor', name='walker_edit_sponsor'),
    url(r'^walker/delete-sponsor/$', 'walk.views.walker_delete_sponsor', name='walker_delete_sponsor'),
    url(r'^walker/check_login/$', 'walk.views.walker_not_set', name='walker_not_set'),
    url(r'^mywalk/team/$', 'walk.views.walker_team', name='walker_team'),
    url(r'^walker/example/$', 'walk.views.walker_example', name='walker_example'),
    url(r'^walker/(?P<uuid>[a-z0-9\-]*)/$', 'walk.views.walker_home', name='walker_home'),
    url(r'^teams/$', 'walk.views.teams', name='teams'),
    url(r'^teams/new/$', 'walk.views.create_team', name='create_team'),

    (r'^paypal/872a9fcb-9a57-485c-853f-e581a3a0d277/$', MyEndPoint()),
   
    (r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'home.html'}),
    url(r'^(?P<username>[\w\._-]+)/$', 'walk.views.public_home', name='public_home'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
