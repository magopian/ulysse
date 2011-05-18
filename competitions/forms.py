#-*- coding: utf-8 -*-
from copy import deepcopy
from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.auth.models import Group
from django import forms
from django.conf import settings
from django.utils.translation import ugettext as _
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
        
        
class CandidateAdminForm(forms.Form):
    """
    A custom orm for candidate in competition admin

    """    
    def __init__(self, data=None, *args, **kwargs):        
        super(CandidateAdminForm, self).__init__(data, *args, **kwargs)        
        self._build_dynamic_fields()
        
    def _build_dynamic_fields(self):
        # Set form fields        
        self.fields["education"] = forms.CharField(widget=forms.Textarea())        
    
        
    #education    = forms.CharField(widget=forms.Textarea())
    #experience   = forms.CharField(label=_("Professional experience"),widget=forms.Textarea())
    #distinctions = forms.CharField(label=_("Distinctions"),widget=forms.Textarea())
    #motivation   = forms.CharField(label=_("Motivation letter"),widget=forms.Textarea())

class CandidateJuryAllocationForm(forms.ModelForm):
    class Meta:
        model = CandidateJuryAllocation

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
