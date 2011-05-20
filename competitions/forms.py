#-*- coding: utf-8 -*-
from copy import deepcopy
from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.auth.models import Group
from django import forms
from django.conf import settings
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe
from competitions.models import JuryMember, CandidateJuryAllocation, Evaluation, EvaluationStatus


class CompetitionAdminAuthenticationForm(AdminAuthenticationForm):
    """
    A custom authentication form used in the competion admin app.

    """
    
    def clean(self):
        # Call base class first
        super(CompetitionAdminAuthenticationForm,self).clean()
        if self._errors: # no need to go further if the form is already invalid
            return

        # Do extra check        
        logged_user = self.user_cache
        check = False
        if logged_user.is_superuser:
            check = True
        else:
            if not hasattr(settings,'COMPETITION_ADMIN_GROUP'):
                raise RuntimeError("You should specify 'COMPETITION_ADMIN_GROUP' in settings")
            competition_admin_group = Group.objects.get_or_create(name=settings.COMPETITION_ADMIN_GROUP)[0]

            jury_member = JuryMember.objects.filter(user=logged_user).exists()

            user_groups = logged_user.groups.all()
            check = competition_admin_group in user_groups or jury_member
        if not check:
            raise forms.ValidationError(_(u"Seuls les administrateurs de concours, les membres du jury et les super-utilisateurs peuvent se connecter au site d'administration des concours"))
        
        

class DynamicForm(forms.Form):
    """
    A custom orm for candidate in competition admin

    """    
    def __init__(self, data=None, *args, **kwargs):
        label= kwargs.pop('fields_dictionary')
        fields_dictionary = kwargs.pop('label')
        super(DynamicForm, self).__init__(data, *args, **kwargs)
        self.label = label
        self.fields_dictionary = fields_dictionary
        self._build_dynamic_fields()
        
    def _build_dynamic_fields(self):
        # Set form fields        
        self.fields["education"] = forms.CharField(widget=forms.Textarea())        
        
        
class Form1(forms.Form):
    # Temporaire (code en dur)
    lastname    = forms.CharField(label=_(u"Last name"))
    firstname   = forms.CharField(label=_(u"First name"))
    birth_date  = forms.CharField(label=_(u"Birth date"))
    citizenship = forms.CharField(label=_(u"Citizenship"))
    address1    = forms.CharField(label=_(u"Address1"))
    address2    = forms.CharField(label=_(u"Address2"))
    zipcode     = forms.CharField(label=_(u"Zip code"))
    country     = forms.CharField(label=_(u"Country"))
    phone1      = forms.CharField(label=_(u"Phone 1"))
    phone2      = forms.CharField(label=_(u"Phone 2"))                                           
                             
    def get_title(self):
        return _(u"Administrative infos")
        
        
                                
class Form2(forms.Form):
    """
    Temporary hard coded form

    """    
    cursus     = forms.CharField(label=_(u"Personal cursus"),widget=forms.Textarea())
    experience = forms.CharField(label=_(u"Profesional experience"),widget=forms.Textarea())
    prices     = forms.CharField(label=_(u"Prices & distinctions"),widget=forms.Textarea())
    motivation = forms.CharField(label=_(u"Motivation letter"),widget=forms.Textarea())
    
    def get_title(self):
        return _(u"Biography")                
                  

     
class Form3(forms.Form):
    """
    Temporary hard coded form
    """    
    field3 = forms.CharField(widget=forms.Textarea())
    
    def as_table(self):
    # Ugly patch (temporary)
        s = ""
        s+=("<tr><th>Titre</th><td>Concerto pour clarinette et orchestre</td></tr>")
        s+=("<tr><th>Audio</th><td><object type=\"application/x-shockwave-flash\" data=\"/static/flash/player_mp3_maxi.swf\" height=\"220\" width=\"180\"><param name=\"movie\" value=\"/static/flash/player_mp3_maxi.swf\" /><param name=\"wmode\" value=\"transparent\" /><param name=\"FlashVars\" value=\"wav=http://ulysse-test.fr/static/media/K622.mp3&amp;showstop=1&amp;showvolume=1&amp;bgcolor1=ffa50b&amp;bgcolor2=d07600\" /> </object> </td></tr>")          
        s+=("<tr><th>Partition</th><td><iframe src=\"http://docs.google.com/viewer?url=http%3A%2F%2Fulysse-test.fr%2Fstatic%2Fmedia%2FK622.pdf&embedded=true\" width=\"600\" height=\"780\" style=\"border: none;\"></iframe></td>")
        return mark_safe(s)
    
    def get_title(self):
        return _(u"Work 1")                

class Form4(forms.Form):
    """
    Temporary hard coded form
    """        
    
    def as_table(self):
    # Ugly patch (temporary)
        s = ""
        s+=("<tr><th>Titre</th><td>Concerto pour piano et orchestre n°21</td></tr>")
        s+=("<tr><th>Audio</th><td><object type=\"application/x-shockwave-flash\" data=\"/static/flash/player_mp3_maxi.swf\" height=\"220\" width=\"180\"><param name=\"movie\" value=\"/static/flash/player_mp3_maxi.swf\" /><param name=\"wmode\" value=\"transparent\" /><param name=\"FlashVars\" value=\"wav=http://ulysse-test.fr/static/media/K622.mp3&amp;showstop=1&amp;showvolume=1&amp;bgcolor1=ffa50b&amp;bgcolor2=d07600\" /> </object> </td></tr>")          
        s+=("<tr><th>Partition</th><td><iframe src=\"http://docs.google.com/viewer?url=http%3A%2F%2Fulysse-test.fr%2Fstatic%2Fmedia%2FK467.pdf&embedded=true\" width=\"600\" height=\"780\" style=\"border: none;\"></iframe></td>")
        return mark_safe(s)
    
    
    def get_title(self):
        return _(u"Work 2")               
                             
class Form5(forms.Form):
    """
    Temporary hard coded form
    """    
    decision = forms.ChoiceField(label="Decision",choices=(('1','Yes'),('2','No')),widget=forms.RadioSelect())
    comments = forms.CharField(widget=forms.Textarea())
    
    def get_title(self):
        return _(u"Evaluation (pre-jury)")               
    
    
class Form6(forms.Form):
    """
    Temporary hard coded form
    """    
    integer  = forms.IntegerField(label="Note")
    comments = forms.CharField(widget=forms.Textarea())
    
    def get_title(self):
        return _(u"Evaluation (jury)")                       
                                                   
        
    
class CandidateJuryAllocationForm(forms.ModelForm):
    class Meta:
        model = CandidateJuryAllocation

    def __init__(self, *args, **kwargs):
        super(CandidateJuryAllocationForm, self).__init__(*args, **kwargs)
        if self.instance.pk: # we can't filter if we're adding
            competition = self.instance.step.competition
            self.fields['jury_members'].queryset = competition.jurymember_set.all()

    def save(self, *args, **kwargs):
        obj = super(CandidateJuryAllocationForm, self).save(*args, **kwargs)
        eval_status = EvaluationStatus.objects.get(name='to process')
        jury_members = self.cleaned_data['jury_members']
        # remove unused Evaluations, for removed jury members
        removed = [jm for jm in obj.jury_members.all() if jm not in jury_members]
        Evaluation.objects.filter(competition_step=obj.step,
                                  candidate=obj.candidate,
                                  jury_member__in=removed).delete()
        # and add Evaluations for the new ones
        for jm in jury_members:
            Evaluation.objects.get_or_create(
                    competition_step=obj.step,
                    candidate=obj.candidate,
                    jury_member=jm,
                    defaults={'status': eval_status})
        return obj
 
class JuryMembersSelection(forms.ModelForm):
    """Select jury members to assign to candidates for a given step"""

    def __init__(self, competition, *args, **kwargs):
        super(JuryMembersSelection, self).__init__(*args, **kwargs)
        self.fields['jury_members'].queryset = competition.jurymember_set.all()

    class Meta:
        fields = ['jury_members']
        model = CandidateJuryAllocation
        widgets = {'jury_members': forms.CheckboxSelectMultiple}
