#-*- coding: utf-8 -*- 
from django.db import models

class Partner(models.Model):
    name         = models.CharField(verbose_name=u"nom",max_length=200)
    url          = models.CharField(verbose_name=u"url",max_length=200)
    logo         = models.ImageField(verbose_name=u"logo",upload_to="logos",blank=True,null=True)
    presentation = models.TextField(verbose_name=u"présentation",blank=True,null=True)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name  = "partenaire"


    