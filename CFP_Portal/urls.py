from django.urls import path
from . import views
from django.conf import settings
# from django.conf.urls import patterns, include, url
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name = 'blog-home'),


    path('viewdetailsproject/', views.viewdetailsproject , name= 'viewdetailsproject'), #overview of submission
    path('about/', views.about , name= 'about'),
    path('leave/feedback/', views.feedback , name= 'feedback'),
    path('reviewDisplay/', views.reviewdisplay , name= 'review-display'), #review grid

    
    
    path('review/<int:review_id>/', views.review, name = 'review-detail'), # VIEW ONE REVIEW
    path('reviewdetail/<int:project_id>/', views.projectreviewdetail , name= 'reviewdetail'),

   
    path('project/<int:pk>/', views.projectdetail, name = 'project-detail'),  

    path('project/<int:project_id>/review/<int:review_id>/', views.detail, name='detail'),
    
    

    path('markAndReview/project/<int:pk>/', views.markprojectdetail, name = 'mark-project-detail'),



    path('users/', views.UserDisplay, name = 'users'),
    path('projects/', views.projectgrid, name = 'projects' ),
    path('projects/list', views.projectlistview, name = 'projectslist' ),
    path('acceptedprojects', views.acceptedprojects, name = 'acceptedprojects' ),
    path('underreviewprojects', views.underreviewprojects, name = 'underreviewprojects' ),
    path('rejectedprojects', views.rejectedprojects, name = 'rejectedprojects' ),


    path('SubmissionPortal/', views.SubmissionPortal, name= 'SubmissionPortal'),
    path('ReviewPortal/<int:project_id>/', views.ReviewPortal, name= 'ReviewPortal'),
    path('export/', views.export, name='export')
    

    
   
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


