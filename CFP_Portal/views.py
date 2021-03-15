from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User, Group
from .models import Organisation, Post, Person, Review, Comment, RejectedProjects, AcceptedProjects
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import Proposal, ReviewForm
from .forms import Commentform
from .filters import ProjectFilter
from django.contrib.auth.decorators import login_required, user_passes_test
from django import template
import csv
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models.functions import Lower
from django.urls import reverse
from django.shortcuts import redirect

register = template.Library()

# Create your views here.
@register.filter(name='has_group')
def has_group(user, group_name): 
    group = Group.objects.get(name=group_name) 
    return True if group in user.groups.all() else False

def is_user(user):
    
    return user.is_superuser or user.is_staff or user.groups.filter(name__in=['Submitters','Reviewers','Approvers']).exists()
    # print(user.groups)

def is_reviewer(user):
    
    return user.is_superuser or user.is_staff or user.groups.filter(name__in=['Reviewers','Approvers']).exists()

def is_submitter(user):
    return user.groups.filter(name__in=['Submitters']).exists()
    # print(user.groups)
   

def is_lead(user):  
    # print(user.groups)
    return  user.is_superuser or user.is_staff or user.groups.filter(name__in=['Approvers']).exists()

def export(request):
    response = HttpResponse(content_type ='text/csv')
    writer = csv.writer(response)
    writer.writerow(['Name', 'Phone Number', 'Email', 'Title', 'Project Title', 'Summarised Abstract', 'Full Abstract', 'Department', 'Organisation', 'Expertise Skills', 'Devices and Technologies', 'Project Complexity', 'Completion of form', 'Source type', 'Launching date', 'Motivations', 'Tags', 'Status', 'NICEtier'])


    for project in Person.objects.all().values_list('name', 'phone_number', 'email', 'title', 'project_title', 'summarised_abstract', 'full_abstract', 'department', 'organisation', 'expertiseskills', 'devices', 'project_complexity', 'ethics_form','source_type', 'launching_date', 'motivations', 'tags__name', 'status', 'NICEtier'):
        writer.writerow(project)
    response['Content-Disposition'] = 'attachment; filename ="projects.csv"'

    return response
@login_required
@user_passes_test(is_reviewer)
def index(request):
    item_list = Organisation.objects.all()
    #template = loader.get_template('CFP_Portal/index.html')
    context ={
        'item_list': item_list,
    }
    #return HttpResponse(template.render(context, request))
    return render(request, 'CFP_Portal/index.html', context)

@login_required
@user_passes_test(is_user)
def projectdetail(request, pk):
    project = get_object_or_404(Person, pk=pk)

    group = ''
    if request.user.groups.filter(name__in=['Submitters']).exists():
        group = 'Submitters'
    
    reviewers = User.objects.filter(groups__name__in=['Reviewers','Approvers',])
    #reviewers = User.objects.filter(groups__name='Reviewers')

    if request.method == 'POST' and 'comment' in request.POST:
        
        form = Commentform(request.POST)
        if form.is_valid():
            user = User.objects.get(pk=request.user.id)
            comments = Comment()
            comments.project = project
            comments.name = user.profile.full_name
            comments.feedback = form.cleaned_data['feedback']
            comments.save()
    else:
        form = Commentform()     

    if request.method == 'POST' and 'reviewers' in request.POST:
        
        for item in request.POST.getlist('options'):
            project.reviewers.add(item)
        #Person.objects.filter(id=pk).update(reviewers=request.POST.getlist('options'))
        
    

    common_tags = project.tags.all()
    commentslist = Comment.objects.all()
    context = {
        'project': project,
        'comments': commentslist,
        'form': form,
        'common_tags':common_tags,
        'group': group,
        'reviewers' : reviewers
    }
    return render(request, 'CFP_Portal/person_detail.html', context)

@login_required
@user_passes_test(is_reviewer)
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


    
@login_required
@user_passes_test(is_user)
def home(request):
    order_by = request.GET.get('order_by')
    projects = Person.objects.order_by('-submission_date')

    
    paginator = Paginator(projects, 10)
    page = request.GET.get('page', 1)
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        projects = paginator.page(1)
    except EmptyPage:
        projects = paginator.page(paginator.num_pages)

    acceptednumber = AcceptedProjects.objects.all().count()
    pending = Person.objects.filter(status__in =['Submitted', 'Under Review']).count()
    
    group =''
    if request.user.groups.filter(name__in=['Submitters']).exists():
        group = 'Submitters'

    individualprojects = Person.objects.filter(user=request.user)
    individualaccepted= Person.objects.filter(user=request.user, status='Accepted').count()
    individualrejected= Person.objects.filter(user=request.user, status='Rejected').count()
    individualpending = Person.objects.filter(user=request.user, status__in =['Submitted', 'Under Review']).count()
    
    
    if 'search' in request.GET:
        
        search_term = request.GET['search']
        projects = Person.objects.all().filter(project_title__icontains=search_term).order_by('-submission_date')
    
    
         
    if request.method == 'GET' and 'allprojects' in request.GET:
        
        projects = Person.objects.all()
    

    if request.method == 'GET' and 'assigned' in request.GET:
        projects = Person.objects.filter(reviewers=request.user)
    
   
    
    #return HttpResponse('<h1> Blog Home </h1>')
    totalnumber = Person.objects.all().count()
    
    context = {
        'projects':projects,
        'totalnumber': totalnumber,
        'acceptednumber':acceptednumber,
        'pending': pending,
        'individualprojects': individualprojects,
        'group' : group, 
        'individualaccepted' : individualaccepted,
        'individualpending' : individualpending
        # 'all_projects':all_projects,
        # 'order_by': order_by
    }
    # table = PeopleTable(projects)
    # table.paginate(page=request.GET.get("page", 1), per_page=5)
   
    return render(request, 'CFP_Portal/home.html', context)





@login_required
@user_passes_test(is_reviewer)
def projectgrid(request):
      #template = loader.get_template('CFP_Portal/index.html')
    projects = Person.objects.order_by('-submission_date')
   
    

    myFilter = ProjectFilter(request.GET, queryset = projects)
    projects = myFilter.qs
    innovationnumber = Person.objects.filter(project_complexity='Innovation').count()
    scaffoldingnumber = Person.objects.filter(project_complexity='Scaffolding').count()
    discoverynumber = Person.objects.filter(project_complexity='Discovery').count()

    if request.method == 'GET' and 'innovation' in request.GET:
        projects = Person.objects.filter(project_complexity='Innovation').order_by('-submission_date')

    if request.method == 'GET' and 'discovery' in request.GET:
        projects = Person.objects.filter(project_complexity='Discovery').order_by('-submission_date')

    if request.method == 'GET' and 'scaffolding' in request.GET:
       projects = Person.objects.filter(project_complexity='Scaffolding').order_by('-submission_date')
    
    if request.method == 'GET' and 'assigned' in request.GET:
        projects = Person.objects.filter(reviewers=request.user).order_by('-submission_date')

    context ={
        'projects': projects,
        'myFilter': myFilter,
        'innovationumber': innovationnumber,
        'discoverynumber': discoverynumber,
        'scaffoldingnumber': scaffoldingnumber
    }
    
    #return HttpResponse(template.render(context, request))
    return render(request, 'CFP_Portal/projects_grid.html', context)

@login_required
@user_passes_test(is_reviewer)
def detail(request, project_id, review_id):
    project = get_object_or_404(Person, pk=project_id)
    review = get_object_or_404(Review, pk = review_id)
    return render(request, 'CFP_Portal/detail.html', {'project': project, 'review':review, 'reviews': Review.objects.filter(project_id=project_id)})

@login_required
@user_passes_test(is_user)
def review(request, review_id):
    # project = get_object_or_404(Person, pk=project_id)
    group = ''
    if request.user.groups.filter(name__in=['Submitters']).exists():
        group = 'Submitters'
    
    review = get_object_or_404(Review, pk = review_id)
    context = {
        'review': review,
        'group': group
    }
        
    
    return render(request, 'CFP_Portal/review.html', context)

@login_required
@user_passes_test(is_user)
def projectreviewdetail(request, project_id):
    project = get_object_or_404(Person, pk=project_id)
    Display = ' '
    if request.user.groups.filter(name__in=['Approvers']).exists():
        group = 'Approvers'

    if request.method == 'GET' and 'approve' in request.GET:
        Person.objects.filter(id=project_id).update(status='Accepted')
        acceptedproject = AcceptedProjects(project=project)
        acceptedproject.save()
        Display = 'Project has been successfully accepeted'
    
    if request.method == 'GET' and 'reject' in request.GET:
        
        Person.objects.filter(id=project_id).update(status='Rejected')
        rejectedproject = RejectedProjects(project=project)
        rejectedproject.save()
        Display = 'Project has been successfully rejected'
    
    group = ''
    if request.user.groups.filter(name__in=['Submitters']).exists():
        group = 'Submitters'
        
        
    context = {
        'project': project,
        'reviews': Review.objects.filter(project_id=project_id),
        'Display' : Display,
        'group' : group
    }

    return render(request, 'CFP_Portal/reviewdetail.html', context)

@login_required
@user_passes_test(is_reviewer)
def projectlistview(request):
    #template = loader.get_template('CFP_Portal/index.html')
    projects = Person.objects.order_by('-submission_date')

    myFilter = ProjectFilter(request.GET, queryset = projects)
    projects = myFilter.qs
    innovationnumber = Person.objects.filter(project_complexity='Innovation').count()
    scaffoldingnumber = Person.objects.filter(project_complexity='Scaffolding').count()
    discoverynumber = Person.objects.filter(project_complexity='Discovery').count()


    if request.method == 'GET' and 'innovation' in request.GET:
        projects = Person.objects.filter(project_complexity='Innovation').order_by('-submission_date')

    if request.method == 'GET' and 'discovery' in request.GET:
        projects = Person.objects.filter(project_complexity='Discovery').order_by('-submission_date')

    if request.method == 'GET' and 'scaffolding' in request.GET:
       projects = Person.objects.filter(project_complexity='Scaffolding').order_by('-submission_date')

    context ={
        'projects': projects,
        'myFilter': myFilter,
        'innovationumber': innovationnumber,
        'discoverynumber': discoverynumber,
        'scaffoldingnumber': scaffoldingnumber
    }
    
    #return HttpResponse(template.render(context, request))
    return render(request, 'CFP_Portal/project_listview.html', context)

@login_required
@user_passes_test(is_reviewer)
def rejectedprojects(request):
    #template = loader.get_template('CFP_Portal/index.html')
    rejectedprojects = RejectedProjects.objects.order_by('-date_accepted')

    myFilter = ProjectFilter(request.GET, queryset = rejectedprojects)
    projects = myFilter.qs
    innovationnumber = RejectedProjects.objects.filter(project__project_complexity='Innovation').count()
    scaffoldingnumber = RejectedProjects.objects.filter(project__project_complexity='Scaffolding').count()
    discoverynumber = RejectedProjects.objects.filter(project__project_complexity='Discovery').count()


    if request.method == 'GET' and 'innovation' in request.GET:
        projects = Person.objects.filter(project_complexity='Innovation').order_by('-date_accepted')

    if request.method == 'GET' and 'discovery' in request.GET:
        projects = Person.objects.filter(project_complexity='Discovery').order_by('-date_accepted')

    if request.method == 'GET' and 'scaffolding' in request.GET:
       projects = Person.objects.filter(project_complexity='Scaffolding').order_by('-date_accepted')

    context ={
        'rejectedprojects': rejectedprojects,
        'myFilter': myFilter,
        'innovationumber': innovationnumber,
        'discoverynumber': discoverynumber,
        'scaffoldingnumber': scaffoldingnumber
    }
    
    #return HttpResponse(template.render(context, request))
    return render(request, 'CFP_Portal/rejectedprojects.html', context)

@login_required
@user_passes_test(is_reviewer)
def acceptedprojects(request):
    #template = loader.get_template('CFP_Portal/index.html')
    acceptedprojects = AcceptedProjects.objects.order_by('-date_accepted')

    myFilter = ProjectFilter(request.GET, queryset = acceptedprojects)
    projects = myFilter.qs
    innovationnumber = AcceptedProjects.objects.filter(project__project_complexity='Innovation').count()
    scaffoldingnumber = AcceptedProjects.objects.filter(project__project_complexity='Scaffolding').count()
    discoverynumber = AcceptedProjects.objects.filter(project__project_complexity='Discovery').count()


    if request.method == 'GET' and 'innovation' in request.GET:
        projects = Person.objects.filter(project_complexity='Innovation').order_by('-date_accepted')

    if request.method == 'GET' and 'discovery' in request.GET:
        projects = Person.objects.filter(project_complexity='Discovery').order_by('-date_accepted')

    if request.method == 'GET' and 'scaffolding' in request.GET:
       projects = Person.objects.filter(project_complexity='Scaffolding').order_by('-date_accepted')

    if request.method == 'GET' and 'approve' in request.GET:
        response = HttpResponse(content_type ='text/csv')
        writer = csv.writer(response)
        writer.writerow(['Name', 'Phone Number', 'Email', 'Title', 'Project Title', 'Summarised Abstract', 'Full Abstract', 'Department', 'Organisation', 'Expertise Skills', 'Devices and Technologies', 'Project Complexity', 'Completion of form', 'Source type', 'Launching date', 'Motivations', 'Tags', 'Status', 'NICEtier'])
        for project in Person.objects.all().values_list('name', 'phone_number', 'email', 'title', 'project_title', 'summarised_abstract', 'full_abstract', 'department', 'organisation', 'expertiseskills', 'devices', 'project_complexity', 'ethics_form','source_type', 'launching_date', 'motivations', 'tags__name', 'status', 'NICEtier'):
             writer.writerow(project)
        response['Content-Disposition'] = 'attachment; filename ="acceptedprojects.csv"'
        return response

    context ={
        'acceptedprojects': acceptedprojects,
        'myFilter': myFilter,
        'innovationumber': innovationnumber,
        'discoverynumber': discoverynumber,
        'scaffoldingnumber': scaffoldingnumber
    }
    
    #return HttpResponse(template.render(context, request))
    return render(request, 'CFP_Portal/acceptedprojects.html', context)

@login_required
@user_passes_test(is_reviewer)  
class OrganisationListView(ListView):
    model = Organisation
    template_name ='CFP_Portal/organisation_list.html'
    context_object_name = 'organisations'
    paginate_by = 5

@login_required
@user_passes_test(is_reviewer)  
class ReviewsListView(ListView):
    model = Review
    template_name = 'CFP_Portal/reviews.html'
    context_object_name = 'reviews'

@login_required
@user_passes_test(is_reviewer)
class  ReviewsDisplayListView(ListView):
    model = Person
    template_name = 'CFP_Portal/review_display.html'
    context_object_name = 'projects'

@login_required
@user_passes_test(is_reviewer)
def reviewdisplay(request):
    projects = Person.objects.filter(reviewers=request.user).order_by('-submission_date')
   
    if request.method == 'GET' and 'projects' in request.GET:
        projects = Person.objects.filter(reviewers=request.user, status__in=['Submitted','Under Review']).order_by('-submission_date')
 
    if request.method == 'GET' and 'allprojects' in request.GET:
        projects = Person.objects.order_by('-submission_date')

    if request.method == 'GET' and 'assigned' in request.GET:
        projects = Person.objects.filter(reviewers=request.user).order_by('-submission_date')
        
    context = {
        'projects' : projects

        # 'comments': commentslist,
        # 'form': form
    }
   
    return render(request, 'CFP_Portal/review_display.html', context)
@login_required
@user_passes_test(is_reviewer)
class  Trial(ListView):
    model = Person
    template_name = 'CFP_Portal/trial.html'
    context_object_name = 'projects'

@login_required
@user_passes_test(is_reviewer)
def UserDisplay(request):
    users = User.objects.all()
    title = 'All Users'

    if request.method == 'GET' and 'reviewers' in request.GET:
        users = User.objects.filter(groups__name='Reviewers')
        title = 'Reviewers'
    
    if request.method == 'GET' and 'submitters' in request.GET:
        users = User.objects.filter(groups__name='Submitters')
        title = 'Submitters'
    
    if request.method == 'GET' and 'leads' in request.GET:
        users = User.objects.filter(groups__name='Approvers')
        title = 'Approvers'
   
    if request.method == 'GET' and 'allusers' in request.GET:
        users = User.objects.all()
        title = 'All users'
    
        
    context = {
        'users' : users,
        'title' : title

        # 'comments': commentslist,
        # 'form': form
    }
   
    return render(request, 'CFP_Portal/users.html', context)

@login_required
@user_passes_test(is_reviewer)
class ProjectsListView(ListView):
    model = Person
    context_object_name = 'projects'
    
    template_name ='CFP_Portal/projects_grid.html'

@login_required
@user_passes_test(is_reviewer)
class HomeProjectListView(ListView, ): # this is the former PostListView
    model = Person # for the project
    template_name ='CFP_Portal/home.html'
    context_object_name = 'projects'
    #ordering = ['date_posted']
    paginate_by = 5
@login_required
@user_passes_test(is_reviewer)
class PostDetailView(DetailView):
    model = Post
@login_required
@user_passes_test(is_reviewer)
class OrganisationDetailView(DetailView):
    model = Organisation
    context_object_name = 'organisations'
@login_required
@user_passes_test(is_reviewer)
class ProjectDetailView(DetailView):
    
    model = Person
    context_object_name = 'project'
@login_required
@user_passes_test(is_reviewer)  
class ReviewDetailView(DetailView):
    model = Review
    context_object_name = 'review'
@login_required
@user_passes_test(is_reviewer)    
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
@login_required
@user_passes_test(is_reviewer)
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
@login_required
@user_passes_test(is_reviewer)
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
@login_required
@user_passes_test(is_reviewer)
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url ='/'

    def test_func(self): # other users are not allowed to delete the feedback forms except for the original author
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
        #return super().test_func()
@login_required
@user_passes_test(is_reviewer)
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

@login_required
@user_passes_test(is_reviewer)  
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
        
        form = Proposal(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():

           
            user = User.objects.get(pk=request.user.id)
            project = form.save(commit=False)
            project.status = 'Submitted'
            project.department = user.profile.department
            project.organisation = user.profile.organisation
            project.user = user
            project.save()
            form.save_m2m()
            # item_list = Person.objects.all()
            # return redirect("/CFP_Portal/project/", pk=project.id)
                    

            
        item_list = Person.objects.all()
        
        return redirect('/CFP_Portal/')
    

    form = Proposal()
    
    return render(request, 'CFP_Portal/submission_portal.html', {"form": form})
    
    # def get_redirect_url(self, pk):
    #     # article = Article.objects.get(pk=pk)
    #     # slug = article.slug
    #     return reverse('project', args=(pk))

    # my_id_project = 0
  
    # if request.method == "POST":
        
    #     form = Proposal(request.POST)
        
    #     print(form.errors)
    #     if form.is_valid():

           
    #         user = User.objects.get(pk=request.user.id)
    #         project = form.save(commit=False)
    #         project.status = 'Submitted'
    #         project.department = user.profile.department
    #         project.department = user.profile.organisation
    #         project.user = user
    #         project.save()
    #         form.save_m2m()
    #         my_id_project = project.id
    #         print("heeeereee", project.id)
                    

            
    #         item_list = Person.objects.all()
    #         return redirect('CFP_Portal/')
    #         # return get_redirect_url(project.id)
    #         # return redirect("project", pk=project.id)
       
    # form = Proposal()
    
    # return render(request, 'CFP_Portal/submission_portal.html', {"form": form})

    

 
@login_required
@user_passes_test(is_reviewer)
def ReviewPortal(request, project_id):
    projects= get_object_or_404(Person, pk=project_id)
    

    if request.method == "POST":

        # project =  get_object_or_404(Person, pk=project_id)
        data = {
        'id': project_id,
        'project': Person.objects.all(),
    }
        form = ReviewForm(request.POST)
        
        if form.is_valid():
            results = Review()
            model = Person
            context_object_name = 'project'

            # project = Person.objects.get(pk=**kwargs['intervention_pk'])

            # results2 = Person()
            
            results.project = projects
            # results.project = form.cleaned_data['project']
            
            results.project.status = "Reviewed"
            results.reviewer_name = request.user.profile.full_name
            
            results.reviewer_email = request.user.email
            results.comments = form.cleaned_data['comments']

            results.interoperabilityComments = form.cleaned_data['standards_and_interoperability_comments']
            results.technical_strengthComments = form.cleaned_data['technical_and_scientific_strength_comments']
            results.user_designComments = form.cleaned_data['user_centred_design_comments']
            results.usabilityTestingComments = form.cleaned_data['usability_testing_comments']
            results.researchQualityComments = form.cleaned_data['research_quality_comments']
            results.scalabilityComments = form.cleaned_data['scalability_comments']
            results.resilienceComments = form.cleaned_data['resilience_comments']

            results.interoperabilityPoints = form.cleaned_data['standards_and_interoperability_points']
            results.technical_strengthPoints = form.cleaned_data['technical_and_scientific_strength_points']
            results.user_designPoints = form.cleaned_data['user_centred_design_points']
            results.scalabilityPoints = form.cleaned_data['scalability_points']
            results.resiliencePoints = form.cleaned_data['resilience_points']
            results.usabilityTestingPoints = form.cleaned_data['usability_testing_points']
            results.researchQualityPoints = form.cleaned_data['research_quality_points']
            results.RAGlevel = request.POST.get('options')
            Person.objects.filter(id=project_id).update(status='Under Review')
            
             
            # results2.status = 'Reviewed'

            results.save() 
            item_list = Review.objects.all()
            return redirect('/CFP_Portal/reviewDisplay')
    else:
        form = ReviewForm()

    model = Review
    context_object_name = 'review'
    # review = get_object_or_404(Review, project_id=project_id)
   
    context = {
        'review': review,
        'form': form,        
        # 'project': Person.objects.filter(pk=project_id) # there will be exactly one project with that project_id 

    }
    
    return render(request, 'CFP_Portal/review_portal.html', context)

# def markprojectdetail(request, pk):
#     model = Review
#     review = get_object_or_404(Review, pk=pk)
#     context_object_name = 'review'
#     context = {
#         'review': review,
#         # 'comments': commentslist,
#         # 'form': form
#     }
#     return render(request, 'CFP_Portal/mark_project_detail.html', context)

# def projectreviewdetail(request, project_id):
#     project = get_object_or_404(Person, pk=project_id)
        
#     context = {
#         'project': project,
#         'reviews': Review.objects.filter(project_id=project_id)
#     }
#     return render(request, 'CFP_Portal/reviewdetail.html', context)


 

