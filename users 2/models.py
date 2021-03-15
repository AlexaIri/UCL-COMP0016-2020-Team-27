from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    department = models.CharField(max_length = 255, default = "", blank=True)
    organisation = models.CharField(max_length = 255, default = "", blank=True)
    organisation_address = models.CharField(max_length = 255, default = "", blank=True)
    full_name = models.CharField(max_length = 255, default = "")

    about = models.TextField(default="")
    

    

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
       

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)