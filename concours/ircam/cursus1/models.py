#-*- coding: utf-8 -*- 
from django.db import models
from compositeurs.models import AdministrativeDocument
from compositeurs.models import Work
import concours

                
class CandidateCursus1(concours.models.Candidate):
    curriculum_vitae        = models.TextField(max_length="4000",verbose_name=u"formation & diplômes")
    professional_experience = models.TextField(max_length="4000",verbose_name=u"expérience professionnelle",blank=True,null=True)
    prices_and_distinctions = models.TextField(max_length="4000",verbose_name=u"distinctions obtenues",blank=True,null=True)
    motivation_letter       = models.TextField(max_length="4000",verbose_name=u"lettre de motivation")
    work1    = models.ForeignKey(Work,verbose_name=u"oeuvre 1",related_name="work1")    
    work2    = models.ForeignKey(Work,verbose_name=u"oeuvre 2",related_name="work2",)
    passport = models.ForeignKey(AdministrativeDocument,verbose_name=u"pièce d'identité",related_name="passport")
    
    class Meta:        
        app_label     = "concours"        
        verbose_name  = "candidat"        
    
class EvaluationCursus1PreJury(concours.models.Evaluation):
    yes      = models.BooleanField(verbose_name="candidat retenu", help_text="cocher cette case si le candidat est retenu")    
    note     = models.IntegerField(verbose_name="note",help_text="note de 1 à 10 (facultative)")
    yes      = models.BooleanField(verbose_name="candidat retenu", help_text="cocher cette case si le candidat est retenu")    
    comments = models.TextField(verbose_name="commentaires")

    class Meta:
        app_label            = "concours"
        verbose_name         = u"évaluation étape 'pré-jury'"
        verbose_name_plural  = u"évaluations étape 'pré-jury'"
        
class EvaluationCursus1Jury(concours.models.Evaluation):    
    note     = models.IntegerField(verbose_name="note",help_text="note de 1 à 10 (facultative)")    
    comments = models.TextField(verbose_name="commentaires")

    class Meta:
        app_label            = "concours"
        verbose_name         = u"évaluation étape 'jury'"
        verbose_name_plural  = u"évaluations étape 'jury'"