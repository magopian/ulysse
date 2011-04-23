#-*- coding: utf-8 -*-
from django.db import models
from composers.models import Work
from composers.models import AdministrativeDocument
from competitions.models import Candidate

class CandidateCursus1(Candidate):
    curriculum_vitae        = models.TextField(max_length="4000",verbose_name=u"formation & diplômes")
    professional_experience = models.TextField(max_length="4000",verbose_name=u"expérience professionnelle",blank=True,null=True)
    prices_and_distinctions = models.TextField(max_length="4000",verbose_name=u"distinctions obtenues",blank=True,null=True)
    motivation_letter       = models.TextField(max_length="4000",verbose_name=u"lettre de motivation")
    work1    = models.ForeignKey(Work,verbose_name=u"oeuvre 1",related_name="work1")    
    work2    = models.ForeignKey(Work,verbose_name=u"oeuvre 2",related_name="work2",)
    passport = models.ForeignKey(AdministrativeDocument,verbose_name=u"pièce d'identité",related_name="passport")
    
    class Meta:        
        verbose_name        = u"candidat Cursus 1"
        verbose_name_plural = u"candidats Cursus 1"
        