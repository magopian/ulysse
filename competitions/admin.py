#-*- coding: utf-8 -*- 
from django.contrib import admin
from django.contrib.admin import TabularInline
from models import Candidate
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
from models import EvaluationYesNo
from models import EvaluationYesNoAndNote
from models import CandidateJuryAllocation    
from session import get_active_competition

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
    

class CandidateAdmin(admin.ModelAdmin):    
        
    list_display  = ('nom_','prenom_')
    
    def save_model(self, request, obj, form, change):        
        obj.competition = get_active_competition(request)
        obj.save()
        
class CandidateJuryAllocationAdmin(admin.ModelAdmin):
    
    def queryset(self, request):
        # Get candidates for active competition step        
        qs = CandidateJuryAllocation.objects.filter(step=get_active_competition_step(request))        
        return wrap_queryset(self,qs)
        
    
    list_display  = ('nom_','prenom_','jury_')
    list_filter = ['jury_members']
    filter_vertical = ['jury_members',]


class CandidateGroupAdmin(admin.ModelAdmin):
    fields = ('name','members')
    filter_vertical = ['members',]
    list_display = ("name",)
    
    def save_model(self, request, obj, form, change):        
        obj.competition = get_active_competition(request)
        obj.save()

class CompetitionStepResultsAdmin(admin.ModelAdmin):
    
    def queryset(self, request):
        # Get results for active competition step        
        qs = CompetitionStepResults.objects.filter(step=get_active_competition_step(request))        
        return wrap_queryset(self,qs)
    
    list_display   = ('nom_','prenom_','evaluations_')   


class CompetitionStepInline(TabularInline):
    model = CompetitionStep
    extra = 2
    
class CompetitionAdmin(admin.ModelAdmin):
    search_fields   = ["title"]
    list_display    = ('title','subtitle','managing_partner','opening_date','closing_date','is_published','is_open')
    list_filter     = ['is_published','is_open','managing_partner','additional_partners']    
    filter_vertical = ['additional_partners']    
    inlines = (CompetitionStepInline,)    
    
    fieldsets = (
        ('Titre & présentation', {
            'classes': ('wide',),
            'fields': ('title','url','subtitle','presentation')
        }),
        ('Organisateur & partenaires', {
            'classes': ('wide',),
            'fields': ('managing_partner','additional_partners')                
        }),
        ('Dates', {
            'classes': ('wide',),
            'fields': ('information_date','opening_date','closing_date','result_date')                
        }),
        ('Statut', {
            'classes': ('wide',),
            'fields': ('is_published','is_open','is_archived')                
        }),        
    )
        
    class Media:
            js = (
            '/static/js/tiny_mce/tiny_mce.js',
            '/static/js/admin_pages.js'
        )
        
    

class CompetitionStepAdmin(admin.ModelAdmin):
    pass

class CompetitionNewsAdmin(admin.ModelAdmin):
    search_fields = ('title','text')
    list_display  = ('date','title','text')
    fieldsets = (
        ('Actualité liée au concours', {
            'classes': ('wide',),
            'fields': ('title','date','text')
        }),    
    )
    
    def save_model(self, request, obj, form, change):        
        obj.competition = get_active_competition(request)
        obj.save()



class JuryMemberAdmin(admin.ModelAdmin):
    search_fields = ['jury__user__last_name',]
    list_display   = ('jury','competition')
    list_filter    = ["competition",]
    
    def save_model(self, request, obj, form, change):        
        obj.competition = get_active_competition(request)
        obj.save()
    

class JuryMemberGroupAdmin(admin.ModelAdmin):
    fields = ('name','members')
    filter_vertical = ['members',]
    list_display = ("name",)
    
    def save_model(self, request, obj, form, change):        
        obj.competition = get_active_competition(request)
        obj.save()
    

class CompetitionManagerAdmin(admin.ModelAdmin):
    pass

class CompetitionStepFollowUpAdmin(admin.ModelAdmin):
    
    def queryset(self, request):
        # Get jury members for active competition step
        active_step = get_active_competition_step(request)        
        qs = CompetitionStepFollowUp.objects.filter(jury__in=active_step.get_jury_members())        
        return wrap_queryset(self,qs)
    
    def get_query_set(self):        
        # Get all jury members for this step
        jury_members = []
        for item in CandidateJuryAllocation.objects.all():
            for jury_member in item.jury_members.all():
                if not jury_member in jury_members:
                    jury_members.append(jury_member)
        return super(CompetitionStepFollowUpIrcamCursus1JuryManager, self).get_query_set().filter(jury__in=jury_members)
    
    list_display   = ('jury','total_','en_attente_','en_cours_','terminees_')   


class EvaluationYesNoAndNoteAdmin(admin.ModelAdmin):
    list_filter  = ['yes','candidate','jury_member']
    list_display  = ('candidate','jury_member','yes','note','comments')

class EvaluationYesNoAdmin(admin.ModelAdmin):
    list_filter  = ['yes','candidate','jury_member']
    list_display  = ('candidate','jury_member','yes','comments')
    
class EvaluationNoteAdmin(admin.ModelAdmin):
    list_filter  = ['note','candidate','jury_member']
    list_display  = ('candidate','jury_member','note','comments')

# Global administration registration    
admin.site.register(Competition,CompetitionAdmin)
admin.site.register(Candidate,CandidateAdmin)
