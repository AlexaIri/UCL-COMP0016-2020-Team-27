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

    organisation_name = models.CharField(max_length = 255, default = "Default name")
    organisation_address = models.CharField(max_length = 255, default = "Default IXN Subscriber Company")
    organisation_logo = models.ImageField(default='default_logo.png', upload_to='organisations_pics')
    overview = models.CharField(max_length = 5000, default = " Default overview")
    IXN_lead = models.CharField(max_length = 255)

    def save(self):
        super().save()

        img = Image.open(self.organisation_logo.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.organisation_logo.path)


class Post(models.Model):
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})

    title = models.CharField(max_length = 100)
    content = models.TextField()
    date_posted = models.DateTimeField(default = timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

   
    