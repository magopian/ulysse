#-*- coding: utf-8 -*- 
from django.db import models
from jury.models import Jury
from composers.models import AdministrativeDocument
from composers.models import Composer
from composers.models import Work
from partners.models  import Partner
from django.contrib.auth.models import User
from menu import get_nav_button

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
    
    
    def get_menu(self,request):
        nav_buttons = []    
        nav_buttons.append(get_nav_button(request,"infos","Informations"))
        nav_buttons.append(get_nav_button(request,"candidates","Candidats"))
        nav_buttons.append(get_nav_button(request,"jury","Membres du jury"))
        # Add steps dynamically
        for step in self.steps():
            nav_buttons.append(get_nav_button(request,"step/%s" % step.url,"Etape : '%s'" % step.name))        
        return nav_buttons
    
    def steps(self):
        return CompetitionStep.objects.filter(competition=self)
    
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
    url              = models.CharField(verbose_name=u"url",max_length=200)
    order_index      = models.IntegerField(verbose_name=u"index")
    is_open          = models.BooleanField(verbose_name=u"ouvert",help_text=u"lorsque cette case est cochée, l'étape est ouverte (i.e, les évaluations sont possibles)")
    closing_date     = models.DateField(verbose_name="date de clôture d'étape",help_text=u"date indicative de fin d'étape")
    
    def get_jury_members(self):
        jury_members = []
        for item in CandidateJuryAllocation.objects.filter(step=self):
            for jury_member in item.jury_members.all():
                if not jury_member in jury_members:
                    jury_members.append(jury_member)
        return jury_members
    
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
        

class CompetitionStepFollowUp(JuryMember):
    
    def total_(self):
        return u"à implémenter"
    
    def en_attente_(self):
        return u"à implémenter"
    
    def en_cours_(self):
        return u"à implémenter"
    
    def terminees_(self):
        return u"à implémenter"    
    
    
    class Meta:
        proxy = True
        verbose_name        = u"suivi évaluations"
        verbose_name_plural = u"suivis évaluations"
        

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
        
class CandidateJuryAllocation(models.Model):
    composer     = models.ForeignKey(Composer,verbose_name=u"compositeur")
    step         = models.ForeignKey(CompetitionStep,verbose_name=u"étape du concours")
    jury_members = models.ManyToManyField(JuryMember,verbose_name=u"membres du jury")
    
    def nom_(self):
        return self.composer.user.last_name
    
    def prenom_(self):
        return self.composer.user.first_name
    
    def jury_(self):        
        if len(self.jury_members.all())>0:
            return ", ".join(["%s %s" % (member.jury.user.first_name,member.jury.user.last_name) for member in self.jury_members.all()])
        else:
            return u"Aucun membre du jury n'est associé à ce candidat pour cette étape"        
        
    class Meta:
        verbose_name        = "affectation candidat / jury"
        verbose_name_plural = "affectations candidat / jury"

        
class CandidateGroup(models.Model):
    competition = models.ForeignKey(Competition,verbose_name=u"concours")
    name        = models.CharField(verbose_name=u"nom du groupe",max_length=200)
    members     = models.ManyToManyField(Candidate,verbose_name=u"membres du groupes")
     
    class Meta:
        verbose_name         = "groupe de candidat"
        verbose_name_plural  = "groupes de candidat"        
        

class CompetitionStepResults(CandidateJuryAllocation):
    
    def nom_(self):
        return self.composer.user.last_name
    
    def prenom_(self):
        return self.composer.user.first_name
    
    def evaluations_(self):
        return u"synthèse des évaluations par membre du jury (à implémenter)"
    
    class Meta:
        proxy = True
        verbose_name        = u"résultat évaluation"
        verbose_name_plural = u"résultats évaluation"


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
    

        

