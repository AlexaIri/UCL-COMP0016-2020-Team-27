from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image
from django.db.models import F
from taggit.managers import TaggableManager
# from phonenumber_field.modelfields import PhoneNumberField


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

class AnnotationManager(models.Manager):

    def __init__(self, **kwargs):
        super().__init__()
        self.annotations = kwargs

    def get_queryset(self):
        return super().get_queryset().annotate(**self.annotations)
class Person(models.Model):
    
    def get_absolute_url(self):
        return reverse("project-detail", kwargs={"pk": self.pk})

    name = models.CharField("name", max_length=130, default = "")
   
    phone_number = models.CharField("phone number", max_length=130, default = "")
    #phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    email = models.EmailField("email", max_length=130, default = "")
    title = models.CharField("job title", max_length=130, default = "")
    project_title = models.CharField("title", max_length=130, default = "")
    summarised_abstract = models.CharField("summarised abstract", max_length=2000, default = "")
    department = models.CharField("department", max_length=2000, default = "",blank=True)
    organisation = models.CharField("organisation", max_length=2000, default = "",blank=True)
    challenge = models.CharField("challenge", max_length=2000, default = "", blank=True)

    full_abstract = models.TextField("full abstract", default = "")
    expertiseskills = models.TextField("expertise skills", default = "")
    devices = models.TextField("devices", default = "")
    

    
    SHIRT_SIZES = (
        ('Scaffolding','Scaffolding'),
        ('Discovery','Discovery'),
        ('Innovation', 'Innovation'),
    )
    TIERS = (
        ('1','1'),
        ('2','2'),
        ('3', '3'),
        ('4', '4'),)

    
    
    project_complexity = models.CharField("project complexity", max_length=20, choices=SHIRT_SIZES, default = "")

    OPEN_OR_CLOSE = (
        ('Open Source', 'Open Source'),
        ('Closed Source', 'Closed Source'),

    )

    yesno = (
        ('Yes', 'Yes'),
        ('No', 'No'),

    )

   
    source_type = models.CharField("open source or closed source", max_length=20, choices=OPEN_OR_CLOSE, default = "")
    
    ethics_form  = models.CharField("Have you completed the ethics form?", max_length=20, choices=yesno, default = "")
    launching_date = models.DateField("launching date:", default = "2021-01-25")
    motivations = models.TextField("motivations", default = "")
    importance = models.TextField("why is your project important", default = "")
    
    tags = TaggableManager()
    statusType = (
        ('Accepeted', 'Accepted'),
        ('Rejected', 'Rejected'),
        ('Under Review', 'Under Review'),
        ('Submitted', 'Submitted'),
        ('Paused', 'Paused'),
        ('Reviewed', 'Reviewed')

    )

    status = models.CharField("What is the current status of the project?", max_length=20, choices=statusType, default = "")

    completionPercentage = models.IntegerField(default=0) # up to 100%

    priorityStatus = (
        ('High', 'High'),
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('No priority', 'No priority'),
    )

    tier = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
    )
    NICEtier = models.CharField("What is the NICE tier of the project?", max_length=20, choices=tier, default = "")
    challenge = models.TextField("Is this project from a challenge?", default = "", blank= True)
    priority = models.CharField("What is the priority level of the project?", max_length=20, choices=priorityStatus, default = "")
    submission_date = models.DateTimeField(auto_now_add=True)
    user  = models.ForeignKey(User, related_name="user", on_delete=models.CASCADE, null=True)
    evidence = models.FileField(upload_to ='uploads/', blank=True) 
    github = models.URLField("github link",max_length = 200, blank=True) 

    
    def __str__(self):
        return '%s' % (self.project_title)



    
    


class Review(models.Model):
    def get_absolute_url(self):
        return reverse("reviewdetail", kwargs={"pk": self.pk})
    
    # review_date= models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(Person, related_name='reviews',blank=True, null=True, on_delete=models.CASCADE)
    review_body = models.CharField(max_length = 5000, default = "",  null=True)
    reviewer_name = models.CharField("reviewer name", max_length=130, default = "",  null=True)
    reviewer_surname = models.CharField("reviewer surname", max_length=130, default = "",  null=True)
   
    #phone_number = PhoneNumberField(null=False, blank=False, unique=True)
    reviewer_email = models.EmailField("reviewer email", max_length=130, default = "",  null=True)

    #Points of the marking criteria
    interoperabilityPoints = models.IntegerField(default=0,  null=True)
    technical_strengthPoints = models. IntegerField(default=0,  null=True)
    user_designPoints = models.IntegerField(default=0,  null=True)
    scalabilityPoints = models.IntegerField(default=0,  null=True)
    resiliencePoints = models.IntegerField(default=0,  null=True)
    usabilityTestingPoints = models.IntegerField(default=0,  null=True)
    researchQualityPoints = models.IntegerField(default=0,  null=True)

    #Comments on the marking criteria   
    interoperabilityComments = models.CharField("standard and interoperability", max_length=2000, default = "",  null=True)
    technical_strengthComments = models.CharField("technical strength", max_length=2000, default = "",  null=True)
    user_designComments = models.CharField("user-centred design", max_length=2000, default = "",  null=True)
    usabilityTestingComments = models.CharField("usability testing", max_length=2000, default = "",  null=True)
    researchQualityComments = models.CharField("research quality", max_length=2000, default = "",  null=True)
    scalabilityComments = models.CharField("scalability", max_length=2000, default = "",  null=True)
    resilienceComments = models.CharField("resilience", max_length=2000, default = "",  null=True)

    # points = models.IntegerField(null=True)
    # score = models.DecimalField(max_digits=6, decimal_places=2,  null=True)
    # _points = None
    # _score = None

    # objects = AnnotationManager(
    #     points=F('interoperabilityPoints')+F('technical_strengthPoints')+F('user_designPoints')+F('scalabilityPoints') +F('resiliencePoints')+F('usabilityTestingPoints') +F('researchQualityPoints'),
    #     score=F('_points') * 100 / 35
    # )
    points=models.IntegerField(default=0, null=True)
    score = models.DecimalField(default=0.00, max_digits=6, decimal_places=2,  null=True)

    interoperabilityPoints100 = models.IntegerField(default=0,  null=True)
    technical_strengthPoints100 = models. IntegerField(default=0,  null=True)
    user_designPoints100 = models.IntegerField(default=0,  null=True)
    scalabilityPoints100 = models.IntegerField(default=0,  null=True)
    resiliencePoints100 = models.IntegerField(default=0,  null=True)
    usabilityTestingPoints100 = models.IntegerField(default=0,  null=True)
    researchQualityPoints100 = models.IntegerField(default=0,  null=True)
    RAGlevel = models.CharField("RAG level", max_length=130, default = "",  null=True)


    def save(self, *args, **kwargs):
        self.points = int(self.interoperabilityPoints) + int(self.technical_strengthPoints) + int(self.user_designPoints) + int(self.scalabilityPoints) + int(self.resiliencePoints) + int(self.usabilityTestingPoints) + int(self.researchQualityPoints)
        self.score = int(self.points) * 100/35
        self.interoperabilityPoints100 = int(self.interoperabilityPoints)*20
        self.technical_strengthPoints100 = int(self.technical_strengthPoints)*20
        self.user_designPoints100 = int(self.user_designPoints)*20
        self.scalabilityPoints100 = int(self.scalabilityPoints)*20
        self.resiliencePoints100 = int(self.resiliencePoints)*20
        self.usabilityTestingPoints100 = int(self.usabilityTestingPoints)*20
        self.researchQualityPoints100 = int(self.researchQualityPoints)*20
        # self.interoperabilityPoints100  = int(self.points) * 100/35
        super(Review, self).save(*args, **kwargs)
    # @property
    # def points(self):
    #     return self.interoperabilityPoints + self.technical_strengthPoints + self.user_designPoints + self.scalabilityPoints + self.resiliencePoints + self.usabilityTestingPoints + self.researchQualityPoints

    # @property
    # def score(self):
    #     return self.points * 100/35

    #green-amber-red boolean system
    green = models.BooleanField(default = False, null=True)
    amber = models.BooleanField(default =False, null=True)
    red = models.BooleanField(default = False, null=True)

    comments = models.TextField("comments", default = "", null = True)

class Comment(models.Model):
    project = models.ForeignKey(Person, related_name="comments", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    feedback = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s' % (self.project.project_title)



class Post(models.Model):
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})

    title = models.CharField(max_length = 100)
    content = models.TextField()
    date_posted = models.DateTimeField(default = timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)



class AcceptedProjects(models.Model):
    project = models.OneToOneField(
        Person,
        related_name="project",
        on_delete=models.CASCADE,
        primary_key=True,
    )
    date_accepted = models.DateTimeField(default = timezone.now)
    
    def __str__(self):
        return '%s' % (self.project.project_title)

class RejectedProjects(models.Model):
    project = models.OneToOneField(
        Person,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    date_accepted = models.DateTimeField(default = timezone.now)
    
    def __str__(self):
        return '%s' % (self.project.project_title)
    