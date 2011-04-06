##-*- coding: utf-8 -*- 
from django.db import models
from compositeurs.models import Work
import concours

class ProjectTopicArea(models.Model):
    name = models.CharField(verbose_name=u"name",max_length="100")
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name       = "topic area"
        verbose_name_plural= "topic areas"

class CandidateResidence(concours.models.Candidate):
    short_biography   = models.TextField(max_length="4000",verbose_name=u"short biography")
    curriculum_vitae  = models.TextField(max_length="4000",verbose_name=u"cv")    
    motivation_letter = models.TextField(max_length="4000",verbose_name=u"motivation letter")
    # Project
    title  = models.CharField(max_length="200",verbose_name=u"project title")
    additional_authors = models.CharField(max_length="500",verbose_name=u"additional authors",blank=True,null=True)
    topic_areas = models.ManyToManyField(ProjectTopicArea,verbose_name="topic areas")
    state_of_the_art_description = models.TextField(max_length="4000",verbose_name=u"state-of-the-art description")
    project_description = models.TextField(max_length="4000",verbose_name=u"project description")
    relevance_to_ircam_research = models.TextField(max_length="4000",verbose_name="relevance to Ircam research")
    work_plan = models.TextField(max_length="4000",verbose_name="work plan")
    multimedia_sample_1       = models.ForeignKey(Work,verbose_name="multimedia sample (1)",related_name="multimedia_sample1")
    multimedia_sample_1_notes = models.TextField(verbose_name="multimedia sample (1) : notes",null=True,blank=True)
    multimedia_sample_2       = models.ForeignKey(Work,verbose_name="multimedia sample (2)",related_name="multimedia_sample2")
    multimedia_sample_2_notes = models.TextField(verbose_name="multimedia sample (2) : notes",null=True,blank=True)
    
    class Meta:        
        app_label           = "concours"
        verbose_name        = "candidat"        
    
    
class EvaluationLevel(models.Model):
    note   = models.IntegerField(verbose_name=u"value")
    legend = models.CharField(verbose_name=u"legend",max_length=20)
    
    def __unicode__(self):
        return "%s - %s " % (self.note,self.legend)

class EvaluationResidenceJury(concours.models.Evaluation):
    technical_novelty     = models.ForeignKey(EvaluationLevel,related_name="technical_novelty")
    artistic_novelty      = models.ForeignKey(EvaluationLevel,related_name="artistic_novelty")
    artistic_quality      = models.ForeignKey(EvaluationLevel,related_name="artistic_quality")
    research_relevance    = models.ForeignKey(EvaluationLevel,related_name="research_relevance")
    prior_experience      = models.ForeignKey(EvaluationLevel,related_name="prior_experience")
    practicality          = models.ForeignKey(EvaluationLevel,related_name="practicality")
    comments_to_candidate = models.TextField(verbose_name="comments (to candidate)")
    comments_internal     = models.TextField(verbose_name="comments (internal)")

    class Meta:
        app_label            = "concours"
        verbose_name         = u"évaluation étape 'jury'"
        verbose_name_plural  = u"évaluations étape 'jury'"
        
class EvaluationResidencePostJury(concours.models.Evaluation):    
    yes      = models.BooleanField(verbose_name="candidat retenu", help_text="cocher cette case si le candidat est retenu")    
    comments = models.TextField(verbose_name="commentaires")

    class Meta:
        app_label            = "concours"
        verbose_name         = u"évaluation étape 'post-jury'"
        verbose_name_plural  = u"évaluations étape 'post-jury'"