#-*- coding: utf-8 -*- 
from django.contrib.admin.forms import AdminAuthenticationForm
from django import forms
import settings
from django.utils.translation import ugettext as _

class CompetitionAdminAuthenticationForm(AdminAuthenticationForm):
    """
    A custom authentication form used in the competion admin app.

    """
    
    def clean(self):
        # Call base class first
        super(CompetitionAdminAuthenticationForm,self).clean()
        # Do extra check        
        logged_user = self.user_cache
        check = False
        if logged_user.is_superuser:
            check = True
        else:
            if not hasattr(settings,'COMPETITION_ADMIN_GROUP'):
                raise RuntimeError("You should specify 'COMPETITION_ADMIN_GROUP' in settings")
            competition_admin_group = settings.COMPETITION_ADMIN_GROUP            
            if competition_admin_group in [group.name for group in logged_user.groups.all()]:
                check = True
        if not check:
            raise forms.ValidationError(u"Seuls les administrateurs de concours et les super-utilisateurs peuvent se connecter au site d'administration des concours")
        
        
class CandidateAdminForm(forms.ModelForm):
    """
    A custom model form for candidate in competition admin

    """
    # TO DO : rendre générique cette partie (hard-coded pour l'instant)   
    education    = forms.CharField(widget=forms.Textarea())
    experience   = forms.CharField(label=_("Professional experience"),widget=forms.Textarea())
    distinctions = forms.CharField(label=_("Distinctions"),widget=forms.Textarea())
    motivation   = forms.CharField(label=_("Motivation letter"),widget=forms.Textarea())
 
    
    
        