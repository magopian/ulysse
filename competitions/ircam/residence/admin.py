#-*- coding: utf-8 -*- 
from django.contrib  import admin
from competitions.admin import CandidateAdmin
from competitions.ircam.residence.models import ProjectTopicArea
from competitions.ircam.residence.models import EvaluationLevel
from competitions.ircam.residence.models import CandidateResidence
from competitions.ircam.residence.models import EvaluationResidenceJury
from competitions.ircam.residence.models import EvaluationResidencePostJury
from competitions.ircam.residence import site

class ProjectTopicAreaAdmin(admin.ModelAdmin):    
    pass

class EvaluationLevelAdmin(admin.ModelAdmin):    
    pass

class CandidateResidenceAdmin(CandidateAdmin):
    filter_vertical = ("topic_areas",)
    fieldsets = (
        ('Personal informations', {
            'classes': ('wide',),
            'fields': ('composer','short_biography','curriculum_vitae','motivation_letter')                
        }),        
        ('Project submission', {
            'classes': ('wide',),
            'fields': ('title','additional_authors','topic_areas','state_of_the_art_description','project_description','relevance_to_ircam_research','work_plan')
        }),
        ('Multimedia samples', {
            'classes': ('wide',),
            'fields': ('multimedia_sample_1','multimedia_sample_1_notes','multimedia_sample_2','multimedia_sample_2_notes')
        }),
                
    )
    
    def save_model(self, request, obj, form, change):
        obj.competition = concours.get_active_competition(request)
        obj.save()
    

class EvaluationResidenceJuryAdmin(admin.ModelAdmin):
    pass

class EvaluationResidencePostJuryAdmin(admin.ModelAdmin):
    pass

# Register common models
from jury.admin import register as register_jury
from competitions.admin import register as register_competitions
from composers.admin import register as register_composers
register_jury(site)
register_competitions(site)
register_composers(site)

# Register Ircam residence specific models
site.register(ProjectTopicArea,ProjectTopicAreaAdmin)
site.register(EvaluationLevel,EvaluationLevelAdmin)
site.register(CandidateResidence,CandidateResidenceAdmin)
site.register(EvaluationResidenceJury,EvaluationResidenceJuryAdmin)
site.register(EvaluationResidencePostJury,EvaluationResidencePostJuryAdmin)

