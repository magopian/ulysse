from django.conf.urls.defaults import patterns, include, url
import settings
import jury
import competitions

from competitions.ircam import cursus1
from competitions.ircam import residence

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',        
    url(r'^admin/', include(admin.site.urls)),    
    url(r'^jury/admin/', include(jury.site.urls)),
    url(r'^ircam/cursus1-2011/admin/',   include(competitions.ircam.cursus1.site.urls)),
    url(r'^ircam/residence-2011/admin/', include(competitions.ircam.residence.site.urls)),
    (r'^$', 'web.views.show_home'),
)

