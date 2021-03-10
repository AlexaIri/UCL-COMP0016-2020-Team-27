from django import forms
from CFP_Portal.models import Person, Comment, Review
from django.forms import ModelChoiceField
# from phonenumber_field.formfields import PhoneNumberField




class Proposal(forms.ModelForm):
    class Meta:
        model = Person
        # fields = ['name','surname','email','phone_number','title','project_title','summarised_abstract','full_abstract','expertiseskills','devices','launching_date','motivations','importance','hashtags','tags','project_complexity','source_type','ethics_form']
        exclude = ['priority','status','department','organisation','completionPercentage','submission_date']
        widgets = {
            "name" : forms.TextInput(attrs ={'placeholder': 'First name'}),
            "surname" : forms.TextInput(attrs ={'placeholder': 'Family name'}),
            "email" : forms.TextInput(attrs ={'placeholder': 'Email address'}),
            # phone_number = PhoneNumberField()
            "phone_number" : forms.TextInput(attrs ={'placeholder': 'Phone'}),
            "title" : forms.TextInput(attrs ={'placeholder': 'Job Title'}),
            "project_title" : forms.TextInput(attrs ={'placeholder': 'Title'}),
            "summarised_abstract" : forms.TextInput(attrs ={'placeholder': 'Abstract (summary)'}),
            "full_abstract" : forms.TextInput(attrs ={'placeholder': 'Abstract (in full)'}),
            "expertiseskills" : forms.TextInput(attrs ={'placeholder': 'Skills & Knowledge'}),
            "devices" : forms.TextInput(attrs ={'placeholder': 'Devices'}),
            
            
            "launching_date" : forms.TextInput(attrs ={'placeholder': 'Date'}),
            "motivations" : forms.TextInput(attrs ={'placeholder': 'What motivated you?'}),
            "importance" : forms.TextInput(attrs ={'placeholder': 'Why is your project important?'}),
            "challenge" : forms.TextInput(attrs ={'placeholder': 'Is this project a response to a challenge?'}),
        
           }
    
   
class Commentform(forms.ModelForm):
       class Meta:
           model = Comment
           fields = ('feedback',)
           widgets = {
                "feedback" : forms.TextInput(attrs ={'placeholder': 'feedback'}),
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

    RAG = [('Red','Red'),
         ('Amber','Amber'),
         ('Green','Green')]
         

    standards_and_interoperability_points = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    technical_and_scientific_strength_points = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    user_centred_design_points = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    usability_testing_points = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    research_quality_points = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    scalability_points = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    resilience_points = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    #RAGlevel = forms.ChoiceField(choices=RAG, widget=forms.RadioSelect)