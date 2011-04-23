from django.conf.urls.defaults import patterns, include, url
import settings
import jury
import competitions
from specific.ircam import cursus1

from django.contrib import admin
admin.autodiscover()

def show_test_page(request):
    from django.shortcuts import render_to_response
    return render_to_response('test_page.html')

urlpatterns = patterns('',
    (r'^test',show_test_page),
    url(r'^admin/', include(admin.site.urls)),    
    url(r'^jury/admin/', include(jury.site.urls)),
    url(r'^ircam-cursus1/',   include(cursus1.site.urls)),    
    (r'^$', 'web.views.show_home'),
)

