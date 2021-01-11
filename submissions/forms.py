from django import forms

from .models import Abstract, PROBLEM_STATEMENT_CHOICES

class AbstractForm(forms.ModelForm):
    problem_statement = forms.ChoiceField( choices=PROBLEM_STATEMENT_CHOICES,
        widget = forms.Select(
            attrs={
                "class": "form-control py-1 form-control-user"
            }
        )
    )

    project_title = forms.CharField( required=True,
        widget = forms.TextInput(
            attrs={
                "class": "form-control py-1 form-control-user",
                "placeholder": "Enter Project Title"
            }
        )
    )

    abstract = forms.CharField( required=True, help_text="Give a brief abstract of your project",
        widget = forms.Textarea(
            attrs={
                "placeholder": "Project Abstract",
                "class": "form-control py-1"
            }
        )
    )

    class Meta:
        model =  Abstract
        fields = ('problem_statement', 'project_title', 'abstract')