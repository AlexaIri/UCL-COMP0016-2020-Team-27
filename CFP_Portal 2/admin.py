from django.contrib import admin
from CFP_Portal.models import Organisation, Post, Person, Review, Comment, AcceptedProjects, RejectedProjects
# Register your models here.
admin.site.register(Organisation)
admin.site.register(Post)
admin.site.register(Person)
admin.site.register(Review)
admin.site.register(Comment)
admin.site.register(AcceptedProjects)
admin.site.register(RejectedProjects)