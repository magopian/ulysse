#-*- coding: utf-8 -*- 
from django.db import models
from django.contrib.auth.models import User
from reference.models import Citizenship

class Composer(models.Model):
    user        = models.OneToOneField(User)
    birth_date  = models.DateField(verbose_name="date de naissance",blank=True,null=True)
    citizenship = models.ForeignKey(Citizenship,verbose_name=u"nationalité")
    address1    = models.CharField(verbose_name=u"adresse (1)",max_length=200)
    address2    = models.CharField(verbose_name=u"adresse (2)",max_length=200,blank=True,null=True)
    zipcode     = models.CharField(verbose_name=u"code postal",max_length=10)
    city        = models.CharField(verbose_name=u"ville",max_length=50)
    country     = models.CharField(verbose_name=u"pays",max_length=100)
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
        verbose_name  = "compositeur"
        
class Media(models.Model):
    composer = models.ForeignKey(Composer,verbose_name=u"compositeur")
    title = models.CharField(verbose_name="titre",max_length=200)
    file  = models.FileField(verbose_name="fichier",upload_to="medias")
    
    def __unicode__(self):
        return self.file
    
    class Meta:
        verbose_name  = u"média"
        
class BiographicElement(models.Model):
    composer = models.ForeignKey(Composer,verbose_name=u"compositeur")
    title    = models.CharField(verbose_name="titre",max_length=200)
    text     = models.TextField(verbose_name="texte",max_length=200)
     
    def __unicode__(self):
        return self.title
    
    class Meta:
        verbose_name         = u"élément biographique"
        verbose_name_plural  = u"éléments biographiques"