from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from .models import Organisation
from .models import Person
from .forms import Proposal, Proposal2, Proposal3, Proposal4

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

def SubmissionPortal(request):
    
    if request.method == "POST":
        
        form = Proposal(request.POST)
        if form.is_valid():
            form.save()
        item_list = Person.objects.all()
        #template = loader.get_template('CFP_Portal/index.html')
        
        
        
        return redirect('/CFP_Portal/SubmissionPortal/Step2')
    

    form = Proposal()
    
    #return HttpResponse(template.render(context, request))
    return render(request, 'CFP_Portal/submission_portal.html', {"form": form})

def Submission2(request):
    
    if request.method == "POST":
        
        form = Proposal2(request.POST)
        if form.is_valid():
            form.save()
        item_list = Person.objects.all()
        #template = loader.get_template('CFP_Portal/index.html')
        context =  {'item_list': item_list,}
        
        
        return redirect('/CFP_Portal/SubmissionPortal/Step3')
    

    form = Proposal2()
    
    #return HttpResponse(template.render(context, request))
    return render(request, 'CFP_Portal/submission/step2.html', {"form": form})

def Submission3(request):
    
    if request.method == "POST":
        
        form = Proposal3(request.POST)
        if form.is_valid():
            form.save()
        item_list = Person.objects.all()
        #template = loader.get_template('CFP_Portal/index.html')
        context =  {'item_list': item_list,}
        
        return redirect('/CFP_Portal/SubmissionPortal/Step4')
    
    form = Proposal3()
    
    #return HttpResponse(template.render(context, request))
    return render(request, 'CFP_Portal/submission/step3.html', {"form": form})

def Submission4(request):
        
    if request.method == "POST":
        
        form = Proposal4(request.POST)
        if form.is_valid():
            form.save()
        item_list = Person.objects.all()
        #template = loader.get_template('CFP_Portal/index.html')
        context =  {'item_list': item_list,}
        
        return render(request, 'CFP_Portal/success.html/')
    
    form = Proposal4()
    
    #return HttpResponse(template.render(context, request))
    return render(request, 'CFP_Portal/submission/step4.html', {"form": form})