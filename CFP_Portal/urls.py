from django.urls import path
from . import views
from .views import (HomeProjectListView, 
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
                UsersListView,
                ProjectsListView, 
                ProjectDetailView,
                ReviewsDisplayListView,
                Trial)


urlpatterns = [
    path('', views.home, name = 'blog-home'),
    path('user/<str:username>', views.UserPostListView, name='user-posts'),
    path('about/', views.about, name = 'blog-about'),
    path('displayOrganisations/', views.OrganisationListView , name= 'organisations'),
    path('reviews/', views.ReviewsListView , name= 'reviews'),
    path('trial/', views.Trial , name= 'trial'),
    path('reviewDisplay/', views.reviewdisplay , name= 'review-display'), #review grid

    path('post/<int:pk>/', views.PostDetailView, name = 'post-detail'), # feedback sheet
    # path('review/<int:review_id>/', ReviewDetailView.as_view(), name = 'review-detail'),
    path('review/<int:review_id>/', views.review, name = 'review-detail'), # VIEW ONE REVIEW
    path('reviewdetail/<int:project_id>/', views.projectreviewdetail , name= 'reviewdetail'),

    path('organisation/<int:pk>/', views.OrganisationDetailView, name = 'organisation-detail'),
    path('project/<int:pk>/', views.projectdetail, name = 'project-detail'),

    path('project/<int:project_id>/review/<int:review_id>/', views.detail, name='detail'),
    
    
    # path('markAndReview/project/<int:pk>/', MarkProjectDetail.as_view(), name = 'mark-project-detail'),
    path('markAndReview/project/<int:pk>/', views.markprojectdetail, name = 'mark-project-detail'),

    path('post/<int:pk>/update/', views.PostUpdateView, name = 'post-update'),
    path('post/<int:pk>/delete/', views.PostDeleteView, name = 'post-delete'),
    path('organisation/<int:pk>/update/', views.OrganisationUpdateView, name = 'organisation-update'),
    path('organisation/<int:pk>/delete/', views.OrganisationDeleteView, name = 'organisation-delete'),
    path('post/new/', views.PostCreateView, name = 'post-create'),

    path('users/', views.UsersListView, name = 'users' ),
    path('projects/', views.projectgrid, name = 'projects' ),
    path('projects/list', views.projectlistview, name = 'projectslist' ),
    path('acceptedprojects', views.acceptedprojects, name = 'acceptedprojects' ),
    path('rejectedprojects', views.rejectedprojects, name = 'rejectedprojects' ),


    path('SubmissionPortal/', views.SubmissionPortal, name= 'SubmissionPortal'),
    path('ReviewPortal/<int:project_id>/', views.ReviewPortal, name= 'ReviewPortal'),
    path('export/', views.export, name='export')
    # path('ReviewPortal/', views.ReviewPortal, name= 'ReviewPortal'),

    
   
]