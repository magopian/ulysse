#-*- coding: utf-8 -*- 
from django.db import models

class Citizenship(models.Model):
    name  = models.CharField(verbose_name=u"valeur",max_length=200)
        
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name  = u"nationalité"
        
class MediaType(models.Model):    
    extension    = models.CharField(verbose_name="extension",max_length=20)
    description  = models.CharField(verbose_name="description",max_length=200,blank=True,null=True)
    
    def __unicode__(self):
        return "fichier %s" % self.extension
    
    class Meta:
        verbose_name         = u"type de média"
        verbose_name_plural  = u"types de média"
        
class BiographicElementType(models.Model):    
    name         = models.CharField(verbose_name="name",max_length=20)    
    description  = models.CharField(verbose_name="description",max_length=200,blank=True,null=True)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name         = u"type d'élément biographique"
        verbose_name_plural  = u"types d'élément biographiques"