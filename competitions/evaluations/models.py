#-*- coding: utf-8 -*- 
from django.db import models
from competitions.models import CompetitionStep
from competitions.models import JuryMember
from competitions.models import Candidate

class EvaluationBase(models.Model):
    competition_step   = models.ForeignKey(CompetitionStep,verbose_name=u"étape du concours")
    candidate          = models.ForeignKey(Candidate,verbose_name=u"candidat")
    jury_member        = models.ForeignKey(JuryMember,verbose_name=u"membre du jury")    

    class Meta:
        verbose_name  = u"évaluation"
        
class EvaluationLevel(models.Model):
    note   = models.IntegerField(verbose_name=u"value")
    legend = models.CharField(verbose_name=u"legend",max_length=20)
    
    def __unicode__(self):
        return "%s - %s " % (self.note,self.legend)

class EvaluationYesNoAndNote(EvaluationBase):
    yes      = models.BooleanField(verbose_name="candidat retenu", help_text="cocher cette case si le candidat est retenu")    
    note     = models.IntegerField(verbose_name="note",help_text="note de 1 à 10 (facultative)")    
    comments = models.TextField(verbose_name="commentaires")

    class Meta:
        pass
        
class EvaluationNote(EvaluationBase):    
    note     = models.IntegerField(verbose_name="note",help_text="note de 1 à 10 (facultative)")    
    comments = models.TextField(verbose_name="commentaires")

    class Meta:
        pass
    
class EvaluationYesNo(EvaluationBase):    
    yes      = models.BooleanField(verbose_name="candidat retenu", help_text="cocher cette case si le candidat est retenu")    
    comments = models.TextField(verbose_name="commentaires")

    class Meta:
        pass
    

        
