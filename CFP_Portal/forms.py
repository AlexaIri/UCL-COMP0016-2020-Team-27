from django import forms
from CFP_Portal.models import Person, Comment, Review
from django.forms import ModelChoiceField
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
    # email = forms.CharField(widget = forms.TextInput(attrs ={'placeholder': 'Email address'}))
    email = forms.EmailField(widget = forms.EmailInput(attrs ={'placeholder': 'Email address'}))
    # phone_number = PhoneNumberField()
    phone_number =  forms.CharField(widget = forms.TextInput(attrs ={'placeholder': 'Phone'}))

    # project_title = forms.CharField(widget = forms.TextInput(attrs ={'placeholder': 'Title'}))
    project_title = forms.CharField(max_length=2000, widget = forms.Textarea(attrs ={"rows":2, "cols":20, 'placeholder': 'Title'}))
    # summarized_abstract = forms.CharField(max_length=2000, widget = forms.TextInput(attrs ={'placeholder': 'Abstract (summary)'}))
    summarized_abstract = forms.CharField(max_length=2000, widget = forms.Textarea(attrs ={"rows":5, "cols":20, 'placeholder': 'Abstract (summary)'}))
    # full_abstract = forms.CharField(max_length=5000, widget = forms.TextInput(attrs ={'placeholder': 'Abstract (in full)'}))
    full_abstract = forms.CharField(max_length=5000, widget = forms.Textarea(attrs ={"rows":7, "cols":20, 'placeholder': 'Abstract (in full)'}))
    # expertise_and_skills = forms.CharField(max_length=200, widget = forms.TextInput(attrs ={'placeholder': 'Skills & Knowledge'}))
    expertise_and_skills = forms.CharField(max_length=200, widget = forms.Textarea(attrs ={"rows":2, "cols":20, 'placeholder': 'Skills & Knowledge'}))
    # devices = forms.CharField(max_length=200, widget = forms.TextInput(attrs ={'placeholder': 'Devices'}))
    devices = forms.CharField(max_length=200, widget = forms.Textarea(attrs ={"rows":2, "cols":20, 'placeholder': 'Devices'}))
    
    project_complexity = forms.ChoiceField(choices=SHIRT_SIZES)

    source_type = forms.ChoiceField(choices=OPEN_OR_CLOSE)
    
    ethics_form  = forms.ChoiceField(choices=yesno)
    launching_date = forms.CharField(widget = forms.TextInput(attrs ={'placeholder': 'Date'}))
    # motivations = forms.CharField(widget = forms.TextInput(attrs ={'placeholder': 'What motivated you?'}))
    motivations = forms.CharField(max_length=1000, widget = forms.Textarea(attrs ={"rows":3, "cols":20, 'placeholder': 'What motivated you?'}))
    # importance = forms.CharField(widget = forms.TextInput(attrs ={'placeholder': 'Why is your project important?'}))
    importance = forms.CharField(max_length=1000, widget = forms.Textarea(attrs ={"rows":3, "cols":20, 'placeholder': 'Why is your project important?'}))
    hashtags = forms.CharField(widget = forms.TextInput(attrs ={'placeholder': 'Hashtags'}))
   
class Commentform(forms.ModelForm):
       class Meta:
           model = Comment
           fields = ('name','feedback',)
           widgets = {
                "name" : forms.TextInput(attrs ={'placeholder': 'Full name'}),
                "feedback" : forms.TextInput(attrs ={'placeholder': 'Write your feedback'}),
           }
           
class ProjectModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "Project #%s) %s" % (obj.id,obj.project_title)

class ReviewForm(forms.Form):

    TIERS = (
        ('1','1'),
        ('2','2'),
        ('3', '3'),
        ('4', '4'),
        )

    id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    project = ProjectModelChoiceField(queryset=Person.objects.all())
    
    reviewer_name = forms.CharField(widget = forms.TextInput(attrs ={'placeholder': ''}))
    reviewer_surname = forms.CharField(widget = forms.TextInput(attrs ={'placeholder': ''}))
    reviewer_email = forms.CharField(widget = forms.TextInput(attrs ={'placeholder': ''}))
    # phone_number = PhoneNumberField()
    reviewer_phone_number =  forms.CharField(widget = forms.TextInput(attrs ={'placeholder': ''}))

    comments = forms.CharField(widget = forms.Textarea(attrs ={"rows":5, "cols":20, 'placeholder': 'Write your final feedback in here...'}))
    # widget=forms.Textarea(attrs={"rows":5, "cols":20}

    standards_and_interoperability_comments = forms.CharField(max_length=2000, widget = forms.Textarea(attrs ={"rows":5, "cols":20, 'placeholder': 'Type in your comment...'}))
    technical_and_scientific_strength_comments = forms.CharField(max_length=2000, widget = forms.Textarea(attrs ={"rows":5, "cols":20, 'placeholder': 'Type in your comment...'}))
    user_centred_design_comments = forms.CharField(max_length=2000, widget = forms.Textarea(attrs ={"rows":5, "cols":20, 'placeholder': 'Type in your comment...'}))
    usability_testing_comments = forms.CharField(max_length=2000, widget = forms.Textarea(attrs ={"rows":5, "cols":20, 'placeholder': 'Type in your comment...'}))
    research_quality_comments = forms.CharField(max_length=2000, widget = forms.Textarea(attrs ={"rows":5, "cols":20, 'placeholder': 'Type in your comment...'}))
    scalability_comments = forms.CharField(max_length=2000, widget = forms.Textarea(attrs ={"rows":5, "cols":20, 'placeholder': 'Type in your comment...'}))
    resilience_comments = forms.CharField(max_length=2000, widget = forms.Textarea(attrs ={"rows":5, "cols":20, 'placeholder': 'Type in your comment...'}))

    # CHOICES=[('0',' 0 - Extremely Low'),
    #      ('1','     1 - Low'),
    #      ('2',' 2 - Moderate'),
    #      ('3','Score: 3 - Good'),
    #      ('4','Score: 4 - Very good'),
    #      ('5','Score: 5 - Excellent')]

    CHOICES=[('0','0'),
         ('1','1'),
         ('2','2'),
         ('3','3'),
         ('4','4'),
         ('5','5')]

    standards_and_interoperability_points = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    technical_and_scientific_strength_points = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    user_centred_design_points = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    usability_testing_points = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    research_quality_points = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    scalability_points = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    resilience_points = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)