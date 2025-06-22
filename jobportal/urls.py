from django.urls import path
from . import views

urlpatterns = [
    # Public pages
    path('', views.home, name='home'),
    path('jobs/', views.job_list, name='job_list'),
    path('job/<int:job_id>/', views.job_detail, name='job_detail'),
    path('category/<int:category_id>/', views.category_jobs, name='category_jobs'),
    
    # Authentication
    path('register/', views.register, name='register'),
    path('register/company/', views.register_company, name='register_company'),
    
    # Job application
    path('job/<int:job_id>/apply/', views.apply_job, name='apply_job'),
    
    # User features (login required)
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('applications/', views.my_applications, name='my_applications'),
    path('bookmarks/', views.my_bookmarks, name='my_bookmarks'),
    path('job/<int:job_id>/bookmark/', views.bookmark_job, name='bookmark_job'),
    
    # Company features (login required)
    path('post-job/', views.post_job, name='post_job'),
] 