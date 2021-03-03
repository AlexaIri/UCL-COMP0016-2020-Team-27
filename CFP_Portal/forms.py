from django import forms
from CFP_Portal.models import Person, Comment
# from phonenumber_field.formfields import PhoneNumberField




class Proposal(forms.Form):

    SHIRT_SIZES = (
        ('Scaffolding','Scaffolding'),
        ('Discovery','Discovery'),
        ('Innovation', 'Innovation'),
    )
    
    OPEN_OR_CLOSE = (
        ('Open Source', 'Open Source'),
        ('Closed Source', 'Closed Source'),

    )

    yesno = (
        ('Y', 'Yes'),
        ('N', 'No'),

    )

    TIERS = (
        ('1','1'),
        ('2','2'),
        ('3', '3'),
        ('4', '4'),
        )
    
    #  class Meta:
    #      model = Person
         
    #      fields = ('name', 'surname', 'phone_number', 'email',)

    name = forms.CharField(widget = forms.TextInput(attrs ={'placeholder': 'First name'}))
    surname = forms.CharField(widget = forms.TextInput(attrs ={'placeholder': 'Family name'}))
    email = forms.CharField(widget = forms.TextInput(attrs ={'placeholder': 'Email address'}))
    # phone_number = PhoneNumberField()
    phone_number =  forms.CharField(widget = forms.TextInput(attrs ={'placeholder': 'Phone'}))
    title = forms.CharField(widget = forms.TextInput(attrs ={'placeholder': 'Job Title'}))
    project_title = forms.CharField(widget = forms.TextInput(attrs ={'placeholder': 'Title'}))
    summarized_abstract = forms.CharField(max_length=2000, widget = forms.TextInput(attrs ={'placeholder': 'Abstract (summary)'}))
    full_abstract = forms.CharField(max_length=5000, widget = forms.TextInput(attrs ={'placeholder': 'Abstract (in full)'}))
    expertise_and_skills = forms.CharField(max_length=200, widget = forms.TextInput(attrs ={'placeholder': 'Skills & Knowledge'}))
    devices = forms.CharField(max_length=200, widget = forms.TextInput(attrs ={'placeholder': 'Devices'}))
    
    project_complexity = forms.ChoiceField(choices=SHIRT_SIZES)

    source_type = forms.ChoiceField(choices=OPEN_OR_CLOSE)
    
    ethics_form  = forms.ChoiceField(choices=yesno)
    launching_date = forms.CharField(widget = forms.TextInput(attrs ={'placeholder': 'Date'}))
    motivations = forms.CharField(widget = forms.TextInput(attrs ={'placeholder': 'What motivated you?'}))
    importance = forms.CharField(widget = forms.TextInput(attrs ={'placeholder': 'Why is your project important?'}))
    hashtags = forms.CharField(widget = forms.TextInput(attrs ={'placeholder': 'Hashtags'}))
   
class Commentform(forms.ModelForm):
       class Meta:
           model = Comment
           fields = ('name','feedback',)
           widgets = {
                "name" : forms.TextInput(attrs ={'placeholder': 'First name'}),
                "feedback" : forms.TextInput(attrs ={'placeholder': 'feedback'}),
           }