from django import forms

from .models import Team
from .validators import is_valid_uuid

class TeamCreateForm(forms.ModelForm):
    # team_doesnt_exist = False

    # def __init__(self, user, *args, **kwargs):
    #     self.user  = user
    #     super(TeamCreateForm, self).__init__(self.user,*args, **kwargs)

    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Enter a Team Name",                
                "class": "form-control form-control-user"
            }
        ))
    class Meta:
        model = Team
        fields = ('name',)
    def clean_name(self):
        name = self.cleaned_data.get('name')
        try:
            team = Team.objects.exclude(pk=self.instance.id).get(name=name)
            # team = Team.objects.exclude(admin=self.user).get(name=name)
        except Team.DoesNotExist:
            return name
        raise forms.ValidationError('Team name "%s" is already taken or you have already created a team' %(team.name))
        # try:
        #     team = Team.objects.exclude(admin=user).get(name=name)
        # except Team.DoesNotExist:
        #     return name
        # raise forms.ValidationError("You already have a team!!")
    # def clean_user(self):
    #     name = self.cleaned_data.get('name')
    #     team = Team.objects.filter(admin=request.user)
    #     if len(team) == 0:
    #         return name
    #     raise forms.ValidationError("You already have a team!!")

class TeamSearchForm(forms.Form):
    team_id = forms.CharField(max_length=64,
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Enter Team ID to Search",                
                "class": "form-control form-control-user"
            }
        ))

    def clean_team_id(self):
        team_id = self.cleaned_data.get('team_id')
        if not is_valid_uuid(team_id):
            raise forms.ValidationError("Not a valid Team ID!!")
        return team_id