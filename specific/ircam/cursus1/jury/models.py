#-*- coding: utf-8 -*- 
from django.db import models
from competitions.models import CompetitionStepResults
from competitions.models import CompetitionStepFollowUp
from competitions.models import CandidateJuryAllocation
from competitions.models import CompetitionStep

def get_active_competition_step():
    # Hard-coded (to be improved)
    return CompetitionStep.objects.filter(competition__id=1,url='jury')[0]

class CandidateJuryAllocationIrcamCursus1JuryManager(models.Manager):
    def get_query_set(self):
        jury = CompetitionStep.objects.filter(competition__id=1,url='jury')
        return super(CandidateJuryAllocationIrcamCursus1JuryManager, self).get_query_set().filter(step=jury)

class CandidateJuryAllocationIrcamCursus1Jury(CandidateJuryAllocation):
    
    objects = CandidateJuryAllocationIrcamCursus1JuryManager()
    
    class Meta:
        proxy = True
        verbose_name        = u"Affectation candidat / jury (étape : jury)"
        verbose_name_plural = u"Affectations candidat / jury (étape : jury)"
        

class CompetitionStepResultsIrcamCursus1Jury(CompetitionStepResults):
    
    class Meta:
        proxy = True
        verbose_name        = u"Résultat évaluation (jury)"
        verbose_name_plural = u"Résultats évaluation (jury)"
        
        
class CompetitionStepFollowUpIrcamCursus1JuryManager(models.Manager):
    def get_query_set(self):        
        # Get all jury members for this step
        jury_members = []
        for item in CandidateJuryAllocationIrcamCursus1Jury.objects.all():
            for jury_member in item.jury_members.all():
                if not jury_member in jury_members:
                    jury_members.append(jury_member)
        return super(CompetitionStepFollowUpIrcamCursus1JuryManager, self).get_query_set().filter(jury__in=jury_members)

        
class CompetitionStepFollowUpIrcamCursus1Jury(CompetitionStepFollowUp):
    
    objects = CompetitionStepFollowUpIrcamCursus1JuryManager()
    
    class Meta:
        proxy = True
        verbose_name        = u"Suivi évaluation (jury)"
        verbose_name_plural = u"Suivis évaluation (jury)"