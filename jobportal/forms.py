from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Company, Job, Application, UserProfile

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class CompanyRegistrationForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'description', 'website', 'logo', 'location', 'industry', 'founded_year', 'company_size']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'founded_year': forms.NumberInput(attrs={'min': 1800, 'max': 2024}),
        }

class JobPostForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            'title', 'category', 'description', 'requirements', 'responsibilities',
            'location', 'employment_type', 'experience_level', 'salary_min',
            'salary_max', 'is_remote', 'deadline'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 6}),
            'requirements': forms.Textarea(attrs={'rows': 4}),
            'responsibilities': forms.Textarea(attrs={'rows': 4}),
            'deadline': forms.DateInput(attrs={'type': 'date'}),
            'salary_min': forms.NumberInput(attrs={'min': 0}),
            'salary_max': forms.NumberInput(attrs={'min': 0}),
        }

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['cover_letter', 'resume']
        widgets = {
            'cover_letter': forms.Textarea(attrs={'rows': 8, 'placeholder': 'Write your cover letter here...'}),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'phone', 'address', 'bio', 'skills', 'experience_years',
            'education', 'profile_picture', 'resume', 'linkedin_url', 'github_url'
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'skills': forms.Textarea(attrs={'rows': 3}),
            'education': forms.Textarea(attrs={'rows': 4}),
            'experience_years': forms.NumberInput(attrs={'min': 0, 'max': 50}),
        }

class JobSearchForm(forms.Form):
    keyword = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Job title, keywords, or company'}))
    location = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'City, state, or remote'}))
    category = forms.ModelChoiceField(queryset=None, required=False, empty_label="All Categories")
    employment_type = forms.ChoiceField(choices=[('', 'All Types')] + Job.EMPLOYMENT_TYPE_CHOICES, required=False)
    experience_level = forms.ChoiceField(choices=[('', 'All Levels')] + Job.EXPERIENCE_LEVEL_CHOICES, required=False)
    is_remote = forms.BooleanField(required=False, label="Remote only")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .models import Category
        self.fields['category'].queryset = Category.objects.all() 