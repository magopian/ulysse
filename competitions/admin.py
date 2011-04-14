#-*- coding: utf-8 -*- 
from django.contrib import admin
from django.contrib.admin import TabularInline
from competitions.models import Partner
from competitions.models import Competition
from competitions.models import CompetitionStep
from competitions.models import CompetitionNews
from competitions.models import Candidate
from competitions.models import CandidateGroup
from competitions.models import JuryMember
from competitions.models import JuryMemberGroup
from competitions.models import CompetitionManager
from competitions.models import Evaluation

import jury


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
        ('Informations générales', {
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
        from competitions import get_active_competition
        obj.competition = get_active_competition(request)
        obj.save()

class CandidateAdmin(admin.ModelAdmin):    
    list_display  = ('nom_','prenom_')
    
    def save_model(self, request, obj, form, change):
        from competitions import get_active_competition
        obj.competition = get_active_competition(request)
        obj.save()


class CandidateGroupAdmin(admin.ModelAdmin):
    fields = ('name','members')
    filter_vertical = ['members',]
    list_display = ("name",)
    
    def save_model(self, request, obj, form, change):
        from competitions import get_active_competition
        obj.competition = get_active_competition(request)
        obj.save()


class JuryMemberAdmin(admin.ModelAdmin):
    search_fields = ['jury__user__last_name',]
    list_display   = ('jury','competition')
    list_filter    = ["competition",]
    
    def save_model(self, request, obj, form, change):
        from competitions import get_active_competition
        obj.competition = get_active_competition(request)
        obj.save()
    

class JuryMemberGroupAdmin(admin.ModelAdmin):
    fields = ('name','members')
    filter_vertical = ['members',]
    list_display = ("name",)
    
    def save_model(self, request, obj, form, change):
        from competitions import get_active_competition
        obj.competition = get_active_competition(request)
        obj.save()
    

class EvaluationAdmin(admin.ModelAdmin):
    pass

class CompetitionManagerAdmin(admin.ModelAdmin):
    pass

def register(site):
    site.register(JuryMember,JuryMemberAdmin)
    site.register(JuryMemberGroup,JuryMemberGroupAdmin)
    site.register(CandidateGroup,CandidateGroupAdmin)
    site.register(Competition,CompetitionAdmin)
    site.register(CompetitionNews,CompetitionNewsAdmin)    

# Global administration registration    
admin.site.register(Competition,CompetitionAdmin)
