from django.db import models

# Create your models here.
class Organisation(models.Model):

    def __str__(self):
        return self.organisation_name

    organisation_name = models.CharField(max_length = 255, default = "Default name")
    organisation_address = models.CharField(max_length = 255, default = "Default IXN Subscriber Company")
    overview = models.CharField(max_length = 5000, default = " Default overview")
    IXN_lead = models.CharField(max_length = 255)


