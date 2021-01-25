from django.db import models

# Create your models here.
class Organisation(models.Model):

    def __str__(self):
        return self.organisation_name

    organisation_name = models.CharField(max_length = 255, default = "Default name")
    organisation_address = models.CharField(max_length = 255, default = "Default IXN Subscriber Company")
    overview = models.CharField(max_length = 5000, default = " Default overview")
    IXN_lead = models.CharField(max_length = 255)



class Person(models.Model):

    name = models.CharField("name", max_length=130, default = "")
    surname = models.CharField("surname", max_length=130, default = "")
    phone_number = models.CharField("phone number", max_length=130, default = "")
    email = models.EmailField("email", max_length=130, default = "")
    project_title = models.CharField("title", max_length=130, default = "")
    summarised_abstract = models.CharField("summarised abstract", max_length=2000, default = "")
    full_abstract = models.TextField("full abstract", default = "")
    expertiseskills = models.TextField("expertise skills", default = "")
    devices = models.TextField("devices", default = "")

    
    SHIRT_SIZES = (
        ('Scaffolding','Scaffolding'),
        ('Discovery','Discovery'),
        ('Innovation', 'Innovation'),
    )
    
    project_complexity = models.CharField("project complexity", max_length=20, choices=SHIRT_SIZES, default = "")

    OPEN_OR_CLOSE = (
        ('Open Source', 'Open Source'),
        ('Closed Source', 'Closed Source'),

    )

    yesno = (
        ('Y', 'Yes'),
        ('N', 'No'),

    )

   
    source_type = models.CharField("open source or closed source", max_length=20, choices=OPEN_OR_CLOSE, default = "")
    
    ethics_form  = models.CharField("Have you completed the ethics form?", max_length=20, choices=yesno, default = "")
    launching_date = models.DateField("launching date:", default = "2021-01-25")
    motivations = models.TextField("motivations", default = "")
    importance = models.TextField("why is your project important", default = "")
    hashtags = models.CharField(max_length = 255, default = "hashtags")