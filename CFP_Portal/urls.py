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
                OrganisationDeleteView,
                ReviewsListView, 
                ReviewDetailView, 
                UsersListView)


urlpatterns = [
    path('', PostListView.as_view(), name = 'blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('about/', views.about, name = 'blog-about'),
    path('displayOrganisations/', OrganisationListView.as_view() , name= 'organisations'),
    path('reviews/', ReviewsListView.as_view() , name= 'reviews'),
    path('post/<int:pk>/', PostDetailView.as_view(), name = 'post-detail'), # feedback sheet
    path('review/<int:pk>/', ReviewDetailView.as_view(), name = 'review-detail'),
    path('organisation/<int:pk>/', OrganisationDetailView.as_view(), name = 'organisation-detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name = 'post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name = 'post-delete'),
    path('organisation/<int:pk>/update/', OrganisationUpdateView.as_view(), name = 'organisation-update'),
    path('organisation/<int:pk>/delete/', OrganisationDeleteView.as_view(), name = 'organisation-delete'),
    path('post/new/', PostCreateView.as_view(), name = 'post-create'),

    path('users/', UsersListView.as_view(), name = 'users' ),


    path('SubmissionPortal/', views.SubmissionPortal, name= 'SubmissionPortal'),
    path('SubmissionPortal/Step2', views.Submission2, name='step2'),
    path('SubmissionPortal/Step3', views.Submission3, name='step3'),
    path('SubmissionPortal/Step4', views.Submission4, name='step4'),
]