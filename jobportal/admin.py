from django.contrib import admin
from .models import Category, Company, Job, Application, UserProfile, JobBookmark

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    ordering = ['name']

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'location', 'industry', 'company_size', 'created_at']
    list_filter = ['industry', 'company_size', 'created_at']
    search_fields = ['name', 'location', 'industry']
    ordering = ['name']

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'category', 'location', 'employment_type', 'experience_level', 'is_active', 'created_at']
    list_filter = ['category', 'employment_type', 'experience_level', 'is_active', 'is_remote', 'created_at']
    search_fields = ['title', 'company__name', 'location']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['applicant', 'job', 'status', 'applied_at']
    list_filter = ['status', 'applied_at']
    search_fields = ['applicant__username', 'applicant__first_name', 'applicant__last_name', 'job__title']
    ordering = ['-applied_at']
    date_hierarchy = 'applied_at'

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'experience_years', 'created_at']
    list_filter = ['experience_years', 'created_at']
    search_fields = ['user__username', 'user__first_name', 'user__last_name']
    ordering = ['user__username']

@admin.register(JobBookmark)
class JobBookmarkAdmin(admin.ModelAdmin):
    list_display = ['user', 'job', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'job__title']
    ordering = ['-created_at']
