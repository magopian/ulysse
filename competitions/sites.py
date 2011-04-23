#-*- coding: utf-8 -*- 
from django.conf.urls.defaults import patterns, url, include
from django.contrib.admin.sites import AdminSite
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.template import RequestContext
from composers.models import Composer
from admin import CandidateAdmin
from partners.models import Partner
from partners.admin import PartnerAdmin
from composers.models import Composer, Work, AdministrativeDocument
from composers.admin import ComposerAdmin, WorkAdmin, AdministrativeDocumentAdmin
from competitions.models import Competition, CompetitionStep, JuryMember, CandidateJuryAllocation, CompetitionStepFollowUp, CompetitionStepResults
from competitions.admin import CompetitionAdmin, JuryMemberAdmin, CandidateJuryAllocationAdmin, CompetitionStepFollowUpAdmin, CompetitionStepResultsAdmin
from session import get_active_competition

    
class CompetitionAdminSite(AdminSite):          
    
    def index(self, request, extra_context=None):
       return redirect('%sinfos' % request.META["PATH_INFO"])
           
    def register_models(self):
        self.register(Partner,PartnerAdmin)
        self.register(Composer,ComposerAdmin)
        self.register(Work,WorkAdmin)
        self.register(AdministrativeDocument,AdministrativeDocumentAdmin)
        self.register(JuryMember,JuryMemberAdmin)
        self.register(CandidateJuryAllocation,CandidateJuryAllocationAdmin)
        self.register(CompetitionStepFollowUp,CompetitionStepFollowUpAdmin)
        self.register(CompetitionStepResults,CompetitionStepResultsAdmin)
            
    def show_informations(self,request):        
        from models import Competition
        from admin import CompetitionAdmin
        context = {}
        context['competition_admin'] = True
        context['title'] = ''
        return CompetitionAdmin(Competition,self).change_view(request,'1',context)        
                    
    def show_step(self,request,url):
        return redirect('%s/allocations/' % request.META["PATH_INFO"])               
        
    def get_steps(self):
        raise RuntimeError("Should be overriden in derived class")
    
    def get_urls(self):
        
        urls = super(CompetitionAdminSite,self).get_urls()
        
        my_urls = patterns('',            
            (r'^admin',super(CompetitionAdminSite,self).index),
            (r'^infos',self.show_informations),                                    
            (r'^jury/', include(self._registry[JuryMember].urls)),                                            
        )
        
        for step_name in self.get_steps():
            my_urls += patterns('',
                (r'^step/%s/allocations/' % step_name, include(self._registry[CandidateJuryAllocation].urls)),
                (r'^step/%s/evaluations/' % step_name, include(self._registry[CompetitionStepFollowUp].urls)),
                (r'^step/%s/results/' % step_name, include(self._registry[CompetitionStepResults].urls)),
            )
        
        # Nota : this should be defined after steps        
        
        my_urls += patterns('',                                        
            (r'^step/(?P<url>.*)', self.show_step),
        )
            
        return my_urls + urls
        
        

    
        
        





