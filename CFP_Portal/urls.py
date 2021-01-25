from django.urls import path
from . import views
from .views import PostListView, PostDetailView, PostCreateView

urlpatterns = [
    path('', PostListView.as_view(), name = 'blog-home'),
    path('about/', views.about, name = 'blog-about'),
    path('displayOrganisations', views.index, name= 'index'),
    path('post/<int:pk>/', PostDetailView.as_view(), name = 'post-detail'),
    path('post/new/', PostCreateView.as_view(), name = 'post-create'),
]