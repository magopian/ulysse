from django.conf.urls.defaults import patterns, include, url
import settings
import competitions

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^super-admin/', include(admin.site.urls)),    
    url(r'^admin/', include(competitions.admin_site.urls)),    
    (r'^$', 'web.views.show_home'),
)

