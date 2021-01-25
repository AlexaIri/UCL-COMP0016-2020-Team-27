from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Organisation(models.Model):

    def __str__(self):
        return self.organisation_name

    organisation_name = models.CharField(max_length = 255, default = "Default name")
    organisation_address = models.CharField(max_length = 255, default = "Default IXN Subscriber Company")
    overview = models.CharField(max_length = 5000, default = " Default overview")
    IXN_lead = models.CharField(max_length = 255)


class Post(models.Model):
    title = models.CharField(max_length = 100)
    content = models.TextField()
    date_posted = models.DateTimeField(default = timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})

    