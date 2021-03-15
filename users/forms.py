from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    department = forms.CharField(widget = forms.TextInput(attrs ={'placeholder': 'Department you work in'}), required=False)
    organisation = forms.CharField(widget = forms.TextInput(attrs ={'placeholder': 'Organisation or Trust '}), required=False)
    
    Users = [('Submitters','Submitters'),
         ('Reviewers','Reviewers'),
         ('Lead','Lead')]
         
    group = forms.ChoiceField(choices=Users, widget=forms.RadioSelect)


    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ProfileRegisterForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['image', 'department', 'organisation','full_name']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    fullname = forms.CharField(widget = forms.TextInput(attrs ={'placeholder': 'Full name'}))
    department = forms.CharField(widget = forms.TextInput(attrs ={'placeholder': 'Department you work in'}), required=False)
    organisation = forms.CharField(widget = forms.TextInput(attrs ={'placeholder': 'Organisation or Trust '}), required=False)
    organisation_address = forms.CharField(widget = forms.TextInput(attrs ={'placeholder': 'Organisation Address '}), required=False)

    about = forms.CharField(max_length=2000, widget = forms.Textarea(attrs ={"rows":5, "cols":20, 'placeholder': 'Type in your bio description...'}))
  
    wordpress = forms.URLField(widget = forms.URLInput(attrs ={'placeholder': 'Wordpress Link '}), required=False)
    twitter = forms.URLField(widget = forms.URLInput(attrs ={'placeholder': 'Twitter Link '}), required=False)
    linkedin = forms.URLField(widget = forms.URLInput(attrs ={'placeholder': 'Linkedin Link '}), required=False)
    facebook = forms.URLField(widget = forms.URLInput(attrs ={'placeholder': 'Facebook Link '}), required=False)
    git = forms.URLField(widget = forms.URLInput(attrs ={'placeholder': 'Github Link '}), required=False)
 

    class Meta:
        model = Profile
        fields = ['image']

class Login(forms.Form):
    
    username = forms.CharField(widget = forms.TextInput(attrs ={'placeholder': ''}))
    password = forms.CharField(widget = forms.TextInput(attrs ={'placeholder': ''}))
    # reviewer_email = forms.CharField(widget = forms.TextInput(attrs ={'placeholder': ''}))
    # phone_number = PhoneNumberField()
    # reviewer_phone_number =  forms.CharField(widget = forms.TextInput(attrs ={'placeholder': ''}))

    # comments = forms.CharField(widget = forms.Textarea(attrs ={"rows":5, "cols":20, 'placeholder': 'Write your final feedback in here...'}))
    # widget=forms.Textarea(attrs={"rows":5, "cols":20}

  