from django import forms
from CFP_Portal.models import Person

class Proposal(forms.ModelForm):
    
     class Meta:
         model = Person
         
         fields = ('name', 'surname', 'phone_number', 'email',)

class Proposal2(forms.ModelForm):
    
     class Meta:
         model = Person
         
         fields = ('project_title', 'summarised_abstract', 'full_abstract', 'expertiseskills', 'devices',)


class Proposal3(forms.ModelForm):
        
     class Meta:
         model = Person
         
         fields = ('project_complexity', 'source_type','ethics_form', 'launching_date',)

class Proposal4(forms.ModelForm):
        
     class Meta:
         model = Person
         
         fields = ('motivations', 'importance','hashtags', )
    