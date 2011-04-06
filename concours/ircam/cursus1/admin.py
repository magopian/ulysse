#-*- coding: utf-8 -*- 
from django.contrib  import admin
from concours.admin import CandidateAdmin 
from concours.ircam.cursus1.models import CandidateCursus1
from concours.ircam.cursus1.models import EvaluationCursus1PreJury
from concours.ircam.cursus1.models import EvaluationCursus1Jury


class CandidateCursus1Admin(CandidateAdmin):    
    list_display  = ('nom_','prenom_','work1','work2')
    
    fieldsets = (
        ('Etat-civil', {
            'classes': ('wide',),
            'fields': ('composer','passport')                                                
        }),    
        ('Eléments biographiques', {
            'classes': ('wide',),
            'fields': ('curriculum_vitae','professional_experience','prices_and_distinctions','motivation_letter')                                                
        }),
        ('Oeuvres proposées', {
            'classes': ('wide',),
            'fields': ('work1','work2')    
        }),    
    )

class EvaluationCursus1PreJuryAdmin(admin.ModelAdmin):
    list_filter  = ['yes','candidate','jury_member']
    list_display  = ('candidate','jury_member','yes','note','comments')

class EvaluationCursus1JuryAdmin(admin.ModelAdmin):
    pass

# Register common models
from jury.admin import register as register_jury
from concours.admin import register as register_concours
from compositeurs.admin import register as register_compositeurs
from concours.ircam.cursus1 import site
register_jury(site)
register_concours(site)
register_compositeurs(site)


# Register Ircam cursus 1 specific models
site.register(CandidateCursus1,CandidateCursus1Admin)
site.register(EvaluationCursus1PreJury,EvaluationCursus1PreJuryAdmin)
site.register(EvaluationCursus1Jury,EvaluationCursus1JuryAdmin)

