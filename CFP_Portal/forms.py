from django import forms
from CFP_Portal.models import Person, Comment, Review
from django.forms import ModelChoiceField
# from phonenumber_field.formfields import PhoneNumberField




class Proposal(forms.ModelForm):
    class Meta:
        model = Person
        # fields = ['name','surname','email','phone_number','title','project_title','summarised_abstract','full_abstract','expertiseskills','devices','launching_date','motivations','importance','hashtags','tags','project_complexity','source_type','ethics_form']
        exclude = ['priority','status','department','organisation','completionPercentage','submission_date','user']
        widgets = {
            "name" : forms.TextInput(attrs ={'placeholder': 'Full name'}),
            "email" : forms.TextInput(attrs ={'placeholder': 'Email address'}),
            # phone_number = PhoneNumberField()
            "phone_number" : forms.TextInput(attrs ={'placeholder': 'Phone'}),
            "title" : forms.TextInput(attrs ={'placeholder': 'Job Title'}),
            "project_title" : forms.TextInput(attrs ={'placeholder': 'Title'}),
            "summarised_abstract" :  forms.Textarea(attrs ={"rows":5, "cols":20, 'placeholder': 'Provide a summary of your abstract...'}),
            "full_abstract" : forms.Textarea(attrs ={"rows":5, "cols":20, 'placeholder': 'Provide the full version of your abstract...'}),
            "expertiseskills" : forms.Textarea(attrs ={"rows":3, "cols":20, 'placeholder': 'Skills and Knowledge'}),
            "devices" : forms.Textarea(attrs ={"rows":3, "cols":20, 'placeholder': 'Devices and Technologies'}),
            
            
            "launching_date" : forms.TextInput(attrs ={'placeholder': 'Date'}),
            "motivations" : forms.Textarea(attrs ={"rows":3, "cols":20, 'placeholder': 'What motivated you?'}),
            "importance" : forms.Textarea(attrs ={"rows":3, "cols":20, 'placeholder': 'Why is your project important?'}),
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
    # project = ProjectModelChoiceField(queryset=Person.objects.all())
    
    
    # phone_number = PhoneNumberField()
   

    comments = forms.CharField(widget = forms.Textarea(attrs ={"rows":5, "cols":20, 'placeholder': 'Write your final feedback in here...'}))
    # widget=forms.Textarea(attrs={"rows":5, "cols":20}

    standards_and_interoperability_comments = forms.CharField(max_length=2000, widget = forms.Textarea(attrs ={"rows":5, "cols":20, 'placeholder': 'Type in your comment...'}))
    technical_and_scientific_strength_comments = forms.CharField(max_length=2000, widget = forms.Textarea(attrs ={"rows":5, "cols":20, 'placeholder': 'Type in your comment...'}))
    user_centred_design_comments = forms.CharField(max_length=2000, widget = forms.Textarea(attrs ={"rows":5, "cols":20, 'placeholder': 'Type in your comment...'}))
    usability_testing_comments = forms.CharField(max_length=2000, widget = forms.Textarea(attrs ={"rows":5, "cols":20, 'placeholder': 'Type in your comment...'}))
    research_quality_comments = forms.CharField(max_length=2000, widget = forms.Textarea(attrs ={"rows":5, "cols":20, 'placeholder': 'Type in your comment...'}))
    scalability_comments = forms.CharField(max_length=2000, widget = forms.Textarea(attrs ={"rows":5, "cols":20, 'placeholder': 'Type in your comment...'}))
    resilience_comments = forms.CharField(max_length=2000, widget = forms.Textarea(attrs ={"rows":5, "cols":20, 'placeholder': 'Type in your comment...'}))


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