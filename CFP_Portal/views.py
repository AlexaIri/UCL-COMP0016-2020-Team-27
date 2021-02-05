from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User
from .models import Organisation, Post, Person, Review
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import Proposal, Proposal2, Proposal3, Proposal4

# Create your views here.

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
        'project':Person.objects.all()
    }
    return render(request, 'CFP_Portal/home.html', context)

def about(request):
    # context={
        
    # }
    # return render(request, 'CFP_Portal/about.html', context)
    if request.method == "POST":
        
        form = Proposal(request.POST)
        if form.is_valid():
            form.save()
        item_list = Person.objects.all()        
        
        
        # return redirect('/CFP_Portal/SubmissionPortal/Step2')
        return redirect('/CFP_Portal/')
    

    form = Proposal()
    
    return render(request, 'CFP_Portal/about.html', {"form": form})


class OrganisationListView(ListView):
    model = Organisation
    template_name ='CFP_Portal/organisation_list.html'
    context_object_name = 'organisations'
    paginate_by = 5
    
class ReviewsListView(ListView):
    model = Post
    template_name ='CFP_Portal/reviews.html'
    context_object_name = 'posts'
    ordering = ['date_posted']
    paginate_by = 5

class UsersListView(ListView):
    model = Organisation
    template_name ='CFP_Portal/users_grid.html'

class ProjectsListView(ListView):
    model = Person
    template_name ='CFP_Portal/projects_grid.html'

class HomeProjectListView(ListView): # this is the former PostListView
    model = Person # for the project
    template_name ='CFP_Portal/home.html'
    context_object_name = 'projects'
    #ordering = ['date_posted']
    paginate_by = 5

class PostDetailView(DetailView):
    model = Post

class OrganisationDetailView(DetailView):
    model = Organisation
    context_object_name = 'organisations'

class ProjectDetailView(DetailView):
    model = Person
    context_object_name = 'projects'

class ReviewDetailView(DetailView):
    model = Review
    context_object_name = 'reviews'
    
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self): # other users are not allowed to update the feedback forms except for the original author
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
        #return super().test_func()

class OrganisationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Organisation
    fields = ['organisation_name', 'overview', 'organisation_address']

    def form_valid(self, form):
        organisation = self.get_object()
        form.instance.IXN_lead = self.organisation.IXN_lead #todo: change here to update!!!
        return super().form_valid(form)

    def test_func(self): # other IXN_leads are not allowed to update the organisation details except for the original lead
        organisation = self.get_object()
        # if self.request.user == organisation.IXN_lead:
        #     return True
        # return False
        return True
        #return super().test_func()

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url ='/'

    def test_func(self): # other users are not allowed to delete the feedback forms except for the original author
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
        #return super().test_func()

class OrganisationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Organisation
    success_url ='/'

    def test_func(self): # other users are not allowed to delete the feedback forms except for the original author
        organisation = self.get_object()
        # if self.request.user == organisation.IXN_lead:
        #     return True
        # return False
        return True
        #return super().test_func()

class UserPostListView(ListView):
    model = Post
    template_name ='CFP_Portal/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username = self.kwargs.get('username'))
        return Post.objects.filter(author = user).order_by('-date_posted')


def SubmissionPortal(request):
    
    if request.method == "POST":
        
        form = Proposal(request.POST)
        if form.is_valid():
            form.save()
        item_list = Person.objects.all()        
        
        
        return redirect('/CFP_Portal/SubmissionPortal/Step2')
        # return redirect('/CFP_Portal/')
    

    form = Proposal()
    
    return render(request, 'CFP_Portal/submission_portal.html', {"form": form})

    # name = request. POST["name"]
    # surname = request.POST["surname"]
    # phone_number = request.POST["phone_number"]
    # email = request.POST["email"]
    # project_title = request.POST["project_title"]

    # projectObject = Person(name= name, surname = surname, phone_number = phone_number, email = email, project_title = project_title)
    # projectObject.save()
    # return render(request, 'CFP_Portal/submission_portal.html')

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