#-*- coding: utf-8 -*- 
from django.db import models
from django.contrib.auth.models import User

class JuryMember(models.Model):
    user        = models.OneToOneField(User)    
    phone       = models.CharField(verbose_name=u"téléphone",max_length=100,blank=True,null=True)
    
    def email(self):
        return self.user.email
    
    def first_name(self):
        return self.user.first_name
    
    def last_name(self):
        return self.user.last_name
    
    def __unicode__(self):
        return self.user.username
    
    class Meta:
        verbose_name         = "membre du jury"
        verbose_name_plural  = "membres du jury"
        

    