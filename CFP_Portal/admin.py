from django.contrib import admin
from CFP_Portal.models import Organisation, Post, Person, Review
# Register your models here.
admin.site.register(Organisation)
admin.site.register(Post)
admin.site.register(Person)
admin.site.register(Review)