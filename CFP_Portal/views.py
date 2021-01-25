from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Organisation, Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

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

class PostListView(ListView):
    model = Post
    template_name ='CFP_Portal/home.html'
    context_object_name = 'posts'
    ordering = ['date_posted']
    paginate_by = 5

class PostDetailView(DetailView):
    model = Post
    
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

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url ='/'

    def test_func(self): # other users are not allowed to delete the feedback forms except for the original author
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
        #return super().test_func()