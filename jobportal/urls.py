from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Public pages
    path('', views.home, name='home'),
    path('jobs/', views.job_list, name='job_list'),
    path('job/<int:job_id>/', views.job_detail, name='job_detail'),
    path('category/<int:category_id>/', views.category_jobs, name='category_jobs'),
    
    # Authentication
    path('register/', views.register, name='register'),
    path('register/company/', views.company_register, name='register_company'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Job application
    path('job/<int:job_id>/apply/', views.apply_job, name='apply_job'),
    
    # User features (login required)
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.user_profile, name='user_profile'),
    path('applications/', views.my_applications, name='my_applications'),
    path('bookmarks/', views.my_bookmarks, name='my_bookmarks'),
    path('job/<int:job_id>/bookmark/', views.bookmark_job, name='bookmark_job'),
    
    # Company features (login required)
    path('post-job/', views.post_job, name='post_job'),
    path('save-search/', views.save_search, name='save_search'),
    path('my-saved-searches/', views.my_saved_searches, name='my_saved_searches'),
    path('courses/', views.courses, name='courses'),
    path('company/dashboard/', views.company_dashboard, name='company_dashboard'),
    path('company/<int:company_id>/', views.company_profile, name='company_profile'),
    path('company/post-job/', views.company_post_job, name='company_post_job'),
    path('application/<int:application_id>/update-status/', views.update_application_status, name='update_application_status'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('job/<int:job_id>/renew/', views.renew_job, name='renew_job'),
] 