#-*- coding: utf-8 -*- 
from django.conf.urls.defaults import patterns, url, include
from django.core.exceptions import PermissionDenied
from django.contrib.admin.sites import AdminSite
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.template import RequestContext
from django.utils.functional import update_wrapper
from composers.models import Composer
from admin import CandidateAdmin
from partners.models import Partner
from partners.admin import PartnerAdmin
from forms import CompetitionAdminAuthenticationForm
from composers.models import Composer, Work, Document, TextElement
from composers.admin import ComposerAdmin, WorkAdmin, DocumentAdmin, TextElementAdmin
from competitions.models import Competition, CompetitionStep, JuryMember, CandidateJuryAllocation, CompetitionStepFollowUp, CompetitionStepResults, Candidate, CompetitionManager, CompetitionNews
from competitions.admin import CompetitionAdmin, JuryMemberAdmin, CandidateJuryAllocationAdmin, CompetitionStepFollowUpAdmin, CompetitionStepResultsAdmin, CandidateAdmin, CompetitionNewsAdmin
from django.contrib.auth.signals import user_logged_out, user_logged_in
from views import import_candidates, notify_jury_members
import settings

def on_user_logged_in(sender, **kwargs):
    request = kwargs['request']
    jury_member = JuryMember.objects.filter(user=request.user).exists()
    if jury_member:
        from competitions import admin_site        
        admin_site.set_jury_member(request)
user_logged_in.connect(on_user_logged_in)

def on_user_logged_out(sender, **kwargs):
    request = kwargs['request']
    from competitions import admin_site        
    admin_site.clear_active_competition(request)
    admin_site.clear_jury_member(request)
user_logged_out.connect(on_user_logged_out)

class CompetitionAdminSite(AdminSite):
    
    login_form = CompetitionAdminAuthenticationForm
    
    def select_competition(self,request,id):
        """
        Sets the active competition and redirect to competition admin home page
        """
        # Perform security check
        if not request.user.is_authenticated():
            return self.login(request)            

        checked = False
        if request.user.is_superuser:                
            checked = True
        else:
            # Competition should be managed by current user
            competition = Competition.objects.get(id=id)

            if self.get_jury_member(request):
                jm = JuryMember.objects.get(user=request.user)
                checked = competition in jm.competitions.all()
            else:
                checked = CompetitionManager.objects.filter(user=request.user, competition=competition).exists()
        if not checked:
            raise PermissionDenied()
        # Set active competition
        self.set_active_competition(request,id)
        # Redirect to admin home page
        return redirect('/admin')
        
    def get_active_competition_step(self,request):
        # Get step name from url
        path = request.META["PATH_INFO"]
        tokens = path.split('/')
        i = tokens.index('step')
        step_url = tokens[i+1]
        # Get CompetitionStep object        
        active_competition = self.get_active_competition(request)
        results = CompetitionStep.objects.filter(competition=active_competition,url=step_url)
        if len(results)==0:
            raise RuntimeError("Could not find a step with url '%s' for competition '%s'" % (step_url,active_competition))
        return results[0]    
        
        
    def get_active_competition(self,request):    
        if not request.session.__contains__(settings.ACTIVE_COMPETITION_KEY ):
            return None
        active_competition = request.session[settings.ACTIVE_COMPETITION_KEY ]
        if not type(active_competition) is Competition:
            return None
        return active_competition
    
    def set_active_competition(self,request,id):    
        request.session[settings.ACTIVE_COMPETITION_KEY] = Competition.objects.get(id=id)
        
    def clear_active_competition(self,request):
        if settings.ACTIVE_COMPETITION_KEY in request.session:
            del request.session[settings.ACTIVE_COMPETITION_KEY]
        
    def get_jury_member(self,request):
        return request.session.get(settings.JURY_MEMBER_KEY, False)
    
    def set_jury_member(self,request):
        request.session[settings.JURY_MEMBER_KEY] = True
    
    def clear_jury_member(self,request):
        if settings.JURY_MEMBER_KEY in request.session:
            del request.session[settings.JURY_MEMBER_KEY]

    
    def choose_competition(self,request):
        """
        Displays a view allowing logged user to select which competition he want to administrate    
        """   
        competitions = []    
        if request.user.is_superuser:
            # If current user is a super user : choose among all competitions
            competitions = Competition.objects.all()
        elif self.get_jury_member(request): # user is 'jury-member'
            jm = JuryMember.objects.get(user=request.user)
            competitions = jm.competitions.all()
        else: # Current user is 'competition-admin'
            competitions = Competition.objects.filter(competitionmanager__user=request.user)
        # Display a view allowing user to select the competition
        params = {}
        params["is_superuser"] = request.user.is_superuser
        params["competitions"] = competitions
        return render_to_response('admin/choose_competition.html', params,context_instance=RequestContext(request))
    
    def competition_admin_view(self, view):
        """
        Decorator to create an admin view attached to this ``CompetitionAdminSite``.
        Checks

        You'll want to use this from within ``CompetitionAdminSite.get_urls()``:

            class MyAdminSite(CompetitionAdminSite):

                def get_urls(self):
                    from django.conf.urls.defaults import patterns, url

                    urls = super(MyAdminSite, self).get_urls()
                    urls += patterns('',
                        url(r'^my_view/$', self.competition_admin_view(some_view))
                    )
                    return urls
        """
        def inner(request, *args, **kwargs):            
            if not self.has_permission(request):
                return self.login(request)            
            if not self.get_active_competition(request):
                return self.choose_competition(request)
            return self.admin_view(view)(request, *args, **kwargs)        
        # Call update_wrapper helper function
        return update_wrapper(inner, view)
    
    def index(self, request, extra_context=None):
        if self.get_jury_member(request):
            return redirect('%scandidates' % request.META['PATH_INFO'])
        return redirect('%sinfos' % request.META["PATH_INFO"])
           
    def register_models(self):
        self.register(Partner,PartnerAdmin)
        self.register(Composer,ComposerAdmin)
        self.register(Work,WorkAdmin)
        self.register(Document,DocumentAdmin)
        self.register(TextElement,TextElementAdmin)
        self.register(JuryMember,JuryMemberAdmin)
        self.register(Candidate,CandidateAdmin)
        self.register(CompetitionNews,CompetitionNewsAdmin)
        self.register(CandidateJuryAllocation,CandidateJuryAllocationAdmin)
        self.register(CompetitionStepFollowUp,CompetitionStepFollowUpAdmin)
        self.register(CompetitionStepResults,CompetitionStepResultsAdmin)                
    
    def show_informations(self,request):        
        from models import Competition
        context = {}
        context['competition_admin'] = True
        context['title'] = ''
        active_competition = self.get_active_competition(request)        
        return CompetitionAdmin(Competition,self).change_view(request,'%s' % active_competition.id,context)        
                    
    def show_step(self,request,url):
        return redirect('%s/allocations/' % request.META["PATH_INFO"])               
        
    def get_steps(self):
        return ['pre-jury','jury'] # Temporaire ! A rendre dynamique et dépendant du concours              
    
    def get_urls(self):
        
        urls = super(CompetitionAdminSite,self).get_urls()
        
        my_urls = patterns('',            
            (r'^admin',super(CompetitionAdminSite,self).index),
            # This url doesn't use competition_admin_view wrapper
            (r'^select_competition/(?P<id>.*)',self.select_competition),
            # The urls below use competition_admin_view wrapper
            (r'^infos',self.competition_admin_view(self.show_informations)),                       
        )                               
        
        my_urls += patterns('',
            (r'^jury_members/',include(self._registry[JuryMember].urls)),
            (r'^candidates/',include(self._registry[Candidate].urls)),
            (r'^news/',include(self._registry[CompetitionNews].urls))
        )
        
        for step_name in self.get_steps():
            my_urls += patterns('',
                (r'^step/%s/importation/' % step_name, import_candidates),                 
                (r'^step/%s/allocations/' % step_name, include(self._registry[CandidateJuryAllocation].urls)),
                (r'^step/%s/notifications/' % step_name, notify_jury_members),                 
                (r'^step/%s/evaluations/' % step_name, include(self._registry[CompetitionStepFollowUp].urls)),                
                (r'^step/%s/results/' % step_name, include(self._registry[CompetitionStepResults].urls)),                 
            )            
        
        # Nota : this should be defined after steps, because of regex evaluation precedence
        
        my_urls += patterns('',                                        
            (r'^step/(?P<url>.*)', self.show_step),
        )
            
        return my_urls + urls
        
        

    
        
        





