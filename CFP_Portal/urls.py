from django.urls import path
from . import views
from .views import (PostListView, 
                PostDetailView,
                PostCreateView, 
                PostUpdateView, 
                PostDeleteView, 
                UserPostListView,
                OrganisationListView,
                OrganisationDetailView,
                OrganisationUpdateView,
                OrganisationDeleteView)


urlpatterns = [
    path('', PostListView.as_view(), name = 'blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('about/', views.about, name = 'blog-about'),
    path('displayOrganisations/', OrganisationListView.as_view() , name= 'organisations'),
    path('post/<int:pk>/', PostDetailView.as_view(), name = 'post-detail'),
    path('organisation/<int:pk>/', OrganisationDetailView.as_view(), name = 'organisation-detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name = 'post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name = 'post-delete'),
    path('organisation/<int:pk>/update/', OrganisationUpdateView.as_view(), name = 'organisation-update'),
    path('organisation/<int:pk>/delete/', OrganisationDeleteView.as_view(), name = 'organisation-delete'),
    path('post/new/', PostCreateView.as_view(), name = 'post-create'),
]