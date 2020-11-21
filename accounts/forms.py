from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from accounts.models import Account

class RegistrationForm(UserCreationForm):
    # email = forms.EmailField(max_length=64, help_text='Required. Add a valid email address')
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Username",                
                "class": "form-control form-control-user",
                "id": "exampleInputUsername"
            }
        ))

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder" : "Email",                
                "class": "form-control form-control-user",
                "id": "exampleInputEmail"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Password",                
                "class": "form-control form-control-user",
                "id": "exampleInputPassword"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Password check",                
                "class": "form-control form-control-user",
                "id": "exampleRepeatPassword"
            }
        ))
    class Meta:
        model = Account
        fields = ('email', 'username', 'password1', 'password2')

class AccountAuthenticationForm(forms.ModelForm):
    # password = forms.CharField(label='password', widget=forms.PasswordInput)
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder" : "Enter Email Address...",                
                "class": "form-control form-control-user",
                "id": "exampleInputEmail"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Password",                
                "class": "form-control form-control-user",
                "id": "exampleInputPassword"
            }
        ))

    class Meta:
        model = Account
        fields = ('email', 'password')

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if not authenticate(email=email, password=password):
            raise forms.ValidationError("Invalid Login!!")

class AccountUpdateForm(forms.ModelForm):

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Username",                
                "class": "form-control form-control-user",
                "id": "exampleInputUsername"
            }
        ))

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder" : "Email",                
                "class": "form-control form-control-user",
                "id": "exampleInputEmail"
            }
        ))

    class Meta:
        model = Account
        fields = ('email', 'username')

    def clean_email(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            try:
                account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
            except Account.DoesNotExist:
                return email
            raise forms.ValidationError('Email "%s" is already in use' %(account.email))
    
    def clean_username(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            try:
                account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
            except Account.DoesNotExist:
                return username
            raise forms.ValidationError('Username "%s" is already in use' %(account.username))