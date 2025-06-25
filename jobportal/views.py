from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from .models import Job, Company, Application, UserProfile, Category, JobBookmark, SavedSearch
from .forms import (
    UserRegistrationForm, CompanyRegistrationForm, JobPostForm,
    ApplicationForm, UserProfileForm, JobSearchForm, CompanyJobPostForm
)
from django.contrib.admin.views.decorators import staff_member_required
from datetime import timedelta
from django.utils import timezone

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
    # Only show jobs in India or Remote
    indian_cities = [
        'Bangalore', 'Bengaluru', 'Chennai', 'Hyderabad', 'Pune', 'Delhi', 'Mumbai', 'Kolkata', 'Ahmedabad',
        'Gurgaon', 'Noida', 'Jaipur', 'Lucknow', 'Chandigarh', 'Coimbatore', 'Indore', 'Nagpur', 'Patna',
        'Bhopal', 'Visakhapatnam', 'Vadodara', 'Ludhiana', 'Agra', 'Nashik', 'Faridabad', 'Meerut', 'Rajkot',
        'Varanasi', 'Srinagar', 'Aurangabad', 'Dhanbad', 'Amritsar', 'Allahabad', 'Ranchi', 'Howrah', 'Jabalpur',
        'Gwalior', 'Vijayawada', 'Jodhpur', 'Madurai', 'Raipur', 'Kota', 'Guwahati', 'Solapur', 'Hubli', 'Mysore',
        'Tiruchirappalli', 'Bareilly', 'Aligarh', 'Tiruppur', 'Moradabad', 'Jalandhar', 'Bhubaneswar', 'Salem',
        'Warangal', 'Guntur', 'Bhiwandi', 'Saharanpur', 'Gorakhpur', 'Bikaner', 'Amravati', 'Noida'
    ]
    city_q = Q(location__icontains='india') | Q(location__icontains='remote')
    for city in indian_cities:
        city_q |= Q(location__icontains=city)
    jobs = jobs.filter(city_q)
    search_form = JobSearchForm(request.GET)
    
    if search_form.is_valid():
        keyword = search_form.cleaned_data.get('keyword')
        location = search_form.cleaned_data.get('location')
        category = search_form.cleaned_data.get('category')
        employment_type = search_form.cleaned_data.get('employment_type')
        experience_level = search_form.cleaned_data.get('experience_level')
        is_remote = search_form.cleaned_data.get('is_remote')
        min_salary = search_form.cleaned_data.get('min_salary')
        max_salary = search_form.cleaned_data.get('max_salary')
        
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
        
        if min_salary is not None:
            jobs = jobs.filter(salary_max__gte=min_salary)
        if max_salary is not None:
            jobs = jobs.filter(salary_min__lte=max_salary)
    
    sort = request.GET.get('sort')
    if sort == 'date':
        jobs = jobs.order_by('-created_at')
    elif sort == 'salary':
        jobs = jobs.order_by('-salary_max')
    elif sort == 'title':
        jobs = jobs.order_by('title')
    
    # Pagination
    paginator = Paginator(jobs, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get applied and bookmarked job ids for the current user
    if request.user.is_authenticated:
        applied_job_ids = set(Application.objects.filter(applicant=request.user).values_list('job_id', flat=True))
        bookmarked_job_ids = set(JobBookmark.objects.filter(user=request.user).values_list('job_id', flat=True))
    else:
        applied_job_ids = set()
        bookmarked_job_ids = set()
    
    context = {
        'jobs': page_obj,
        'search_form': search_form,
        'total_jobs': jobs.count(),
        'applied_job_ids': applied_job_ids,
        'bookmarked_job_ids': bookmarked_job_ids,
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

@login_required
def company_register(request):
    if hasattr(request.user, 'company_profile'):
        return redirect('company_dashboard')  # Or wherever you want to redirect if already registered
    if request.method == 'POST':
        form = CompanyRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            company = form.save(commit=False)
            company.user = request.user
            company.save()
            return redirect('company_dashboard')  # Or wherever you want
    else:
        form = CompanyRegistrationForm()
    return render(request, 'jobportal/register_company.html', {'form': form})

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
        # Recommendation logic
        recommended_jobs = Job.objects.filter(is_active=True)
        profile = getattr(request.user, 'userprofile', None)
        if profile and profile.skills:
            skill_list = [s.strip().lower() for s in profile.skills.split(',') if s.strip()]
            skill_q = Q()
            for skill in skill_list:
                skill_q |= Q(requirements__icontains=skill) | Q(description__icontains=skill)
            recommended_jobs = recommended_jobs.filter(skill_q)
        # Also recommend jobs in categories the user has applied to
        applied_categories = applications.values_list('job__category', flat=True)
        if applied_categories:
            recommended_jobs = recommended_jobs | Job.objects.filter(category__in=applied_categories, is_active=True)
        # Exclude jobs already applied/bookmarked
        recommended_jobs = recommended_jobs.exclude(applications__applicant=request.user).exclude(bookmarks__user=request.user).distinct()[:6]
        context = {
            'applications': applications,
            'bookmarks': bookmarks,
            'is_company': False,
            'recommended_jobs': recommended_jobs,
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

def logout_view(request):
    """Custom logout view"""
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'You have been successfully logged out.')
        return redirect('home')
    else:
        # For any other method, redirect to home
        return redirect('home')

@login_required
def save_search(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        keyword = request.POST.get('keyword')
        location = request.POST.get('location')
        category_id = request.POST.get('category')
        employment_type = request.POST.get('employment_type')
        experience_level = request.POST.get('experience_level')
        is_remote = request.POST.get('is_remote') == 'on' or request.POST.get('is_remote') == 'True'
        category = Category.objects.filter(id=category_id).first() if category_id else None
        SavedSearch.objects.create(
            user=request.user,
            name=name,
            keyword=keyword,
            location=location,
            category=category,
            employment_type=employment_type,
            experience_level=experience_level,
            is_remote=is_remote
        )
        messages.success(request, 'Search saved!')
        return redirect('my_saved_searches')
    return redirect('job_list')

@login_required
def my_saved_searches(request):
    searches = request.user.saved_searches.all()
    return render(request, 'jobportal/my_saved_searches.html', {'searches': searches})

def courses(request):
    """Courses listing page (to be implemented)"""
    # Placeholder for course data
    courses = []
    context = {'courses': courses}
    return render(request, 'jobportal/courses.html', context)

@login_required
def company_dashboard(request):
    if not hasattr(request.user, 'company_profile'):
        return redirect('register_company')
    company = request.user.company_profile
    jobs = Job.objects.filter(company=company)
    return render(request, 'jobportal/company_dashboard.html', {'company': company, 'jobs': jobs})

def company_profile(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    jobs = Job.objects.filter(company=company, is_active=True)
    return render(request, 'jobportal/company_profile.html', {'company': company, 'jobs': jobs})

@login_required
def company_post_job(request):
    if not hasattr(request.user, 'company_profile'):
        return redirect('register_company')
    if request.method == 'POST':
        form = CompanyJobPostForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.company = request.user.company_profile
            job.save()
            return redirect('company_dashboard')
    else:
        form = CompanyJobPostForm()
    return render(request, 'jobportal/company_post_job.html', {'form': form})

@login_required
def company_edit_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, company=request.user.company_profile)
    if request.method == 'POST':
        form = CompanyJobPostForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('company_dashboard')
    else:
        form = CompanyJobPostForm(instance=job)
    return render(request, 'jobportal/company_post_job.html', {'form': form, 'edit_mode': True})

@login_required
def company_delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, company=request.user.company_profile)
    if request.method == 'POST':
        job.delete()
        return redirect('company_dashboard')
    return render(request, 'jobportal/company_confirm_delete.html', {'job': job})

@login_required
def user_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'jobportal/profile.html', {'form': form, 'profile': profile})

@login_required
def update_application_status(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    # Only allow the company that owns the job to update status
    if not hasattr(request.user, 'company') or application.job.company != request.user.company:
        return HttpResponseForbidden("You are not allowed to update this application.")
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Application.STATUS_CHOICES):
            application.status = new_status
            application.save()
            messages.success(request, 'Application status updated.')
        else:
            messages.error(request, 'Invalid status.')
    return redirect('company_dashboard')

@staff_member_required
def admin_dashboard(request):
    from django.contrib.auth.models import User
    from .models import Company, Job, Application
    user_count = User.objects.count()
    company_count = Company.objects.count()
    job_count = Job.objects.count()
    application_count = Application.objects.count()
    context = {
        'user_count': user_count,
        'company_count': company_count,
        'job_count': job_count,
        'application_count': application_count,
    }
    return render(request, 'jobportal/admin_dashboard.html', context)

@login_required
def renew_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if not hasattr(request.user, 'company') or job.company != request.user.company:
        return HttpResponseForbidden("You are not allowed to renew this job.")
    if request.method == 'POST':
        job.is_active = True
        job.deadline = timezone.now().date() + timedelta(days=30)
        job.save()
        messages.success(request, 'Job renewed for 30 more days.')
    return redirect('dashboard')
