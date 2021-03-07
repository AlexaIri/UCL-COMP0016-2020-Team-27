from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User
from .models import Organisation, Post, Person, Review, Comment, AcceptedProjects, RejectedProjects
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import Proposal
from .forms import Commentform
from .filters import ProjectFilter

# Create your views here.

def index(request):
    item_list = Organisation.objects.all()
    #template = loader.get_template('CFP_Portal/index.html')
    context ={
        'item_list': item_list,
    }
    #return HttpResponse(template.render(context, request))
    return render(request, 'CFP_Portal/index.html', context)

def projectdetail(request, pk):
    project = get_object_or_404(Person, pk=pk)

    if request.method == 'POST' and 'comment' in request.POST:
        print("post!")
        form = Commentform(request.POST)
        if form.is_valid():
            comments = Comment()
            comments.project = project
            comments.name = form.cleaned_data['name']
            comments.feedback = form.cleaned_data['feedback']
            comments.save()
    else:
        form = Commentform()      

    common_tags = project.tags.all()
    commentslist = Comment.objects.all()
    context = {
        'project': project,
        'comments': commentslist,
        'form': form,
        'common_tags':common_tags
    }
    return render(request, 'CFP_Portal/person_detail.html', context)

def projectreviewdetail(request, pk):
    project = get_object_or_404(Person, pk=pk)
    Display = ' '

    if request.method == 'GET' and 'approve' in request.GET:
        Person.objects.filter(pk=pk).update(status='Accepted')
        acceptedproject = AcceptedProjects(project=project)
        acceptedproject.save()
        Display = 'Project has been successfully accepted'
    
    if request.method == 'GET' and 'reject' in request.GET:
       
        Person.objects.filter(pk=pk).update(status='Rejected')
        rejectedproject = RejectedProjects(project=project)
        rejectedproject.save()
        Display = 'Project has been successfully rejected'
    


        
    context = {
        'project': project,
        'Display' : Display
    }
    return render(request, 'CFP_Portal/reviewdetail.html', context)


def markprojectdetail(request, pk):
    model = Review
    review = get_object_or_404(Review, pk=pk)
    context_object_name = 'review'
    context = {
        'review': review,
        # 'comments': commentslist,
        # 'form': form
    }
    return render(request, 'CFP_Portal/mark_project_detail.html', context)

# class MarkProjectDetail(DetailView):
#     model = Review
#     context_object_name = 'review'

def home(request):
    projects = Person.objects.all()
    #return HttpResponse('<h1> Blog Home </h1>')
    totalnumber = Person.objects.all().count()
    acceptednumber = AcceptedProjects.objects.all().count()
    pending = Person.objects.filter(status='Submitted').count()
    context = {
        'projects':projects,
        'totalnumber': totalnumber,
        'acceptednumber':acceptednumber,
        'pending':pending

    }
    return render(request, 'CFP_Portal/home.html', context)

def about(request):
    # context={
        
    # }
    # return render(request, 'CFP_Portal/about.html', context)
    if request.method == "POST":
        
        form = Proposal(request.POST)
        if form.is_valid():
            results = Person()
            results.name = form.cleaned_data['name']
            results.surname = form.cleaned_data['surname']
            results.phone_number = form.cleaned_data['phone_number']
            results.project_title = form.cleaned_data['project_title']
            results.email = form.cleaned_data['email']
            results.summarized_abstract = form.cleaned_data['summarized_abstract']
            results.full_abstract = form.cleaned_data['full_abstract']
            results.expertise_and_skills = form.cleaned_data['expertise_and_skills']
            results.devices = form.cleaned_data['devices']
            results.project_complexity = form.cleaned_data['project_complexity']
            results.source_type = form.cleaned_data['source_type']
            results.ethics_form = form.cleaned_data['ethics_form']
            results.launching_date = form.cleaned_data['launching_date']
            results.motivations = form.cleaned_data['motivations']
            results.importance = form.cleaned_data['importance']
            results.hashtags = form.cleaned_data['hashtags']

            results.save()     
        
        
        # return redirect('/CFP_Portal/SubmissionPortal/Step2')
        return redirect('/CFP_Portal/')
    

    form = Proposal()
    
    return render(request, 'CFP_Portal/about.html', {"form": form})

def projectgrid(request):
    #template = loader.get_template('CFP_Portal/index.html')
    projects = Person.objects.all()

    myFilter = ProjectFilter(request.GET, queryset = projects)
    projects = myFilter.qs
    innovationnumber = Person.objects.filter(project_complexity='Innovation').count()
    scaffoldingnumber = Person.objects.filter(project_complexity='Scaffolding').count()
    discoverynumber = Person.objects.filter(project_complexity='Discovery').count()

    

   
    if request.method == 'GET' and 'innovation' in request.GET:
        projects = Person.objects.filter(project_complexity='Innovation')

    if request.method == 'GET' and 'discovery' in request.GET:
        projects = Person.objects.filter(project_complexity='Discovery')

    if request.method == 'GET' and 'scaffolding' in request.GET:
       projects = Person.objects.filter(project_complexity='Scaffolding')

    context ={
        'projects': projects,
        'myFilter': myFilter,
        'innovationumber': innovationnumber,
        'discoverynumber': discoverynumber,
        'scaffoldingnumber': scaffoldingnumber
    }
    
    #return HttpResponse(template.render(context, request))
    return render(request, 'CFP_Portal/projects_grid.html', context)

def projectlistview(request):
    #template = loader.get_template('CFP_Portal/index.html')
    projects = Person.objects.all()

    myFilter = ProjectFilter(request.GET, queryset = projects)
    projects = myFilter.qs
    innovationnumber = Person.objects.filter(project_complexity='Innovation').count()
    scaffoldingnumber = Person.objects.filter(project_complexity='Scaffolding').count()
    discoverynumber = Person.objects.filter(project_complexity='Discovery').count()


    if request.method == 'GET' and 'innovation' in request.GET:
        projects = Person.objects.filter(project_complexity='Innovation')

    if request.method == 'GET' and 'discovery' in request.GET:
        projects = Person.objects.filter(project_complexity='Discovery')

    if request.method == 'GET' and 'scaffolding' in request.GET:
       projects = Person.objects.filter(project_complexity='Scaffolding')

    context ={
        'projects': projects,
        'myFilter': myFilter,
        'innovationumber': innovationnumber,
        'discoverynumber': discoverynumber,
        'scaffoldingnumber': scaffoldingnumber
    }
    
    #return HttpResponse(template.render(context, request))
    return render(request, 'CFP_Portal/project_listview.html', context)

def rejectedprojects(request):
    #template = loader.get_template('CFP_Portal/index.html')
    rejectedprojects = RejectedProjects.objects.all()

    myFilter = ProjectFilter(request.GET, queryset = rejectedprojects)
    projects = myFilter.qs
    innovationnumber = Person.objects.filter(project_complexity='Innovation').count()
    scaffoldingnumber = Person.objects.filter(project_complexity='Scaffolding').count()
    discoverynumber = Person.objects.filter(project_complexity='Discovery').count()


    if request.method == 'GET' and 'innovation' in request.GET:
        projects = Person.objects.filter(project_complexity='Innovation')

    if request.method == 'GET' and 'discovery' in request.GET:
        projects = Person.objects.filter(project_complexity='Discovery')

    if request.method == 'GET' and 'scaffolding' in request.GET:
       projects = Person.objects.filter(project_complexity='Scaffolding')

    context ={
        'rejectedprojects': rejectedprojects,
        'myFilter': myFilter,
        'innovationumber': innovationnumber,
        'discoverynumber': discoverynumber,
        'scaffoldingnumber': scaffoldingnumber
    }
    
    #return HttpResponse(template.render(context, request))
    return render(request, 'CFP_Portal/rejectedprojects.html', context)


def acceptedprojects(request):
    #template = loader.get_template('CFP_Portal/index.html')
    acceptedprojects = AcceptedProjects.objects.all()

    myFilter = ProjectFilter(request.GET, queryset = acceptedprojects)
    projects = myFilter.qs
    innovationnumber = Person.objects.filter(project_complexity='Innovation').count()
    scaffoldingnumber = Person.objects.filter(project_complexity='Scaffolding').count()
    discoverynumber = Person.objects.filter(project_complexity='Discovery').count()


    if request.method == 'GET' and 'innovation' in request.GET:
        projects = Person.objects.filter(project_complexity='Innovation')
        

    if request.method == 'GET' and 'discovery' in request.GET:
        projects = Person.objects.filter(project_complexity='Discovery')

    if request.method == 'GET' and 'scaffolding' in request.GET:
       projects = Person.objects.filter(project_complexity='Scaffolding')

    context ={
        'acceptedprojects': acceptedprojects,
        'myFilter': myFilter,
        'innovationumber': innovationnumber,
        'discoverynumber': discoverynumber,
        'scaffoldingnumber': scaffoldingnumber
    }
    
    #return HttpResponse(template.render(context, request))
    return render(request, 'CFP_Portal/acceptedprojects.html', context)


class OrganisationListView(ListView):
    model = Organisation
    template_name ='CFP_Portal/organisation_list.html'
    context_object_name = 'organisations'
    paginate_by = 5
    
class ReviewsListView(ListView):
    model = Review
    template_name = 'CFP_Portal/reviews.html'
    context_object_name = 'reviews'

class ReviewsDisplayListView(ListView):
    model = Person.objects.filter(project_complexity='Innovation')
    template_name = 'CFP_Portal/review_display.html'
    context_object_name = 'projects'

def reviewdisplay(request):
    projects = Person.objects.filter(status='Submitted')
    #template = loader.get_template('CFP_Portal/index.html')
    context ={
        'projects': projects,
    }
    #return HttpResponse(template.render(context, request))
    return render(request, 'CFP_Portal/review_display.html', context)

class UsersListView(ListView):
    model = Organisation
    template_name ='CFP_Portal/users_grid.html'

class ProjectsListView(ListView):
    model = Person
    context_object_name = 'projects'
    
    template_name ='CFP_Portal/projects_grid.html'


class HomeProjectListView(ListView, ): # this is the former PostListView
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
    context_object_name = 'project'
   
class ReviewDetailView(DetailView):
    model = Review
    context_object_name = 'review'
    
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
        print("unvalid")
        print(form.errors)
        if form.is_valid():
            print("valid!")
            user = User.objects.get(pk=request.user.id)
            project = form.save(commit=False)
            project.status = 'Submitted'
            project.department = user.profile.department
            project.department = user.profile.organisation
            project.save()
            form.save_m2m()
                    

            
        item_list = Person.objects.all()
        #
        return redirect('/CFP_Portal/')
    

    form = Proposal()
    
    return render(request, 'CFP_Portal/submission_portal.html', {"form": form})

# def SubmissionPortal(request):
    
#     if request.method == "POST":
        
#         form = Proposal(request.POST)

#         if form.is_valid():
           
#             user = User.objects.get(pk=request.user.id)
     
#             results = Person()
#             results.name = form.cleaned_data['name']
#             results.surname = form.cleaned_data['surname']
#             results.phone_number = form.cleaned_data['phone_number']
#             results.project_title = form.cleaned_data['project_title']
#             results.title = form.cleaned_data['title']
#             results.email = form.cleaned_data['email']
#             results.summarised_abstract = form.cleaned_data['summarised_abstract']
#             results.full_abstract = form.cleaned_data['full_abstract']
#             results.expertiseskills = form.cleaned_data['expertiseskills']
#             results.devices = form.cleaned_data['devices']
#             results.project_complexity = form.cleaned_data['project_complexity']
#             results.source_type = form.cleaned_data['source_type']
#             results.ethics_form = form.cleaned_data['ethics_form']
#             results.launching_date = form.cleaned_data['launching_date']
#             results.motivations = form.cleaned_data['motivations']
#             results.importance = form.cleaned_data['importance']
#             results.hashtags = form.cleaned_data['hashtags']
#             results.department = user.profile.department
#             results.organisation = user.profile.organisation
            
#             results.status = 'Submitted'

#             results.save() 
            
            
       
#         #
#         return redirect('/CFP_Portal/')

#     else:

#         form = Proposal()
        
#     return render(request, 'CFP_Portal/submission_portal.html', {"form": form})
 

