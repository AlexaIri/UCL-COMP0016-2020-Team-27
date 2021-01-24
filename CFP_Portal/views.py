from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Organisation

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