from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Organisation, Post

# posts = [
#     {
#         'author': 'CoreyMS',
#         'title': 'Blog Post 1',
#         'content': 'First post content',
#         'date_posted': 'August 27, 2018'
#     },
#     {
#         'author': 'Jane Doe',
#         'title': 'Blog Post 2',
#         'content': 'Second post content',
#         'date_posted': 'August 28, 2018'
#     }
# ]


# Create your views here.
def helloWorld(request):
    return HttpResponse('hello world')

def index(request):
    item_list = Organisation.objects.all()
    #template = loader.get_template('CFP_Portal/index.html')
    context ={
        'item_list': item_list,
    }
    #return HttpResponse(template.render(context, request))
    return render(request, 'CFP_Portal/index.html', context)

def home(request):
    #return HttpResponse('<h1> Blog Home </h1>')
    context = {
        'posts':Post.objects.all()
    }
    return render(request, 'CFP_Portal/home.html', context)

def about(request):
    #return HttpResponse('<h1> Blog About </h1>')
    return render(request, 'CFP_Portal/about.html', "title: About")