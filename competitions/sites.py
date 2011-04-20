#-*- coding: utf-8 -*- 
from django.conf.urls.defaults import patterns, url, include
from django.contrib.admin.sites import AdminSite
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.template import RequestContext
import competitions

## Nota : this is specific to Ircam - Cursus 1 and should therefore must be moved in "specific.ircam.cursus1"

REDIRECTIONS = {
    u'candidates' : u'cursus1/candidatecursus1/',
    u'jury'       : u'competitions/jurymember/',    
    u'step/pre-jury/allocations' : u'prejury/candidatejuryallocationircamcursus1prejury/',
    u'step/pre-jury/evaluations' : u'prejury/competitionstepfollowupircamcursus1prejury/',
    u'step/pre-jury/results' : u'prejury/competitionstepresultsircamcursus1prejury/',
    u'step/jury/allocations' : u'jury/candidatejuryallocationircamcursus1jury/',
    u'step/jury/evaluations' : u'jury/competitionstepfollowupircamcursus1jury/',
    u'step/jury/results' : u'jury/competitionstepresultsircamcursus1jury/'    
}


        
#############################################################################################################

def internal_redirect(request,internal_url):
    from competitions import get_active_competition
    active_competition = get_active_competition(request)
    return redirect("/%s/%s" % (active_competition.url,internal_url))

class CompetitionAdminSite(AdminSite):
        
    def index(self, request, extra_context=None):
       return redirect('%sinfos' % request.META["PATH_INFO"])
    
           
    def show_informations(self,request):        
        from models import Competition
        from admin import CompetitionAdmin
        context = {}
        context['competition_admin'] = True
        context['title'] = ''
        return CompetitionAdmin(Competition,self).change_view(request,'1',context)        
        
    def show_candidates(self,request):        
        return internal_redirect(request,REDIRECTIONS['candidates'])        
        
    def show_jury(self,request):
        return internal_redirect(request,REDIRECTIONS['jury'])        
        
    def show_step(self,request,url):
        return redirect('%s/allocations' % request.META["PATH_INFO"])        
        
    def show_step_allocations(self,request,url):
        return internal_redirect(request,REDIRECTIONS['step/%s/allocations' % url])        
        
    def show_step_evaluations(self,request,url):
        return internal_redirect(request,REDIRECTIONS['step/%s/evaluations' % url])        
        
    def show_step_results(self,request,url):
        return internal_redirect(request,REDIRECTIONS['step/%s/results' % url])                
    
    def get_urls(self):
        urls = super(CompetitionAdminSite,self).get_urls()           
        my_urls = patterns('',            
            (r'^admin',super(CompetitionAdminSite,self).index),
            (r'^infos',self.show_informations),
            (r'^candidates', self.show_candidates) ,           
            (r'^jury', self.show_jury),            
            (r'^step/(?P<url>.*)/allocations', self.show_step_allocations),
            (r'^step/(?P<url>.*)/evaluations', self.show_step_evaluations),
            (r'^step/(?P<url>.*)/results', self.show_step_results),
            (r'^step/(?P<url>.*)', self.show_step)
        )
        return urls + my_urls 
        
        

    
        
        





