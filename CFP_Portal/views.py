from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User
from .models import Organisation, Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

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
        'posts':Post.objects.all()
    }
    return render(request, 'CFP_Portal/home.html', context)

def about(request):
    #return HttpResponse('<h1> Blog About </h1>')
    context={
        
    }
    return render(request, 'CFP_Portal/about.html', "title: About", context)

class OrganisationListView(ListView):
    model = Organisation
    template_name ='CFP_Portal/organisation_list.html'
    context_object_name = 'organisations'
    paginate_by = 5
    

class PostListView(ListView):
    model = Post
    template_name ='CFP_Portal/home.html'
    context_object_name = 'posts'
    ordering = ['date_posted']
    paginate_by = 5

class PostDetailView(DetailView):
    model = Post

class OrganisationDetailView(DetailView):
    model = Organisation
    context_object_name = 'organisations'
    
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