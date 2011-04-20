#-*- coding: utf-8 -*- 
from competitions.admin import CandidateAdmin

class CandidateCursus1Admin(CandidateAdmin):    
    list_display  = ('nom_','prenom_','work1','work2')
    
    search_fields= ["composer__user__last_name",]
    
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