#-*- coding: utf-8 -*- 
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_delete
from composers.models import Composer
from composers.models import WorkBase, DocumentBase, TextElementBase
from partners.models  import Partner
from django.contrib.auth.models import User, Group, Permission
from django.utils.translation import ugettext as _

def get_nav_button(request,url,label,children=None):        
    is_selected = request.path.startswith("/admin/%s" % url)
    result = {'url':url,'label':label,'is_selected':is_selected }
    if children:
        result["children"] = children
    return result

class Competition(models.Model):
    url                  = models.CharField(max_length=200,unique=True)
    title                = models.CharField(max_length=200)
    subtitle             = models.CharField(verbose_name=_(u"sub title"),max_length=200)
    presentation         = models.TextField(verbose_name=_(u"summary"),help_text=_(u"competition summary"),max_length=200)    
    managing_partner     = models.ForeignKey(Partner,verbose_name=_(u"managing partner"))
    additional_partners  = models.ManyToManyField(Partner,verbose_name=_(u"partners"),help_text=_(u"additional partners"),related_name="additional_partners",blank=True)    
    information_date = models.DateField()
    opening_date     = models.DateField()
    closing_date     = models.DateField()
    result_date      = models.DateField()
    is_published     = models.BooleanField(verbose_name=_(u"is published"),help_text=u"lorsque cette case est cochée, le concours est publié")
    is_open          = models.BooleanField(verbose_name=_(u"is open"),help_text=u"lorsque cette case est cochée, les candidatures sont ouvertes")
    is_archived      = models.BooleanField(verbose_name=_(u"is archived"),help_text=u"lorsque cette case est cochée, le concours est archivé")
     
    def __unicode__(self):
        return self.title        
    
    def get_menu(self,request):
        from competitions import admin_site
        nav_buttons = []
        if admin_site.is_competition_admin(request) or request.user.is_superuser:
            nav_buttons.append(get_nav_button(request,"infos/",_(u"Informations")))
            nav_buttons.append(get_nav_button(request,"news/",_(u"News")))
            nav_buttons.append(get_nav_button(request,"candidates/",_(u"Candidates")))
            nav_buttons.append(get_nav_button(request,"jury_members/",_(u"Jury member")))
            # Add steps dynamically
            for step in self.steps():
                step_button = get_nav_button(request,"step/%s" % step.url,_(u"'%s' step" % step.name))
                children = []
                children.append(get_nav_button(request,"step/%s/importation/" % step.url,_(u"1 - Import candidates")))
                children.append(get_nav_button(request,"step/%s/allocations/" % step.url,_(u"2 - Manage candidates/jury")))
                children.append(get_nav_button(request,"step/%s/notifications/" % step.url,_(u"3 - Notify jury members")))
                children.append(get_nav_button(request,"step/%s/evaluations/" % step.url,_(u"4 - Follow evaluations")))
                children.append(get_nav_button(request,"step/%s/results/" % step.url,_(u"5 - Follow results")))
                step_button["children"] = children            
                nav_buttons.append(step_button)        
        if admin_site.is_jury_member(request): # jury members only have a limited admin
            nav_buttons.append(get_nav_button(request, "evaluate/", _(u"To evaluate")))
        return nav_buttons
    
    def steps(self):
        return CompetitionStep.objects.filter(competition=self).order_by("order_index")
        
    def managers(self):
        return CompetitionManager.objects.filter(competition=self)
    
    class Meta:
        verbose_name         = "concours"
        verbose_name_plural  = "concours"        
        
class CompetitionManager(models.Model):
    user         = models.ForeignKey(User) 
    competition  = models.ForeignKey(Competition)
        
    class Meta:
        verbose_name         = "gestionnaire de concours"
        verbose_name_plural  = "gestionnaires de concours"
        unique_together      = ('user','competition')


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
        verbose_name         = _(u"competition step")
        verbose_name_plural  = _(u"competition steps")

class CompetitionNews(models.Model):
    competition = models.ForeignKey(Competition,verbose_name=_(u"competition"))
    title       = models.CharField(verbose_name=_(u"title"),max_length=200)
    date        = models.DateField(verbose_name=_(u"date"))
    text        = models.TextField(verbose_name=_(u"text"),help_text=(u"news content"),max_length=200)
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        verbose_name         = _(u"competition news")
        verbose_name_plural  = _(u"competition news")
    
                
class JuryMemberGroup(models.Model):
    competition = models.ForeignKey(Competition,verbose_name=u"concours")
    name        = models.CharField(verbose_name=u"nom",max_length=200)    
     
    class Meta:
        verbose_name         = _(u"jury member group")
        verbose_name_plural  = _(u"jury member groups")
        
class JuryMember(models.Model):
    user         = models.ForeignKey(User,unique=True)    
    phone        = models.CharField(max_length=100,blank=True,null=True)    
    competitions = models.ManyToManyField(Competition,blank=True,null=True)
    groups       = models.ManyToManyField(JuryMemberGroup,blank=True,null=True)
    
    class Meta:        
        verbose_name         = _(u"jury member")
        verbose_name_plural  = _(u"jury members")        

    def __unicode__(self):
        return "%s, %s" % (self.user.last_name,self.user.first_name)

    def save(self, *args, **kwargs):
        # make sure the user is also added to the "jury-members" group
        if not hasattr(settings,'JURY_MEMBER_GROUP'):
            raise RuntimeError("Please specify 'JURY_MEMBER_GROUP' in settings")
        jury_member_group, created = Group.objects.get_or_create(name=settings.JURY_MEMBER_GROUP)
        if created: # group didn't exist before, add all needed permissions
            permissions = Permission.objects.filter(
                    Q(codename__endswith='evaluation') |
                    Q(codename__endswith='evaluationnote') |
                    Q(codename__exact='change_candidatetoevaluate'))
            jury_member_group.permissions.add(*permissions)
        self.user.groups.add(jury_member_group)
        super(JuryMember, self).save(*args, **kwargs)

def on_jury_member_delete(sender, instance, **kwargs):
    """Remove the 'jury-members' group on the user of a deleted JuryMember.

    A signal is used here instead of the JuryMember.delete() method as it would
    not be called on bulk deletion otherwise (select multiple JuryMembers in
    the admin and use the "delete" action)

    """
    jm_group = Group.objects.get(name=settings.JURY_MEMBER_GROUP)
    instance.user.groups.remove(jm_group)
pre_delete.connect(on_jury_member_delete, sender=JuryMember)
     

class CompetitionStepFollowUp(JuryMember):       
    
    class Meta:
        proxy = True
        verbose_name        = u"suivi évaluations"
        verbose_name_plural = u"suivis évaluations"
        
class CandidateGroup(models.Model):
    competition = models.ForeignKey(Competition,verbose_name=u"concours")
    name        = models.CharField(verbose_name=u"nom du groupe",max_length=200)    
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name         = _(u"candidate group")
        verbose_name_plural  = _(u"candidate groups") 
        

class Candidate(models.Model):    
    composer      = models.ForeignKey(Composer,verbose_name=u"compositeur")
    competition   = models.ForeignKey(Competition,verbose_name=u"concours")
    groups        = models.ManyToManyField(CandidateGroup)
    is_valid      = models.BooleanField()
     
    def __unicode__(self):
        return "%s, %s" % (self.composer.user.last_name,self.composer.user.first_name)
            
        
    def last_name(self):
        return self.composer.user.last_name    
    
    def first_name(self):
        return self.composer.user.first_name
    
    class Meta:
        verbose_name  = _(u"candidate")
        unique_together = (('composer', 'competition'),)

class CandidateToEvaluate(Candidate):
    class Meta:
        proxy = True
        
class CandidateWork(WorkBase):
    candidate = models.ForeignKey(Candidate)
        
class CandidateDocument(DocumentBase):
    candidate = models.ForeignKey(Candidate)    
    
class CandidateTextElement(TextElementBase):
    candidate    = models.ForeignKey(Candidate)    

class CandidateJuryAllocation(models.Model):
    candidate    = models.ForeignKey(Candidate)
    step         = models.ForeignKey(CompetitionStep,verbose_name=_(u"competition step"))
    jury_members = models.ManyToManyField(JuryMember,verbose_name=_(u"jury members"))        
    
    
    def jury_(self):        
        if len(self.jury_members.all())>0:
            return ", ".join(["%s %s" % (member.jury.user.first_name,member.jury.user.last_name) for member in self.jury_members.all()])
        else:
            return u"Aucun membre du jury n'est associé à ce candidat pour cette étape"        
        
    class Meta:
        verbose_name        = _(u"candidat / jury allocation")
        
class NotificationStatus(models.Model):
    name  = models.CharField(max_length="50")
    
    class Meta:
        verbose_name         = _(u"notification status")        

class CandidateJuryAllocationNotification(models.Model):
    allocation = models.ForeignKey(CandidateJuryAllocation)
    status     = models.ForeignKey(NotificationStatus)        
        
    class Meta:
        verbose_name         = _(u"candidat / jury allocation notification")
        verbose_name_plural  = _(u"candidat / jury allocation notifications")                


class CompetitionStepResults(CandidateJuryAllocation):
    
    def nom_(self):
        return self.composer.user.last_name
    
    def prenom_(self):
        return self.composer.user.first_name
    
    def evaluations_(self):
        return u"synthèse des évaluations par membre du jury (à implémenter)"
    
    class Meta:
        proxy = True
        verbose_name        = _(u"evaluation result")        


class EvaluationNoteType(models.Model):    
    type = models.CharField(verbose_name=u"type",max_length=20)
    
    def __unicode__(self):
        return "%s" % (self.type)

        
class EvaluationStatus(models.Model):    
    name = models.CharField(verbose_name=u"name",max_length=50)    
    url  = models.CharField(max_length=50)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name        = u"evaluation status"
        verbose_name_plural = u"evaluation status"

class Evaluation(models.Model):
    competition_step   = models.ForeignKey(CompetitionStep,verbose_name=_(u"competition step"))
    candidate          = models.ForeignKey(Candidate,verbose_name=_(u"candidate"))
    jury_member        = models.ForeignKey(JuryMember,verbose_name=_(u"jury member"))    
    status             = models.ForeignKey(EvaluationStatus)

    class Meta:
        verbose_name    = _(u"evaluation")
        unique_together = ('competition_step','candidate','jury_member')
        

        

class EvaluationNote(models.Model):
    evaluation = models.ForeignKey(Evaluation)
    name       = models.CharField(max_length=50)
    type       = models.ForeignKey(EvaluationNoteType,verbose_name=_(u"note type"))
    value      = models.CharField(verbose_name=_(u"note value"),max_length=200)    
    
