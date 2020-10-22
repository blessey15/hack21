from django import forms

from .models import Team

class TeamCreateForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('name',)
    def clean_name(self):
        name = self.cleaned_data.get('name')
        try:
            team = Team.objects.exclude(pk=self.instance.id).get(name=name)
        except Team.DoesNotExist:
            return name
        raise forms.ValidationError('Team name "%s" is already taken' %(team.name))