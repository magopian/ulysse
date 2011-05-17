#-*- coding: utf-8 -*-
from django import forms
from django.conf import settings
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
from models import Evaluation,EvaluationNote, EvaluationStatus, EvaluationNoteType
from forms  import CandidateAdminForm
from models import CandidateJuryAllocation    
from context_processors import in_competition_admin
from django.utils.translation import ugettext as _


def wrap_queryset(model_admin,qs):    
    ordering = model_admin.ordering or () # otherwise we might try to *None, which is bad ;)
    if ordering:
        qs = qs.order_by(*ordering)
    return qs
    

def add_candidates_to_group(modeladmin, request, queryset):
    selected = queryset.values_list('pk', flat=True)    
    referer = request.META["HTTP_REFERER"]
    return redirect("add_to_group?ids=%s&referer=%s" %  (",".join(selected),referer) )
    
add_candidates_to_group.short_description = _(u"Add selected candidates to a group")

def mark_candidates_as_valid(modeladmin, request, queryset):
    selected = queryset.values_list('pk', flat=True)
    Candidate.objects.filter(id__in=selected).update(is_valid=True)    
    
mark_candidates_as_valid.short_description = _(u"Mark selected candidates as valid")

def mark_candidates_as_invalid(modeladmin, request, queryset):
    selected = queryset.values_list('pk', flat=True)
    Candidate.objects.filter(id__in=selected).update(is_valid=False)    
    
mark_candidates_as_invalid.short_description = _(u"Mark selected candidates as invalid")

def import_candidates_to_step(modeladmin, request, queryset):
    active_step = modeladmin.admin_site.get_active_competition_step(request)
    active_comp = modeladmin.admin_site.get_active_competition(request)
    for c in queryset:
        if c.competition == active_comp and c.is_valid:
            caj = CandidateJuryAllocation(candidate=c, step=active_step)
            caj.save()
import_candidates_to_step.short_description = _(u"Import the selected candidates for this step")


def associate_jury_members_to_competition(modeladmin, request, queryset):
    selected = queryset.values_list('pk', flat=True)
    jury_members = JuryMember.objects.filter(id__in=selected)
    active_competition = modeladmin.admin_site.get_active_competition(request)
    for jury_member in jury_members:
        jury_member.competitions.add(active_competition)
        jury_member.save()
    
associate_jury_members_to_competition.short_description = _(u"Associate selected jury members to competition")

def remove_jury_member_from_competition(modeladmin, request, queryset):
    selected = queryset.values_list('pk', flat=True)
    selected = queryset.values_list('pk', flat=True)
    jury_members = JuryMember.objects.filter(id__in=selected)
    active_competition = modeladmin.admin_site.get_active_competition(request)
    for jury_member in jury_members:
        if active_competition in jury_member.competitions.all():
            jury_member.competitions.remove(active_competition)
            jury_member.save()
    
remove_jury_member_from_competition.short_description = _(u"Remove selected jury members from competition")

class CompetitionManagerInline(admin.TabularInline):
    model = CompetitionManager

class CompetitionModelAdmin(admin.ModelAdmin):        
    
    def get_urls(self):
        
        def wrap(view):
            def wrapper(*args, **kwargs):
                # "super admin" doesn't ask for competition selection
                if hasattr(self.admin_site, 'competition_admin_view'):
                    return self.admin_site.competition_admin_view(view)(*args, **kwargs)
                return view(*args, **kwargs)
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
    

class CandidateJuryAllocationInline(admin.TabularInline):
    model = CandidateJuryAllocation

class CandidateAdmin(CompetitionModelAdmin):        
    
    list_display  = ('last_name','first_name','is_valid')
    list_filter   = ['is_valid','groups']
    actions       = [add_candidates_to_group,mark_candidates_as_valid,mark_candidates_as_invalid]
    search_fields = ['composer__user__last_name',]
    inlines       = [CandidateJuryAllocationInline,]
    
    def queryset(self, request):
        if in_competition_admin(request):
            # Get candidates for active competition 
            qs = Candidate.objects.filter(competition=self.admin_site.get_active_competition(request))        
            return wrap_queryset(self,qs)
        else:
            return super(CandidateAdmin,self).queryset(request)
    
    def save_model(self, request, obj, form, change):
        if in_competition_admin(request):
            obj.competition = self.admin_site.get_active_competition(request)
        # Call base class
        super(CandidateAdmin,self).save_model(request,obj,form,change)
        
    def add_to_group(self,request):
        params = {}
        ids        = [int(id) for id in request.GET["ids"].split(',')]
        candidates = Candidate.objects.filter(id__in=ids)
        referer    = request.GET["referer"]
        params["candidates"] = candidates
        params["groups"]     = CandidateGroup.objects.filter(competition=self.admin_site.get_active_competition(request))
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
                    the_group.competition = self.admin_site.get_active_competition(request)
                    the_group.save()
                else:
                    the_group = CandidateGroup.objects.filter(competition=self.admin_site.get_active_competition(request),name=existing_group)[0]
                # Add the group to candidates
                for candidate in candidates:
                    if the_group not in candidate.groups.all():
                        candidate.groups.add(the_group)
                        candidate.save()
                return redirect(referer)
        params["errors"] = errors
        return render_to_response('admin/%s/%s/add_to_group.html' % (self.model._meta.app_label,self.model._meta.module_name),params,context_instance=RequestContext(request))        
    
    def edit_candidate(self,request,id):
        params = {}
        candidate = Candidate.objects.filter(id=id)[0]
        the_form = CandidateAdminForm()
        params["the_form"] = the_form
        return render_to_response('admin/edit_candidate.html',params,context_instance=RequestContext(request))        
    
    def get_urls(self):
        def wrap(view):
            def wrapper(*args, **kwargs):
                # "super admin" doesn't ask for competition selection
                if hasattr(self.admin_site, 'competition_admin_view'):
                    return self.admin_site.competition_admin_view(view)(*args, **kwargs)
                return view(*args, **kwargs)
            return update_wrapper(wrapper, view)
        
        info = self.model._meta.app_label, self.model._meta.module_name
        
        urls = super(CandidateAdmin, self).get_urls()               
        
        if hasattr(self.admin_site,'is_competition_admin_site'):                  
            my_urls = patterns('',                                    
                (r'^add_to_group', self.add_to_group),
                url(r'^(.+)/$',wrap(self.edit_candidate),name='%s_%s_change' % info),
            )            
            return my_urls + urls            
        else:            
            return urls

class CandidateToEvaluateAdmin(CompetitionModelAdmin):
    pass

class CandidateToImportAdmin(CandidateAdmin):
    actions = [import_candidates_to_step]
    list_display = ['last_name','first_name']
    list_filter = ['groups']
    search_fields = ['composer__user__last_name']

    def get_actions(self, request):
        """Keep only our own 'import candidates to step' action"""
        actions = super(CandidateToImportAdmin, self).get_actions(request)
        for k in actions.keys():
            if actions[k][0] not in self.actions:
                del actions[k]
        return actions

    def queryset(self, request):
        # only for the active competition
        qs = super(CandidateToImportAdmin, self).queryset(request)
        # only active candidates
        qs = qs.filter(is_valid=True)
        # only candidates not imported yet in the current step
        active_step = self.admin_site.get_active_competition_step(request)
        imported = CandidateJuryAllocation.objects.filter(step=active_step)
        imported = imported.values_list('candidate', flat=True)
        qs = qs.exclude(pk__in=imported)

        if in_competition_admin:
            return wrap_queryset(self, qs)
        return qs
        
class CandidateJuryAllocationAdmin(CompetitionModelAdmin):
    
    def last_name(self, obj):
      return obj.candidate.composer.user.last_name
    last_name.short_description = 'last name'
    
    def first_name(self, obj):
      return obj.candidate.composer.user.first_name
    first_name.short_description = 'first name'
    
    def queryset(self, request):
        # Get candidates for active competition step        
        qs = CandidateJuryAllocation.objects.filter(step=self.admin_site.get_active_competition_step(request))        
        return wrap_queryset(self,qs)
        
    
    list_display  = ('last_name','first_name','jury_')
    list_filter = ['jury_members',]
    filter_vertical = ['jury_members',]


class CandidateGroupAdmin(CompetitionModelAdmin):
    fields = ('name','members')
    filter_vertical = ['members',]
    list_display = ("name",)
    
    def save_model(self, request, obj, form, change):        
        obj.competition = self.admin_site.get_active_competition(request)
        obj.save()

class CompetitionStepResultsAdmin(CompetitionModelAdmin):
    
    def follow_results(self,request):
        params = {}                
        active_step = self.admin_site.get_active_competition_step(request)                
        #
        # Construct columns
        #
        columns = ['ID','Last name','First name']
        # Add a column for each jury member
        jury_members = active_step.get_jury_members()
        for jury_member in jury_members:
            columns.append("%s. %s" % (jury_member.user.first_name[0].upper(),jury_member.user.last_name))
        #
        # Construct lines
        #
        lines = []
        for candidate in active_step.get_candidates():
            line = [candidate.id,candidate.composer.user.last_name,candidate.composer.user.first_name]
            for jury_member in jury_members:
                evaluations = Evaluation.objects.filter(competition_step=active_step,candidate=candidate,jury_member=jury_member)
                if len(evaluations)==1:
                    evaluation = evaluations[0]
                    if evaluation.status.url == "completed":
                        result = evaluation.get_value()
                    elif evaluation.status.url == "in_progress":
                        result = "in progress"
                    elif evaluation.status.url == "to_process":
                        result = "to process"                        
                    else:
                        raise RuntimeError("Unhandled evaluation status : s%" % evaluation.status.url)                        
                else:
                    result = "N/A"
                line.append(result  )
            lines.append(line)
        params["columns"] = columns
        params["lines"]   = lines
        return render_to_response('admin/%s/%s/change_list.html' % (self.model._meta.app_label,self.model._meta.module_name),params,context_instance=RequestContext(request))                                
    
        
    def get_urls(self):
        
        def wrap(view):
            def wrapper(*args, **kwargs):
                # "super admin" doesn't ask for competition selection
                if hasattr(self.admin_site, 'competition_admin_view'):
                    return self.admin_site.competition_admin_view(view)(*args, **kwargs)
                return view(*args, **kwargs)
            return update_wrapper(wrapper, view)
        
        info = self.model._meta.app_label, self.model._meta.module_name        
        
        urls = super(CompetitionStepResultsAdmin, self).get_urls()               
        
        if hasattr(self.admin_site,'is_competition_admin_site'):                  
            my_urls = patterns('',                                                    
                url(r'^$',wrap(self.follow_results),name='%s_%s_change' % info),
            )            
            return my_urls + urls            
        else:            
            return urls
    
    
    def queryset(self, request):
        # Get results for active competition step        
        qs = CompetitionStepResults.objects.filter(step=self.admin_site.get_active_competition_step(request))        
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
            '%sjs/tiny_mce/tiny_mce.js' %  settings.STATIC_URL,
            '%sjs/admin_pages.js' %  settings.STATIC_URL
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
        obj.competition = self.admin_site.get_active_competition(request)
        obj.save()
        
    class Media:
            js = (
            '%sjs/tiny_mce/tiny_mce.js' % settings.STATIC_URL,
            '%sjs/admin_pages.js' % settings.STATIC_URL
        )


class JuryMemberAdmin(CompetitionModelAdmin):
    search_fields  = ['user__last_name',]
    list_display   = ('last_name','first_name')    
    list_filter    = ['competitions',]
    actions        = [associate_jury_members_to_competition,remove_jury_member_from_competition]
                      
    def last_name(self, obj):
      return obj.user.last_name
    last_name.short_description = 'last name'
    
    def first_name(self, obj):
      return obj.user.first_name
    first_name.short_description = 'first name'
    
    def save_model(self, request, obj, form, change):
        if in_competition_admin(request):
            obj.competition = self.admin_site.get_active_competition(request)
        # Call base class
        super(JuryMemberAdmin,self).save_model(request,obj,form,change)            

class JuryMemberGroupAdmin(CompetitionModelAdmin):
    fields = ('name','members')
    filter_vertical = ['members',]
    list_display = ("name",)
    
    def save_model(self, request, obj, form, change):        
        obj.competition = self.admin_site.get_active_competition(request)
        obj.save()
    

class CompetitionManagerAdmin(CompetitionModelAdmin):
    pass

class CompetitionStepFollowUpAdmin(CompetitionModelAdmin):
    
    def total(self,obj):        
        return obj.total
    
    def to_process(self,obj):
        return u"à implémenter"
    
    def in_progress(self,obj):
        return u"à implémenter"
    
    def completed(self,obj):
        return u"à implémenter"    
    
    
    def queryset(self, request):
        # Get jury members for active competition step
        active_step = self.admin_site.get_active_competition_step(request)        
        qs = CompetitionStepFollowUp.objects.filter(user__in=[jury.user for jury in active_step.get_jury_members()])        
        return wrap_queryset(self,qs)        
        
    def follow_evaluations(self,request):
        params = {}
        # Get all jury members for this step
        active_step = self.admin_site.get_active_competition_step(request)        
        qs = CompetitionStepFollowUp.objects.filter(user__in=[jury.user for jury in active_step.get_jury_members()])
        # Construct results
        columns = ['Jury member','Total','To process','In progress','Completed']
        lines = []
        for obj in qs:
            total = Evaluation.objects.filter(competition_step=active_step,jury_member=obj).count()
            to_process  = Evaluation.objects.filter(competition_step=active_step,jury_member=obj,status__url="to_process").count()
            in_progress = Evaluation.objects.filter(competition_step=active_step,jury_member=obj,status__url="in_progress").count()
            completed   = Evaluation.objects.filter(competition_step=active_step,jury_member=obj,status__url="completed").count()
            jury_member_link = "<a href=\"%s/\">%s %s</a>" % (obj.id,obj.user.first_name,obj.user.last_name)
            lines.append((jury_member_link,total,to_process,in_progress,completed))
        params["columns"] = columns
        params["lines"]   = lines
        return render_to_response('admin/%s/%s/change_list.html' % (self.model._meta.app_label,self.model._meta.module_name),params,context_instance=RequestContext(request))                
    
    def show_jury_member_evaluations(self,request,id):
        params = {}
        jury_member = CompetitionStepFollowUp.objects.get(id=id)
        evaluations = Evaluation.objects.filter(jury_member=jury_member,competition_step=self.admin_site.get_active_competition_step(request))
        params["jury_member"]  = jury_member
        params["evaluations"]  = evaluations
        return render_to_response('admin/%s/%s/change_form.html' % (self.model._meta.app_label,self.model._meta.module_name),params,context_instance=RequestContext(request))                
    
    def get_urls(self):
        
        def wrap(view):
            def wrapper(*args, **kwargs):
                # "super admin" doesn't ask for competition selection
                if hasattr(self.admin_site, 'competition_admin_view'):
                    return self.admin_site.competition_admin_view(view)(*args, **kwargs)
                return view(*args, **kwargs)
            return update_wrapper(wrapper, view)
        
        info = self.model._meta.app_label, self.model._meta.module_name        
        
        urls = super(CompetitionStepFollowUpAdmin, self).get_urls()               
        
        if hasattr(self.admin_site,'is_competition_admin_site'):                  
            my_urls = patterns('',                               
                url(r'^(.+)/$',wrap(self.show_jury_member_evaluations),name='%s_%s_edit' % info),
                url(r'^$',wrap(self.follow_evaluations),name='%s_%s_change' % info),
            )            
            return my_urls + urls            
        else:            
            return urls
    
    list_display   = ('user','total','to_process','in_progress','completed')   


class EvaluationNoteAdmin(CompetitionModelAdmin):
    list_filter  = ['note','candidate','jury_member']
    list_display  = ('candidate','jury_member','note','comments')


class EvaluationStatusAdmin(CompetitionModelAdmin):
    pass

class EvaluationNoteTypeAdmin(CompetitionModelAdmin):
    pass

class EvaluationNoteAdminInline(admin.TabularInline):
    model = EvaluationNote

class EvaluationAdmin(CompetitionModelAdmin):
    list_display  = ('competition_step','candidate','jury_member','status')
    list_filter  = ['competition_step','candidate','jury_member','status']
    inlines = [EvaluationNoteAdminInline,]

# Global administration registration    
admin.site.register(Competition,CompetitionAdmin)
admin.site.register(Candidate,CandidateAdmin)
admin.site.register(JuryMember,JuryMemberAdmin)
admin.site.register(Evaluation,EvaluationAdmin)
admin.site.register(EvaluationNoteType,EvaluationNoteTypeAdmin)
admin.site.register(EvaluationStatus,EvaluationStatusAdmin)
