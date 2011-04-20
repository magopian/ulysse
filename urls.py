from django.conf.urls.defaults import patterns, include, url
import settings
import jury
import competitions
from specific.ircam import cursus1

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',        
    url(r'^admin/', include(admin.site.urls)),    
    url(r'^jury/admin/', include(jury.site.urls)),
    url(r'^ircam-cursus1/',   include(cursus1.site.urls)),    
    (r'^$', 'web.views.show_home'),
)

