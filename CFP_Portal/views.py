from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User, Group
from .models import Organisation, Post, Person, Review, Comment, RejectedProjects, AcceptedProjects, UnderReviewProjects
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import Proposal, ReviewForm, Feedback
from .forms import Commentform
from .filters import ProjectFilter
from django.contrib.auth.decorators import login_required, user_passes_test
from django import template
import csv
from . import forms
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models.functions import Lower
from django.urls import reverse
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.conf import settings

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
@user_passes_test(is_reviewer)
def about(request):
    
    #template = loader.get_template('CFP_Portal/index.html')

    #return HttpResponse(template.render(context, request))
    return render(request, 'CFP_Portal/about.html')


@login_required
@user_passes_test(is_user)
def viewdetailsproject(request):

    project = Person.objects.latest('id')
    context ={
        'project': project,
    }
    return render(request, 'CFP_Portal/viewdetailsproject.html', context)

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

    # for user in project.reviewers.all:
    #     email = user.email
    #     send_mail(
    #         'You have a project assigned to review',
    #         'Dear Reviewer, \n The IXN CFP Portal Engine Team is reaching in order to inform you upon the most recent assignment that you have received. There is a project waiting to be reviewed and the complete list of all the projects to be reviewed can be found in the home page or in the projects grid when pressing the Projects Assigned to Me button. \n\n Thank you in advance for your cooperation! \n\n Best wishes, \n Call-for-projects Portal Team ', 
    #         settings.EMAIL_HOST_USER,
    #         [email],
    #         fail_silently=True
    #     )
        
        
            # send_mail('You have a project assigned to review',   
            # 'Dear Reviewer, \n The IXN CFP Portal Engine Team is reaching in order to inform you upon the most recent assignment that you have received. There is a project waiting to be reviewed and the complete list of all the projects to be reviewed can be found in the home page or in the projects grid when pressing the Projects Assigned to Me button. \n\n Thank you in advance for your cooperation! \n\n Best wishes, \n Call-for-projects Portal Team ',    settings.EMAIL_HOST_USER,    #from
            # [project.reviewers.email],    #to
            # fail_silently=True
            # )
            
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
    group = ''
  
    if request.user.groups.filter(name__in=['Approvers']).exists():
        group = 'Approvers'

    if request.method == 'GET' and 'approve' in request.GET:
        Person.objects.filter(id=project_id).update(status='Accepted')
        acceptedproject = AcceptedProjects(project=project)
        acceptedproject.save()
        Display = 'Project has been successfully accepeted'
        
        send_mail(
            'The waiting is over! Your project proposal is successful!',   #subject line
            'Congratulations upon your successful project proposal.\n The IXN CFP reviewing committee is pleased to announce that they came to a consensus and the result is the one you were waiting for. Your project has been accepted by the majority of the reviewers in our panel and will move forward towards our partner university students. We will come back with specific details on the next stages.\n\n Best wishes, \n Call-for-projects Portal Team ',    #message
            settings.EMAIL_HOST_USER,    #from
            [project.email],    #to
            fail_silently=True
        )
    
    if request.method == 'GET' and 'reject' in request.GET:
        
        Person.objects.filter(id=project_id).update(status='Rejected')
        rejectedproject = RejectedProjects(project=project)
        rejectedproject.save()
        Display = 'Project has been successfully rejected'
        send_mail(
            'The waiting is over! Unfortunately, your project proposal is unsuccessful!',   #subject line
            'We are sorry to announce that your project proposal is unsuccessful.\n The IXN CFP reviewing committee have debated for some time now and carefully reviewed all the key features of your project. Your project has been rejected by the majority of the reviewers in our panel and will therefore not move forward towards our partner university students. But do not get discouraged! It was just a learning experience and you have the opportunity to visualise the read-only comprehensive feedback and comments from all the reviwers. We are looking forward to seeing your ideas and projects put into place in the next round! Good luck with all your future endevours!\n\n Best wishes, \n Call-for-projects Portal Team ',    #message
            settings.EMAIL_HOST_USER,    #from
            [project.email],    #to
            fail_silently=True
        )
   
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


    paginator = Paginator(acceptedprojects, 10)
    page = request.GET.get('page', 1)
    try:
        acceptedprojects_page = paginator.get_page(page)
    except PageNotAnInteger:
        acceptedprojects_page = paginator.get_page(1)
    except EmptyPage:
        acceptedprojects_page = paginator.get_page(paginator.num_pages)



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
        
        for project in Person.objects.filter(status='Accepted').values_list('name', 'phone_number', 'email', 'title', 'project_title', 'summarised_abstract', 'full_abstract', 'department', 'organisation', 'expertiseskills', 'devices', 'project_complexity', 'ethics_form','source_type', 'launching_date', 'motivations', 'tags__name', 'status', 'NICEtier'):
             writer.writerow(project)
        response['Content-Disposition'] = 'attachment; filename ="acceptedprojects.csv"'
        return response

    context ={
        'acceptedprojects': acceptedprojects,
        'myFilter': myFilter,
        'innovationumber': innovationnumber,
        'discoverynumber': discoverynumber,
        'scaffoldingnumber': scaffoldingnumber,
        'acceptedprojects_page': acceptedprojects_page
    }
    
    #return HttpResponse(template.render(context, request))
    return render(request, 'CFP_Portal/acceptedprojects.html', context)


@login_required
@user_passes_test(is_reviewer)
def underreviewprojects(request):
    #template = loader.get_template('CFP_Portal/index.html')
    underreviewprojects = UnderReviewProjects.objects.order_by('-date_under_review')



    myFilter = ProjectFilter(request.GET, queryset = underreviewprojects)
    projects = myFilter.qs
    innovationnumber = UnderReviewProjects.objects.filter(project__project_complexity='Innovation').count()
    scaffoldingnumber = UnderReviewProjects.objects.filter(project__project_complexity='Scaffolding').count()
    discoverynumber = UnderReviewProjects.objects.filter(project__project_complexity='Discovery').count()


    if request.method == 'GET' and 'innovation' in request.GET:
        projects = Person.objects.filter(project_complexity='Innovation').order_by('-date_under_review')

    if request.method == 'GET' and 'discovery' in request.GET:
        projects = Person.objects.filter(project_complexity='Discovery').order_by('-date_under_review')

    if request.method == 'GET' and 'scaffolding' in request.GET:
       projects = Person.objects.filter(project_complexity='Scaffolding').order_by('-date_under_review')

    if request.method == 'GET' and 'approve' in request.GET:
        response = HttpResponse(content_type ='text/csv')
        writer = csv.writer(response)
        writer.writerow(['Name', 'Phone Number', 'Email', 'Title', 'Project Title', 'Summarised Abstract', 'Full Abstract', 'Department', 'Organisation', 'Expertise Skills', 'Devices and Technologies', 'Project Complexity', 'Completion of form', 'Source type', 'Launching date', 'Motivations', 'Tags', 'Status', 'NICEtier'])
        
        for project in Person.objects.filter(status='Under Review').values_list('name', 'phone_number', 'email', 'title', 'project_title', 'summarised_abstract', 'full_abstract', 'department', 'organisation', 'expertiseskills', 'devices', 'project_complexity', 'ethics_form','source_type', 'launching_date', 'motivations', 'tags__name', 'status', 'NICEtier'):
             writer.writerow(project)
        response['Content-Disposition'] = 'attachment; filename ="underreviewprojects.csv"'
        return response
    context ={
        'underreviewprojects': rejectedprojects,
        'myFilter': myFilter,
        'innovationumber': innovationnumber,
        'discoverynumber': discoverynumber,
        'scaffoldingnumber': scaffoldingnumber
    }
    
    #return HttpResponse(template.render(context, request))
    return render(request, 'CFP_Portal/underreviewprojects.html', context)



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
def  trial(request):
    model = Person
    projects = Person.objects.all()
    # template_name = 'CFP_Portal/trial.html'
    context_object_name = 'projects'
    context={
        'projects': projects

    }
    return render(request, 'CFP_Portal/trial.html', context)


@login_required
@user_passes_test(is_reviewer)
def  feedback(request):

    if request.method == 'POST' and 'feedback' in request.POST:
        form = Feedback(request.POST)
        
        if form.is_valid:
        #    save_it = form.save(commit = False)
        #    save_it.save()

           message_firstname = request.POST['message-firstname']
           message_surname = request.POST['message-surname']
           # message_email = request.POST['message-email']
           message_phone = request.POST['message-phone']
           # message = request.POST['message']
           message = request.POST.get('message', '')
           message_email = request.POST.get('message-email', '')
        #    from_email = save_it.email
        
        send_mail(
            'Get in touch - Leave us a feeback',   #subject line
            message,    #message
            message_email,    #from
            [settings.EMAIL_HOST_USER,'alexairimia43@gmail.com'],    #to
            fail_silently=True
        )


        return render(request, 'CFP_Portal/feedback.html', {'message_firstname':message_firstname,'form':form, 'message_surname':message_surname, 'message_email':message_email, 'message_phone':message_phone, 'message':message})
    else:
        form = Feedback()
        return render(request, 'CFP_Portal/feedback.html')
    # model = Person
    # projects = Person.objects.all()
    # context_object_name = 'projects'
    # context={
    #     'projects': projects

    # }
   

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
class HomeProjectListView(ListView, ): # this is the former PostListView
    model = Person # for the project
    template_name ='CFP_Portal/home.html'
    context_object_name = 'projects'
    #ordering = ['date_posted']
    paginate_by = 5


@login_required
@user_passes_test(is_reviewer)
class OrganisationDetailView(DetailView):
    model = Organisation
    context_object_name = 'organisations'



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
                    
           
            # message_firstname = request.POST['message-firstname']
            # message_surname = request.POST['message-surname']
            # # message_email = request.POST['message-email']
            # message_phone = request.POST['message-phone']
            # message = request.POST['message']
            # message = request.POST.get('message', '')
            message_email = request.POST.get('message-email', '')
            #    from_email = save_it.email
        
            send_mail(
                'Thank you! We successfully received your project proposal!',   #subject line
                'Congratulations upon your most recent successful submission of the project proposal.\nYou will soon be informed and contacted in regards to the next steps.\n Best wishes, \n Call-for-projects Portal Team ',    #message
                settings.EMAIL_HOST_USER,    #from
                [project.email],    #to
                fail_silently=True
            )

            
        item_list = Person.objects.all()
        
        return redirect('/CFP_Portal/viewdetailsproject')
    

    form = Proposal()
    
    return render(request, 'CFP_Portal/submission_portal.html', {"form": form})
    
    
    

 
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


 

