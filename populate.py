#-*- coding: utf-8 -*- 
from reference.models import Citizenship
from django.contrib.auth.models import User
from compositeurs.models import Composer
from concours.models import Partner
from concours.models import Competition
from concours.models import ApplicationForm
from concours.models import Candidate
from jury.models import JuryMember
from django.template.defaultfilters import slugify
import datetime
import random


def create_concours_ircam_1(partner):    
    af = ApplicationForm()
    af.title = "Formulaire de candidature Ircam Cursus 1"
    af.save()
    c = Competition()
    c.title    = "Ircam-Cursus 1"
    c.subtitle = "Formation pratique à l'informatique musicale"
    c.presentation    = u"La formation pratique permet à une quinzaine de compositeurs agés de moins de 35 ans de s'initier et de réfléchir aux problématiques théoriques et compositionnelles de l'informatique musicale"
    c.partner         = partner    
    c.application_form = af
    c.information_date = datetime.datetime(2011,5,1)
    c.opening_date     = datetime.datetime(2011,7,1)
    c.closing_date     = datetime.datetime(2011,10,31)
    c.result_date      = datetime.datetime(2011,12,15)        
    c.is_published     = False
    c.is_open          = False
    c.is_archived      = False
    c.save()
    # Creation candidats (on prend 7 compositeurs au hasard)
    random.seed()
    composers = random.sample(Composer.objects.all(),7)
    for composer in composers:
        cd = Candidate()
        cd.composer    = composer
        cd.competition = c
        cd.save()

def create_concours_rm(partner):        
    af = ApplicationForm()
    af.title = "Formulaire de candidature Résidence Recherche Musicale"
    af.save()
    c = Competition()
    c.title    = "Résidence de recherche musicale"
    c.subtitle = "Accueil de chercheurs au sein de l'Ircam"
    c.presentation    = u"Ce programme s'adresse à des chercheurs et des artistes, jeunes professionnels et étudiants, qui souhaitent poursuivre leur projet de recherche au sein de l'Ircam"
    c.partner         = partner    
    c.application_form = af
    c.information_date = datetime.datetime(2011,5,1)
    c.opening_date     = datetime.datetime(2011,7,1)
    c.closing_date     = datetime.datetime(2011,9,30)
    c.result_date     = datetime.datetime(2011,11,30)        
    c.is_published     = False
    c.is_open          = False
    c.is_archived      = False
    c.save()
    # Creation candidats (on prend 5 compositeurs au hasard)    
    random.seed()
    composers = random.sample(Composer.objects.all(),5)
    for composer in composers:
        cd = Candidate()
        cd.composer    = composer
        cd.competition = c
        cd.save()

# Populate database with sample data
def populate_database():
    # Création partenaires
    ircam     = Partner.objects.get_or_create(name="IRCAM")[0]
    royaumont = Partner.objects.get_or_create(name="Royaumont")[0]
    # Création compositeurs
    Composer.objects.all().delete()
    composers = [u"Robert Schumann (allemande)",u"Franz Schubert (autrichienne)",u"Franz Liszt (hongroise)",u"César Franck (belge)"]
    composers += [u"Gabriel Fauré (française)", u"Maurice Ravel (française)", u"Claude Debussy (française)", u"Arnold Schoenberg (autrichienne)", u"Alban Berg (autrichienne)", u"Anton Webern (autrichienne)"]
    for composer in composers:
        print composer
        p1 = composer.find("(")        
        p2 = composer.find(")")        
        citizenship = composer[p1+1:p2]
        fullname    = composer[:p1-1]        
        tokens    = fullname.split(" ")
        firstname = tokens[0]
        lastname  = tokens[1]
        # Create user        
        username = "%s.%s@gmail.com" % (slugify(firstname),slugify(lastname))
        User.objects.filter(username=username).delete()  # Delete existing if any        
        user = User()
        user.first_name = firstname
        user.last_name  = lastname
        user.username   = username
        user.email      = username        
        user.save()
        # Create composer for this user
        Composer.objects.filter(user=user).delete()  # Delete existing if any        
        c = Composer()        
        c.user        = user
        c.birth_date  = datetime.datetime(1981,1,1)
        c.citizenship = Citizenship.objects.get_or_create(name=citizenship)[0]
        c.address1    = "12 rue %s" % fullname        
        c.zipcode     = "75001"
        c.city        = "Paris"
        c.country     = "France"
        c.phone       = "01.42.44.44.44"
        c.save()        
    # Création membres du jury
    jury_members =["George Washington","Thomas Jefferson","James Monroe","Andrew Jackson","John Tyler","James Buchanan","Abraham Lincoln","Benjamin Harrison","Theodore Roosevelt","Adolphe Tiers","Félix Faure","Paul Deschanel","Paul Doumer"]
    for jury_member in jury_members:
        print jury_member
        tokens    = jury_member.split(" ")
        firstname = tokens[0]
        lastname  = tokens[1]
        # Create user        
        username = "%s.%s@gmail.com" % (slugify(firstname),slugify(lastname))
        User.objects.filter(username=username).delete()  # Delete existing if any        
        user = User()
        user.first_name = firstname
        user.last_name  = lastname
        user.username   = username
        user.email      = username        
        user.save()
        # Create jury member
        j = JuryMember()
        j.user  = user
        j.phone = "01.45.25.45.84"
        j.save()
    # Création concours Ircam 
    ApplicationForm.objects.all().delete()
    Competition.objects.all().delete()
    create_concours_ircam_1(ircam)
    create_concours_rm(royaumont)        
    # Done
    print "Done !"