from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from jobportal.models import Category, Company, Job
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Populate database with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')

        # Create categories
        categories_data = [
            {'name': 'Software Development', 'description': 'Jobs in software development and programming'},
            {'name': 'Data Science', 'description': 'Jobs in data analysis, machine learning, and AI'},
            {'name': 'Marketing', 'description': 'Jobs in digital marketing, content creation, and SEO'},
            {'name': 'Design', 'description': 'Jobs in UI/UX design, graphic design, and web design'},
            {'name': 'Sales', 'description': 'Jobs in sales, business development, and account management'},
            {'name': 'Customer Support', 'description': 'Jobs in customer service and technical support'},
            {'name': 'Finance', 'description': 'Jobs in accounting, financial analysis, and investment'},
            {'name': 'Human Resources', 'description': 'Jobs in HR, recruitment, and talent management'},
        ]

        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            categories[cat_data['name']] = category
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Create sample companies
        companies_data = [
            {
                'name': 'TechCorp Solutions',
                'description': 'Leading technology company specializing in innovative software solutions',
                'location': 'San Francisco, CA',
                'industry': 'Technology',
                'company_size': '201-500',
                'founded_year': 2015,
                'website': 'https://techcorp.com'
            },
            {
                'name': 'DataFlow Analytics',
                'description': 'Data science and analytics company helping businesses make data-driven decisions',
                'location': 'New York, NY',
                'industry': 'Data & Analytics',
                'company_size': '51-200',
                'founded_year': 2018,
                'website': 'https://dataflow.com'
            },
            {
                'name': 'Creative Design Studio',
                'description': 'Creative agency specializing in branding, web design, and digital marketing',
                'location': 'Los Angeles, CA',
                'industry': 'Creative & Design',
                'company_size': '11-50',
                'founded_year': 2020,
                'website': 'https://creativestudio.com'
            },
            {
                'name': 'Global Marketing Group',
                'description': 'International marketing agency with expertise in digital and traditional marketing',
                'location': 'Chicago, IL',
                'industry': 'Marketing',
                'company_size': '500+',
                'founded_year': 2010,
                'website': 'https://globalmarketing.com'
            },
        ]

        companies = {}
        for comp_data in companies_data:
            # Create user for company
            username = comp_data['name'].lower().replace(' ', '').replace(',', '')
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'first_name': comp_data['name'].split()[0],
                    'last_name': 'Company',
                    'email': f'{username}@example.com',
                    'password': 'password123'
                }
            )
            if created:
                user.set_password('password123')
                user.save()

            company, created = Company.objects.get_or_create(
                user=user,
                defaults=comp_data
            )
            companies[comp_data['name']] = company
            if created:
                self.stdout.write(f'Created company: {company.name}')

        # Create sample jobs
        jobs_data = [
            {
                'title': 'Senior Python Developer',
                'company': companies['TechCorp Solutions'],
                'category': categories['Software Development'],
                'description': 'We are looking for an experienced Python developer to join our team and help build scalable web applications.',
                'requirements': '5+ years of Python experience, Django/Flask, PostgreSQL, AWS, Git',
                'responsibilities': 'Develop and maintain web applications, collaborate with cross-functional teams, mentor junior developers',
                'location': 'San Francisco, CA',
                'employment_type': 'full-time',
                'experience_level': 'senior',
                'salary_min': 120000,
                'salary_max': 160000,
                'is_remote': True,
                'deadline': timezone.now().date() + timedelta(days=30)
            },
            {
                'title': 'Data Scientist',
                'company': companies['DataFlow Analytics'],
                'category': categories['Data Science'],
                'description': 'Join our data science team to develop machine learning models and provide insights to clients.',
                'requirements': 'Masters in Statistics/CS, Python, R, SQL, machine learning frameworks',
                'responsibilities': 'Build ML models, analyze data, create reports, present findings to stakeholders',
                'location': 'New York, NY',
                'employment_type': 'full-time',
                'experience_level': 'mid',
                'salary_min': 90000,
                'salary_max': 130000,
                'is_remote': False,
                'deadline': timezone.now().date() + timedelta(days=45)
            },
            {
                'title': 'UI/UX Designer',
                'company': companies['Creative Design Studio'],
                'category': categories['Design'],
                'description': 'Creative designer needed to create beautiful and functional user interfaces for web and mobile applications.',
                'requirements': '3+ years of design experience, Figma, Adobe Creative Suite, portfolio required',
                'responsibilities': 'Design user interfaces, create wireframes, conduct user research, collaborate with developers',
                'location': 'Los Angeles, CA',
                'employment_type': 'full-time',
                'experience_level': 'mid',
                'salary_min': 70000,
                'salary_max': 100000,
                'is_remote': True,
                'deadline': timezone.now().date() + timedelta(days=20)
            },
            {
                'title': 'Digital Marketing Specialist',
                'company': companies['Global Marketing Group'],
                'category': categories['Marketing'],
                'description': 'Experienced digital marketer to manage campaigns across multiple platforms and drive growth.',
                'requirements': '2+ years of digital marketing experience, Google Ads, Facebook Ads, Google Analytics',
                'responsibilities': 'Manage ad campaigns, analyze performance, optimize for conversions, report to clients',
                'location': 'Chicago, IL',
                'employment_type': 'full-time',
                'experience_level': 'entry',
                'salary_min': 50000,
                'salary_max': 70000,
                'is_remote': False,
                'deadline': timezone.now().date() + timedelta(days=15)
            },
            {
                'title': 'Frontend Developer (React)',
                'company': companies['TechCorp Solutions'],
                'category': categories['Software Development'],
                'description': 'Frontend developer to build responsive and interactive user interfaces using React.',
                'requirements': '2+ years of React experience, JavaScript, HTML/CSS, responsive design',
                'responsibilities': 'Build React components, optimize performance, work with design team, write tests',
                'location': 'San Francisco, CA',
                'employment_type': 'full-time',
                'experience_level': 'mid',
                'salary_min': 80000,
                'salary_max': 110000,
                'is_remote': True,
                'deadline': timezone.now().date() + timedelta(days=25)
            },
            {
                'title': 'Sales Representative',
                'company': companies['Global Marketing Group'],
                'category': categories['Sales'],
                'description': 'Dynamic sales professional to drive revenue growth and build client relationships.',
                'requirements': '1+ years of sales experience, excellent communication skills, CRM experience',
                'responsibilities': 'Generate leads, conduct sales calls, close deals, maintain client relationships',
                'location': 'Chicago, IL',
                'employment_type': 'full-time',
                'experience_level': 'entry',
                'salary_min': 40000,
                'salary_max': 60000,
                'is_remote': False,
                'deadline': timezone.now().date() + timedelta(days=10)
            },
        ]

        for job_data in jobs_data:
            job, created = Job.objects.get_or_create(
                title=job_data['title'],
                company=job_data['company'],
                defaults=job_data
            )
            if created:
                self.stdout.write(f'Created job: {job.title} at {job.company.name}')

        self.stdout.write(
            self.style.SUCCESS('Successfully created sample data!')
        ) 