#-*- coding: utf-8 -*- 
from django.db import models
from compositeurs.models import Composer
from jury.models import JuryMember

class Partner(models.Model):
    name  = models.CharField(verbose_name=u"nom",max_length=200)
    logo  = models.ImageField(verbose_name=u"logo",upload_to="logos",blank=True,null=True)
     
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name  = "partenaire"


class EvaluationModel(models.Model):
    
    class Meta:
        verbose_name         = u"modèle d'évaluation"
        verbose_name_plural  = u"modèle d'évaluation"

class ApplicationForm(models.Model):
    title  = models.CharField(verbose_name=u"name",max_length=200)
    layout = models.TextField(verbose_name=u"contenu",max_length=4000,blank=True,null=True)
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        verbose_name         = u"formulaire de candidature"
        verbose_name_plural  = u"formulaires de candidature"


class Competition(models.Model):
    title            = models.CharField(verbose_name=u"titre",max_length=200)
    subtitle         = models.CharField(verbose_name=u"sous-titre",max_length=200)
    presentation     = models.TextField(verbose_name=u"présentation",help_text=u"texte de présentation du concours",max_length=200)    
    partner          = models.ForeignKey(Partner,verbose_name=u"partenaire")
    application_form = models.OneToOneField(ApplicationForm,verbose_name=u"formulaire de candidature")
    information_date = models.DateField(verbose_name=u"date de publication de l'annonce")
    opening_date     = models.DateField(verbose_name=u"date d'ouverture des candidatures")
    closing_date     = models.DateField(verbose_name=u"date de clôture des candidatures")
    result_date      = models.DateField(verbose_name=u"date de publication des résultats")
    is_published     = models.BooleanField(verbose_name=u"publié",help_text=u"lorsque cette case est cochée, le concours est publié")
    is_open          = models.BooleanField(verbose_name=u"ouvert",help_text=u"lorsque cette case est cochée, les candidatures sont ouvertes")
    is_archived      = models.BooleanField(verbose_name=u"archivé",help_text=u"lorsque cette case est cochée, le concours est archivé")
     
    def __unicode__(self):
        return self.title
    
    class Meta:
        verbose_name         = "concours"
        verbose_name_plural  = "concours"

class CompetitionStep(models.Model):
    competition      = models.ForeignKey(Competition,verbose_name=u"concours")
    name             = models.CharField(verbose_name=u"name",max_length=200)
    evaluation_model = models.ForeignKey(EvaluationModel)
    is_open          = models.BooleanField(verbose_name=u"ouvert",help_text=u"lorsque cette case est cochée, l'étape est ouverte (i.e, les évaluations sont possibles)")
    closing_date     = models.DateField(verbose_name="date de clôture d'étape",help_text=u"date indicative de fin d'étape")
    
    class Meta:
        verbose_name         = u"étape du concours"
        verbose_name_plural  = u"étapes du concours"

class CompetitionNews(models.Model):
    title  = models.CharField(verbose_name=u"titre",max_length=200)
    date   = models.DateField(verbose_name=u"date")
    text   = models.TextField(verbose_name=u"texte",help_text=u"contenu de l'actualité",max_length=200)
    
    class Meta:
        verbose_name         = u"actualité concours"
        verbose_name_plural  = u"actualités concours"
    
class Candidate(models.Model):
    composer    = models.ForeignKey(Composer,verbose_name=u"composer")
    competition = models.ForeignKey(Competition,verbose_name=u"concours")
     
    class Meta:
        verbose_name  = "candidat"
        
class CandidateGroup(models.Model):
    name    = models.CharField(verbose_name=u"name",max_length=200)
    members = models.ManyToManyField(Candidate,verbose_name=u"membres du groupes")
     
    class Meta:
        verbose_name         = "groupe de candidat"
        verbose_name_plural  = "groupes de candidat"

class JuryMemberGroup(models.Model):
    name    = models.CharField(verbose_name=u"name",max_length=200)
    members = models.ManyToManyField(JuryMember,verbose_name=u"membres du groupes")
     
    class Meta:
        verbose_name         = "groupe de membres du jury"
        verbose_name_plural  = "groupes de membres du jury"

class Evaluation(models.Model):
    competition_step   = models.ForeignKey(CompetitionStep,verbose_name=u"étape du concours")
    candidate          = models.ForeignKey(Candidate,verbose_name=u"candidat")
    jury_member        = models.ForeignKey(JuryMember,verbose_name=u"membre du jury")    


    class Meta:
        verbose_name  = u"évaluation"