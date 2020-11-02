from django import forms

from .models import Team

class TeamCreateForm(forms.ModelForm):
    # team_doesnt_exist = False

    # def __init__(self, user, *args, **kwargs):
    #     self.user  = user
    #     super(TeamCreateForm, self).__init__(self.user,*args, **kwargs)
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
