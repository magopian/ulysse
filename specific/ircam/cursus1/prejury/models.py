#-*- coding: utf-8 -*- 
from django.db import models
from competitions.models import CompetitionStepResults
from competitions.models import CompetitionStepFollowUp
from competitions.models import CandidateJuryAllocation
from competitions.models import CompetitionStep

def get_active_competition_step():
    # Hard-coded (to be improved)
    return CompetitionStep.objects.filter(competition__id=1,url='pre-jury')[0]
    
class CandidateJuryAllocationIrcamCursus1PreJuryManager(models.Manager):
    def get_query_set(self):
        prejury = get_active_competition_step()
        return super(CandidateJuryAllocationIrcamCursus1PreJuryManager, self).get_query_set().filter(step=prejury)
    

class CandidateJuryAllocationIrcamCursus1PreJury(CandidateJuryAllocation):
    
    objects = CandidateJuryAllocationIrcamCursus1PreJuryManager()
    
    class Meta:
        proxy = True
        verbose_name        = u"Affectation candidat / jury (étape : pré-jury)"
        verbose_name_plural = u"Affectations candidat / jury (étape : pré-jury)"


class CompetitionStepFollowUpIrcamCursus1PreJuryManager(models.Manager):
    def get_query_set(self):
        prejury = get_active_competition_step()
        # Get all jury members for this step
        jury_members = []
        for item in CandidateJuryAllocationIrcamCursus1PreJury.objects.all():
            for jury_member in item.jury_members.all():
                if not jury_member in jury_members:
                    jury_members.append(jury_member)
        return super(CompetitionStepFollowUpIrcamCursus1PreJuryManager, self).get_query_set().filter(jury__in=jury_members)


class CompetitionStepFollowUpIrcamCursus1PreJury(CompetitionStepFollowUp):
    
    objects = CompetitionStepFollowUpIrcamCursus1PreJuryManager()
    
    class Meta:
        proxy = True
        verbose_name        = u"Suivi évaluation (pré-jury)"
        verbose_name_plural = u"Suivis évaluation (pré-jury)"

class CompetitionStepResultsIrcamCursus1PreJury(CompetitionStepResults):
    
    class Meta:
        proxy = True
        verbose_name        = u"Résultat évaluation (pré-jury)"
        verbose_name_plural = u"Résultats évaluation (pré-jury)"
        
