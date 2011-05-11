#-*- coding: utf-8 -*-
from django import forms
from django.contrib import admin
from django.utils.functional import update_wrapper
from django.shortcuts import redirect, render_to_response
from django.conf.urls.defaults import patterns, url, include
from django.contrib.admin import TabularInline
from django.template import RequestContext
from models import Candidate, CandidateGroup
from models import Partner
from models import Competition
from models import CompetitionStep
from models import CompetitionNews
from models import CompetitionStepFollowUp
from models import CompetitionStepResults
from models import JuryMember
from models import JuryMemberGroup
from models import CompetitionManager
from models import EvaluationNote
from forms  import CandidateAdminForm
from models import CandidateJuryAllocation    
from session import get_active_competition
from context_processors import in_competition_admin
from django.utils.translation import ugettext as _

def get_active_competition_step(request):
    # Get step name from url
    path = request.META["PATH_INFO"]
    tokens = path.split('/')
    i = tokens.index('step')
    step_url = tokens[i+1]
    # Get CompetitionStep object
    active_competition = get_active_competition(request)
    results = CompetitionStep.objects.filter(competition=active_competition,url=step_url)
    if len(results)==0:
        raise RuntimeError("Could not find a step with url '%s' for competition '%s'" % (step_url,active_competition))
    return results[0]
    
def wrap_queryset(model_admin,qs):    
    ordering = model_admin.ordering or () # otherwise we might try to *None, which is bad ;)
    if ordering:
        qs = qs.order_by(*ordering)
    return qs
    

def add_candidates_to_group(modeladmin, request, queryset):
    selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
    referer = request.META["HTTP_REFERER"]
    return redirect("add_to_group?ids=%s&referer=%s" %  (",".join(selected),referer) )
    
add_candidates_to_group.short_description = _(u"Add selected candidates to a group")

def mark_candidates_as_valid(modeladmin, request, queryset):
    selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)    
    Candidate.objects.filter(id__in=selected).update(is_valid=True)    
    
mark_candidates_as_valid.short_description = _(u"Mark selected candidates as valid")

def mark_candidates_as_invalid(modeladmin, request, queryset):
    selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)    
    Candidate.objects.filter(id__in=selected).update(is_valid=False)    
    
mark_candidates_as_invalid.short_description = _(u"Mark selected candidates as invalid")

class CompetitionManagerInline(admin.TabularInline):
    model = CompetitionManager

class CompetitionModelAdmin(admin.ModelAdmin):        
    
    def get_urls(self):
        
        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.competition_admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)
                       
        info = self.model._meta.app_label, self.model._meta.module_name                

        urlpatterns = patterns('',
            url(r'^$',
                wrap(self.changelist_view),
                name='%s_%s_changelist' % info),
            url(r'^add/$',
                wrap(self.add_view),
                name='%s_%s_add' % info),
            url(r'^(.+)/history/$',
                wrap(self.history_view),
                name='%s_%s_history' % info),
            url(r'^(.+)/delete/$',
                wrap(self.delete_view),
                name='%s_%s_delete' % info),
            url(r'^(.+)/$',
                wrap(self.change_view),
                name='%s_%s_change' % info),
        )
        
        return urlpatterns        
    

class CandidateAdmin(CompetitionModelAdmin):    
    
    form          = CandidateAdminForm        
    list_display  = ('last_name','first_name','is_valid')
    list_filter   = ['is_valid','groups']
    actions       = [add_candidates_to_group,mark_candidates_as_valid,mark_candidates_as_invalid]
    search_fields = ['composer__user__last_name',]
    
    def queryset(self, request):
        if in_competition_admin(request):
            # Get candidates for active competition 
            qs = Candidate.objects.filter(competition=get_active_competition(request))        
            return wrap_queryset(self,qs)
        else:
            return super(CandidateAdmin,self).queryset(request)
    
    def save_model(self, request, obj, form, change):
        if in_competition_admin(request):
            obj.competition = get_active_competition(request)
        # Call base class
        super(CandidateAdmin,self).save_model(request,obj,form,change)
        
    def add_to_group(self,request):
        params = {}
        ids        = [int(id) for id in request.GET["ids"].split(',')]
        candidates = Candidate.objects.filter(id__in=ids)
        referer    = request.GET["referer"]
        params["candidates"] = candidates
        params["groups"]     = CandidateGroup.objects.filter(competition=get_active_competition(request))
        errors = []
        if request.method == 'POST': # If the form has been submitted...
            new_group= None
            existing_group = None
            action_choice = None
            if request.POST.__contains__("action_choice"):
                action_choice = int(request.POST["action_choice"])
                if action_choice==1:
                    # Create new group                    
                    if request.POST.__contains__("new_group"):
                        new_group = request.POST["new_group"]
                    if not new_group:
                        errors.append(u"Merci de préciser le nom du nouveau groupe")
                else:
                    # Add to existing group                    
                    if request.POST.__contains__("existing_group"):
                        existing_group = request.POST["existing_group"]
                    if not existing_group:
                        errors.append(u"Merci de sélectionner un groupe")                    
            else:
                errors.append(u"Merci de sélectionner un choix d'action")
            if not errors:
                # Add to candidates to groups and redirect to referer
                the_group = None
                if new_group:
                    the_group = CandidateGroup()
                    the_group.name = new_group
                    the_group.competition = get_active_competition(request)
                    the_group.save()
                else:
                    the_group = CandidateGroup.objects.filter(competition=get_active_competition(request),name=existing_group)[0]
                # Add the group to candidates
                for candidate in candidates:
                    if the_group not in candidate.groups.all():
                        candidate.groups.add(the_group)
                        candidate.save()
                return redirect(referer)
        params["errors"] = errors
        return render_to_response('admin/%s/%s/add_to_group.html' % (self.model._meta.app_label,self.model._meta.module_name),params,context_instance=RequestContext(request))        
    
    def get_urls(self):
        urls = super(CandidateAdmin, self).get_urls()
        my_urls = patterns('',                                    
            (r'^add_to_group', self.add_to_group)
        )
        return my_urls + urls
        
class CandidateJuryAllocationAdmin(CompetitionModelAdmin):
    
    def queryset(self, request):
        # Get candidates for active competition step        
        qs = CandidateJuryAllocation.objects.filter(step=get_active_competition_step(request))        
        return wrap_queryset(self,qs)
        
    
    list_display  = ('nom_','prenom_','jury_')
    list_filter = ['jury_members',]
    filter_vertical = ['jury_members',]


class CandidateGroupAdmin(CompetitionModelAdmin):
    fields = ('name','members')
    filter_vertical = ['members',]
    list_display = ("name",)
    
    def save_model(self, request, obj, form, change):        
        obj.competition = get_active_competition(request)
        obj.save()

class CompetitionStepResultsAdmin(CompetitionModelAdmin):
    
    def queryset(self, request):
        # Get results for active competition step        
        qs = CompetitionStepResults.objects.filter(step=get_active_competition_step(request))        
        return wrap_queryset(self,qs)
    
    list_display   = ('nom_','prenom_','evaluations_')   


class CompetitionStepInline(TabularInline):
    model = CompetitionStep
    extra = 2
    
class CompetitionAdmin(CompetitionModelAdmin):
    search_fields   = ["title"]
    list_display    = ('title','subtitle','managing_partner','opening_date','closing_date','is_published','is_open')
    list_filter     = ['is_published','is_open','managing_partner','additional_partners']        
    inlines = (CompetitionStepInline,CompetitionManagerInline,)    
    
    fieldsets = (
        (_(u'General informations'), {
            'classes': ('collapse',),
            'fields': ('title','url','subtitle','presentation')
        }),
        (_(u'Manager & partners'), {
            'classes': ('collapse',),
            'fields': ('managing_partner','additional_partners')                
        }),
        (_(u'Dates'), {
            'classes': ('collapse',),
            'fields': ('information_date','opening_date','closing_date','result_date')                
        }),
        (_(u'Status'), {
            'classes': ('collapse',),
            'fields': ('is_published','is_open','is_archived')                
        }),        
    )
        
    class Media:
            js = (
            '/static/js/tiny_mce/tiny_mce.js',
            '/static/js/admin_pages.js'
        )
        
    

class CompetitionStepAdmin(CompetitionModelAdmin):
    pass

class CompetitionNewsAdmin(CompetitionModelAdmin):
    search_fields = ('title','text')
    list_display  = ('date','title','text')
    fieldsets = (
        ('Competition news', {
            'classes': ('wide',),
            'fields': ('title','date','text')
        }),    
    )
    
    def save_model(self, request, obj, form, change):        
        obj.competition = get_active_competition(request)
        obj.save()
        
    class Media:
            js = (
            '/static/js/tiny_mce/tiny_mce.js',
            '/static/js/admin_pages.js'
        )



class JuryMemberAdmin(CompetitionModelAdmin):
    search_fields = ['user__last_name',]
    list_display   = ('user',)
    list_filter    = ["competitions",]       
    
    def save_model(self, request, obj, form, change):
        if in_competition_admin(request):
            obj.competition = get_active_competition(request)
        # Call base class
        super(JuryMemberAdmin,self).save_model(request,obj,form,change)            

class JuryMemberGroupAdmin(CompetitionModelAdmin):
    fields = ('name','members')
    filter_vertical = ['members',]
    list_display = ("name",)
    
    def save_model(self, request, obj, form, change):        
        obj.competition = get_active_competition(request)
        obj.save()
    

class CompetitionManagerAdmin(CompetitionModelAdmin):
    pass

class CompetitionStepFollowUpAdmin(CompetitionModelAdmin):
    
    def queryset(self, request):
        # Get jury members for active competition step
        active_step = get_active_competition_step(request)        
        qs = CompetitionStepFollowUp.objects.filter(user__in=[jury.user for jury in active_step.get_jury_members()])        
        return wrap_queryset(self,qs)
    
    def get_query_set(self):        
        # Get all jury members for this step
        jury_members = []
        for item in CandidateJuryAllocation.objects.all():
            for jury_member in item.jury_members.all():
                if not jury_member in jury_members:
                    jury_members.append(jury_member)
        return super(CompetitionStepFollowUpIrcamCursus1JuryManager, self).get_query_set().filter(jury__in=jury_members)
    
    list_display   = ('user','total_','en_attente_','en_cours_','terminees_')   


class EvaluationNoteAdmin(CompetitionModelAdmin):
    list_filter  = ['note','candidate','jury_member']
    list_display  = ('candidate','jury_member','note','comments')

# Global administration registration    
admin.site.register(Competition,CompetitionAdmin)
admin.site.register(Candidate,CandidateAdmin)
admin.site.register(JuryMember,JuryMemberAdmin)
