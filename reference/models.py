#-*- coding: utf-8 -*- 
from django.db import models

class Citizenship(models.Model):
    name  = models.CharField(verbose_name=u"nom",max_length=200)
        
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name  = u"nationalité"