from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from .models import Job, Company, Application, UserProfile, Category, JobBookmark
from .forms import (
    UserRegistrationForm, CompanyRegistrationForm, JobPostForm,
    ApplicationForm, UserProfileForm, JobSearchForm
)

def home(request):
    """Home page with featured jobs and search functionality"""
    featured_jobs = Job.objects.filter(is_active=True).order_by('-created_at')[:6]
    categories = Category.objects.all()[:8]
    
    context = {
        'featured_jobs': featured_jobs,
        'categories': categories,
        'search_form': JobSearchForm(),
    }
    return render(request, 'jobportal/home.html', context)

def job_list(request):
    """Job listing page with search and filter functionality"""
    jobs = Job.objects.filter(is_active=True)
    search_form = JobSearchForm(request.GET)
    
    if search_form.is_valid():
        keyword = search_form.cleaned_data.get('keyword')
        location = search_form.cleaned_data.get('location')
        category = search_form.cleaned_data.get('category')
        employment_type = search_form.cleaned_data.get('employment_type')
        experience_level = search_form.cleaned_data.get('experience_level')
        is_remote = search_form.cleaned_data.get('is_remote')
        
        if keyword:
            jobs = jobs.filter(
                Q(title__icontains=keyword) |
                Q(description__icontains=keyword) |
                Q(company__name__icontains=keyword)
            )
        
        if location:
            jobs = jobs.filter(location__icontains=location)
        
        if category:
            jobs = jobs.filter(category=category)
        
        if employment_type:
            jobs = jobs.filter(employment_type=employment_type)
        
        if experience_level:
            jobs = jobs.filter(experience_level=experience_level)
        
        if is_remote:
            jobs = jobs.filter(is_remote=True)
    
    # Pagination
    paginator = Paginator(jobs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'jobs': page_obj,
        'search_form': search_form,
        'total_jobs': jobs.count(),
    }
    return render(request, 'jobportal/job_list.html', context)

def job_detail(request, job_id):
    """Job detail page"""
    job = get_object_or_404(Job, id=job_id, is_active=True)
    is_bookmarked = False
    
    if request.user.is_authenticated:
        is_bookmarked = JobBookmark.objects.filter(user=request.user, job=job).exists()
    
    context = {
        'job': job,
        'is_bookmarked': is_bookmarked,
    }
    return render(request, 'jobportal/job_detail.html', context)

@login_required
def apply_job(request, job_id):
    """Apply for a job"""
    job = get_object_or_404(Job, id=job_id, is_active=True)
    
    # Check if user already applied
    if Application.objects.filter(job=job, applicant=request.user).exists():
        messages.warning(request, 'You have already applied for this job.')
        return redirect('job_detail', job_id=job_id)
    
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            messages.success(request, 'Your application has been submitted successfully!')
            return redirect('job_detail', job_id=job_id)
    else:
        form = ApplicationForm()
    
    context = {
        'form': form,
        'job': job,
    }
    return render(request, 'jobportal/apply_job.html', context)

def register(request):
    """User registration"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create user profile
            UserProfile.objects.create(user=user)
            # Log in the user
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    
    context = {'form': form}
    return render(request, 'jobportal/register.html', context)

def register_company(request):
    """Company registration"""
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        company_form = CompanyRegistrationForm(request.POST, request.FILES)
        
        if user_form.is_valid() and company_form.is_valid():
            user = user_form.save()
            company = company_form.save(commit=False)
            company.user = user
            company.save()
            
            # Create user profile
            UserProfile.objects.create(user=user)
            
            # Log in the user
            login(request, user)
            messages.success(request, 'Company account created successfully!')
            return redirect('home')
    else:
        user_form = UserRegistrationForm()
        company_form = CompanyRegistrationForm()
    
    context = {
        'user_form': user_form,
        'company_form': company_form,
    }
    return render(request, 'jobportal/register_company.html', context)

@login_required
def dashboard(request):
    """User dashboard"""
    if hasattr(request.user, 'company'):
        # Company dashboard
        jobs = Job.objects.filter(company=request.user.company)
        applications = Application.objects.filter(job__company=request.user.company)
        
        context = {
            'jobs': jobs,
            'applications': applications,
            'is_company': True,
        }
        return render(request, 'jobportal/company_dashboard.html', context)
    else:
        # Job seeker dashboard
        applications = Application.objects.filter(applicant=request.user)
        bookmarks = JobBookmark.objects.filter(user=request.user)
        
        context = {
            'applications': applications,
            'bookmarks': bookmarks,
            'is_company': False,
        }
        return render(request, 'jobportal/user_dashboard.html', context)

@login_required
def post_job(request):
    """Post a new job (company only)"""
    if not hasattr(request.user, 'company'):
        messages.error(request, 'Only companies can post jobs.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = JobPostForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.company = request.user.company
            job.save()
            messages.success(request, 'Job posted successfully!')
            return redirect('dashboard')
    else:
        form = JobPostForm()
    
    context = {'form': form}
    return render(request, 'jobportal/post_job.html', context)

@login_required
def profile(request):
    """User profile management"""
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
    
    context = {'form': form, 'profile': profile}
    return render(request, 'jobportal/profile.html', context)

@login_required
@require_POST
def bookmark_job(request, job_id):
    """Bookmark/unbookmark a job"""
    job = get_object_or_404(Job, id=job_id)
    bookmark, created = JobBookmark.objects.get_or_create(user=request.user, job=job)
    
    if not created:
        bookmark.delete()
        return JsonResponse({'status': 'unbookmarked'})
    
    return JsonResponse({'status': 'bookmarked'})

@login_required
def my_applications(request):
    """View user's job applications"""
    applications = Application.objects.filter(applicant=request.user)
    context = {'applications': applications}
    return render(request, 'jobportal/my_applications.html', context)

@login_required
def my_bookmarks(request):
    """View user's bookmarked jobs"""
    bookmarks = JobBookmark.objects.filter(user=request.user)
    context = {'bookmarks': bookmarks}
    return render(request, 'jobportal/my_bookmarks.html', context)

def category_jobs(request, category_id):
    """Jobs by category"""
    category = get_object_or_404(Category, id=category_id)
    jobs = Job.objects.filter(category=category, is_active=True)
    
    paginator = Paginator(jobs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'jobs': page_obj,
    }
    return render(request, 'jobportal/category_jobs.html', context)
