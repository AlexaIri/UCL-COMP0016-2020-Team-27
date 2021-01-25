from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image

def user_directory_path(instance, filename): 
  
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename> 
        return 'user_{0}/{1}'.format(instance.user.id, filename) 

# Create your models here.
class Organisation(models.Model):

    def __str__(self):
        return self.organisation_name

    organisation_name = models.CharField(max_length = 255, default = "")
    organisation_address = models.CharField(max_length = 255, default = "")
    organisation_logo = models.ImageField(default='default_logo.png', upload_to='organisations_pics')
    overview = models.CharField(max_length = 5000, default = "")
    IXN_lead = models.CharField(max_length = 255)

    def save(self):
        super().save()

        img = Image.open(self.organisation_logo.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.organisation_logo.path)


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

# class ProjectProposals(models.Model):
#     project_name = models.CharField(max_length = 255, default = "Default name")
#     project_title = models.CharField(max_length = 255, default = "Default title")
#     project_summary = models.CharField(max_length = 2000, default = "Default summary")
#     full_project_abstract = models.CharField(max_length = 10000, default = "Default abstract")
#     technical_challenges = models.CharField(max_length = 255, default = "Default title")
#     expertise_skills= models.CharField(max_length = 255, default = "Default title")
#     technologies_required = models.CharField(max_length = 255, default = "Default title")
#     project_complexity = models.CharField(max_length = 255, default = "Default title")
#     source_type= models.CharField(max_length = 255, default = "Default title")
#     project_start_date=  models.DateField()
#     motivations = models.CharField(max_length = 255, default = "Default title")
#     project_importance= models.CharField(max_length = 255, default = "Default title")
#     hashtags = models.CharField(max_length = 255, default = "Default title")

# class Review(models.Model):
#     # project = models.ForeignKey(ProjectProposals, blank=True, null=True, on_delete=models.CASCADE)
#     review_body = models.CharField(max_length = 5000, default = "Default review body")

#     #Enlist all the marking criteria
#     technical_quality = models. IntegerField()
#     usability = models.IntegerField()
#     scalability = models.IntegerField()
#     innovation = models.IntegerField()

#     #green-amber-red boolean system
#     green = models.BooleanField()
#     amber = models.BooleanField()
#     red = models.BooleanField()


class Post(models.Model):
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})

    title = models.CharField(max_length = 100)
    content = models.TextField()
    date_posted = models.DateTimeField(default = timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

   
    