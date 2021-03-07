from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    department = forms.CharField(widget = forms.TextInput(attrs ={'placeholder': 'Department you work in'}), required=False)
    organisation = forms.CharField(widget = forms.TextInput(attrs ={'placeholder': 'Organisation or Trust '}), required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ProfileRegisterForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['image', 'department', 'organisation']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    department = forms.CharField(widget = forms.TextInput(attrs ={'placeholder': 'Department you work in'}), required=False)
    organisation = forms.CharField(widget = forms.TextInput(attrs ={'placeholder': 'Organisation or Trust '}), required=False)
    class Meta:
        model = Profile
        fields = ['image']