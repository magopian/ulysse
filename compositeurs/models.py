#-*- coding: utf-8 -*- 
from django.db import models
from django.contrib.auth.models import User
from reference.models import Citizenship
from reference.models import MediaType
from reference.models import BiographicElementType

class Composer(models.Model):
    user        = models.ForeignKey(User,verbose_name=u"utilisateur",unique=True)
    birth_date  = models.DateField(verbose_name="date de naissance",blank=True,null=True)
    citizenship = models.ForeignKey(Citizenship,verbose_name=u"nationalité",null=True,blank=True)
    address1    = models.CharField(verbose_name=u"adresse (1)",max_length=200)
    address2    = models.CharField(verbose_name=u"adresse (2)",max_length=200,blank=True,null=True)
    zipcode     = models.CharField(verbose_name=u"code postal",max_length=10)
    city        = models.CharField(verbose_name=u"ville",max_length=50)
    country     = models.CharField(verbose_name=u"pays",max_length=100)
    phone1      = models.CharField(verbose_name=u"téléphone (1)",max_length=100,blank=True,null=True)
    phone2      = models.CharField(verbose_name=u"téléphone (2)",max_length=100,blank=True,null=True)
    
    def nom_(self):
        return self.user.last_name
    
    def prenom_(self):
        return self.user.first_name
        
    def __unicode__(self):
        return "%s, %s" % (self.user.last_name,self.user.first_name)
    
    class Meta:
        verbose_name  = "compositeur"

        

class Work(models.Model):
    composer = models.ForeignKey(Composer,verbose_name=u"compositeur")
    title    = models.CharField(verbose_name="titre",max_length=400)
    score    = models.URLField(verbose_name="partition",max_length=400,help_text="Lien (url) vers la partition")    
    audio    = models.URLField(verbose_name="audio",max_length=400,help_text="Lien (url) vers le fichier audio")    
    notes    = models.TextField(verbose_name="notes",max_length=4000,blank=True,null=True)        
    
    def __unicode__(self):
        return "%s %s : %s" % (self.composer.user.first_name,self.composer.user.last_name,self.title)
    
    class Meta:
        verbose_name  = u"oeuvre"
        
class AdministrativeDocument(models.Model):
    composer = models.ForeignKey(Composer,verbose_name=u"compositeur")
    name     = models.CharField(verbose_name="nom",max_length=200)    
    document = models.FileField(verbose_name="fichier",max_length=200,upload_to="composers")    
    
    def __unicode__(self):
        return "%s %s : %s" % (self.composer.user.first_name,self.composer.user.last_name,self.name)
    
    class Meta:
        verbose_name         = u"document administratif"
        verbose_name_plural  = u"documents administratifs"
        
class BiographicElement(models.Model):
    composer = models.ForeignKey(Composer,verbose_name=u"compositeur")
    type     = models.ForeignKey(BiographicElementType,verbose_name="type")
    text     = models.TextField(verbose_name="texte",max_length=200)
         
    
    class Meta:
        verbose_name         = u"élément biographique"
        verbose_name_plural  = u"éléments biographiques"