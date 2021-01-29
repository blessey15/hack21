from django import forms

from .models import Abstract, PROBLEM_STATEMENT_CHOICES, Submission

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

    abstract = forms.CharField( required=True, help_text="Give a brief abstract of your project", max_length=2000,
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


class SubmissionForm(forms.ModelForm):
    video_link = forms.URLField( required=True,
        error_messages = {
            'invalid': "Please enter a valid URL"
        },
        widget = forms.URLInput(
            attrs={
                "class": "form-control py-1 form-control-user",
                "placeholder": "Link to the project Video(youtube)"
            }
        )
    )

    code_link = forms.URLField( required=False, help_text="Please make sure to submit any code that is involved in the project",
        error_messages = {
            'invalid': "Please enter a valid URL"
        },
        widget = forms.URLInput(
            attrs={
                "class": "form-control py-1 form-control-user",
                "placeholder": "Link to the project code"
            }
        )
    )
    ppt_link = forms.URLField( required=False,
        error_messages = {
            'invalid': "Please enter a valid URL"
        },
        widget = forms.URLInput(
            attrs={
                "class": "form-control py-1 form-control-user",
                "placeholder": "Link to  your presentation"
            }
        )
    )

    class Meta:
        model = Submission
        fields = ('video_link', 'code_link', 'ppt_link')
