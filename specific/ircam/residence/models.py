#-*- coding: utf-8 -*- 

from competitions.models import EvaluationBase

class EvaluationResidence(EvaluationBase):
    technical_novelty     = models.ForeignKey(EvaluationLevel,related_name="technical_novelty")
    artistic_novelty      = models.ForeignKey(EvaluationLevel,related_name="artistic_novelty")
    artistic_quality      = models.ForeignKey(EvaluationLevel,related_name="artistic_quality")
    research_relevance    = models.ForeignKey(EvaluationLevel,related_name="research_relevance")
    prior_experience      = models.ForeignKey(EvaluationLevel,related_name="prior_experience")
    practicality          = models.ForeignKey(EvaluationLevel,related_name="practicality")
    comments_to_candidate = models.TextField(verbose_name="comments (to candidate)")
    comments_internal     = models.TextField(verbose_name="comments (internal)")

    class Meta:
        pass