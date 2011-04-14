#-*- coding: utf-8 -*- 
from django.db import models
from jury.models import Jury
from composers.models import Composer
from partners.models  import Partner
from django.contrib.auth.models import User
from competitions import get_active_competition


class Competition(models.Model):
    url                  = models.CharField(verbose_name=u"url",max_length=200,unique=True)
    title                = models.CharField(verbose_name=u"titre",max_length=200)
    subtitle             = models.CharField(verbose_name=u"sous-titre",max_length=200)
    presentation         = models.TextField(verbose_name=u"présentation",help_text=u"texte de présentation du concours",max_length=200)    
    managing_partner     = models.ForeignKey(Partner,verbose_name=u"organisateur")
    additional_partners  = models.ManyToManyField(Partner,verbose_name=u"partenaires",related_name="additional_partners",blank=True)    
    information_date = models.DateField(verbose_name=u"Publication annonce")
    opening_date     = models.DateField(verbose_name=u"Ouverture candidatures")
    closing_date     = models.DateField(verbose_name=u"Clôture candidatures")
    result_date      = models.DateField(verbose_name=u"Publication résultats")
    is_published     = models.BooleanField(verbose_name=u"publié",help_text=u"lorsque cette case est cochée, le concours est publié")
    is_open          = models.BooleanField(verbose_name=u"ouvert",help_text=u"lorsque cette case est cochée, les candidatures sont ouvertes")
    is_archived      = models.BooleanField(verbose_name=u"archivé",help_text=u"lorsque cette case est cochée, le concours est archivé")
     
    def __unicode__(self):
        return self.title
    
    class Meta:
        verbose_name         = "concours"
        verbose_name_plural  = "concours"
        
class CompetitionManager(models.Model):
    user                 = models.ForeignKey(User,unique=True)    
    managed_competitions = models.ManyToManyField(Competition)
        
    class Meta:
        verbose_name         = "gestionnaire de concours"
        verbose_name_plural  = "gestionnaires de concours"


class CompetitionStep(models.Model):
    competition      = models.ForeignKey(Competition,verbose_name=u"concours")
    name             = models.CharField(verbose_name=u"nom",max_length=200)    
    is_open          = models.BooleanField(verbose_name=u"ouvert",help_text=u"lorsque cette case est cochée, l'étape est ouverte (i.e, les évaluations sont possibles)")
    closing_date     = models.DateField(verbose_name="date de clôture d'étape",help_text=u"date indicative de fin d'étape")
    
    def __unicode__(self):
        return "%s : %s" % (self.competition.title,self.name)
    
    class Meta:
        verbose_name         = u"étape du concours"
        verbose_name_plural  = u"étapes du concours"

class CompetitionNews(models.Model):
    competition = models.ForeignKey(Competition,verbose_name=u"concours")
    title       = models.CharField(verbose_name=u"titre",max_length=200)
    date        = models.DateField(verbose_name=u"date")
    text        = models.TextField(verbose_name=u"texte",help_text=u"contenu de l'actualité",max_length=200)
    
    class Meta:
        verbose_name         = u"actualité"
        verbose_name_plural  = u"actualités"
    
    
class Candidate(models.Model):    
    composer    = models.ForeignKey(Composer,verbose_name=u"compositeur")
    competition = models.ForeignKey(Competition,verbose_name=u"concours")
     
    def __unicode__(self):
        return "%s, %s" % (self.composer.user.last_name,self.composer.user.first_name)
        
    def nom_(self):
        return self.composer.user.last_name
    
    def prenom_(self):
        return self.composer.user.first_name
    
    class Meta:
        verbose_name  = "candidat"
        unique_together = (('composer', 'competition'),)
        

        
    
class CandidateGroup(models.Model):
    competition = models.ForeignKey(Competition,verbose_name=u"concours")
    name        = models.CharField(verbose_name=u"nom du groupe",max_length=200)
    members     = models.ManyToManyField(Candidate,verbose_name=u"membres du groupes")
     
    class Meta:
        verbose_name         = "groupe de candidat"
        verbose_name_plural  = "groupes de candidat"

class JuryMember(models.Model):
    jury        = models.ForeignKey(Jury,verbose_name=u"jury")
    competition = models.ForeignKey(Competition,verbose_name=u"concours")
    
    def __unicode__(self):
        return "%s, %s" % (self.jury.user.last_name,self.jury.user.first_name)
     
    class Meta:
        verbose_name         = "membre du jury"
        verbose_name_plural  = "membres du jury"
        unique_together = (('jury', 'competition'),)

class JuryMemberGroup(models.Model):
    competition = models.ForeignKey(Competition,verbose_name=u"concours")
    name    = models.CharField(verbose_name=u"nom",max_length=200)
    members = models.ManyToManyField(JuryMember,verbose_name=u"membres du groupe")
     
    class Meta:
        verbose_name         = "groupe de membres du jury"
        verbose_name_plural  = "groupes de membres du jury"

class Evaluation(models.Model):
    competition_step   = models.ForeignKey(CompetitionStep,verbose_name=u"étape du concours")
    candidate          = models.ForeignKey(Candidate,verbose_name=u"candidat")
    jury_member        = models.ForeignKey(JuryMember,verbose_name=u"membre du jury")    

    class Meta:
        verbose_name  = u"évaluation"
        
