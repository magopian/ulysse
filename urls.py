from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import settings
import jury
import concours

from concours.ircam import cursus1
from concours.ircam import residence

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Use old-style static file management    
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^admin/', include(admin.site.urls)),    
    url(r'^jury/admin/', include(jury.site.urls)),
    url(r'^ircam/cursus1-2011/admin/',   include(concours.ircam.cursus1.site.urls)),
    url(r'^ircam/residence-2011/admin/', include(concours.ircam.residence.site.urls)),
    (r'^$', 'web.views.show_home'),
)

