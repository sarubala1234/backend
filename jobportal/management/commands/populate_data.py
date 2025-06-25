from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from jobportal.models import Category, Company, Job
from django.utils import timezone
from datetime import timedelta
import random

class Command(BaseCommand):
    help = 'Populate database with sample IT and Non-IT jobs, including Freshers and Experienced options.'

    def handle(self, *args, **options):
        self.stdout.write('Creating IT and Non-IT categories...')
        it_categories = [
            {'name': 'Software Development', 'description': 'Jobs in software development and programming'},
            {'name': 'Network Security', 'description': 'Jobs in network and cyber security'},
            {'name': 'Data Science', 'description': 'Jobs in data analysis, machine learning, and AI'},
            {'name': 'IT Support', 'description': 'Jobs in IT support and administration'},
            {'name': 'IT', 'description': 'General IT jobs'},
        ]
        nonit_categories = [
            {'name': 'Marketing', 'description': 'Jobs in digital marketing, content creation, and SEO'},
            {'name': 'Sales', 'description': 'Jobs in sales, business development, and account management'},
            {'name': 'HR', 'description': 'Jobs in HR, recruitment, and talent management'},
            {'name': 'Finance', 'description': 'Jobs in accounting, financial analysis, and investment'},
            {'name': 'Design', 'description': 'Jobs in UI/UX design, graphic design, and web design'},
            {'name': 'Customer Support', 'description': 'Jobs in customer service and technical support'},
            {'name': 'Non-IT', 'description': 'General Non-IT jobs'},
        ]
        all_categories = it_categories + nonit_categories
        categories = {}
        for cat_data in all_categories:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            categories[cat_data['name']] = category
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Create a sample company if none exists
        company, _ = Company.objects.get_or_create(
            user=User.objects.filter(is_superuser=True).first(),
            defaults={
                'name': 'Demo Company',
                'description': 'A demo company for sample jobs.',
                'website': 'https://demo.com',
                'location': 'Remote',
                'industry': 'Demo',
                'founded_year': 2020,
                'company_size': '11-50',
            }
        )

        # IT Jobs
        self.stdout.write('Creating 60 IT jobs...')
        it_titles = [
            'Python Developer', 'Java Developer', 'Frontend Developer', 'Backend Developer', 'Full Stack Developer',
            'Network Security Analyst', 'Cybersecurity Engineer', 'Data Scientist', 'Machine Learning Engineer', 'AI Engineer',
            'IT Support Specialist', 'DevOps Engineer', 'Cloud Engineer', 'QA Engineer', 'Mobile App Developer',
            'Database Administrator', 'System Administrator', 'IT Project Manager', 'Web Developer', 'Software Tester',
            'Network Engineer', 'Security Consultant', 'Penetration Tester', 'IT Analyst', 'Helpdesk Technician',
            'Business Intelligence Analyst', 'UI Developer', 'UX Designer', 'IT Trainer', 'Technical Writer',
            # 30 more IT job titles
            'Blockchain Developer', 'Game Developer', 'Embedded Systems Engineer', 'Site Reliability Engineer', 'Cloud Solutions Architect',
            'SAP Consultant', 'ERP Specialist', 'IT Auditor', 'Information Security Officer', 'Release Manager',
            'Scrum Master', 'Agile Coach', 'Product Owner', 'Solutions Architect', 'Big Data Engineer',
            'Data Engineer', 'Data Architect', 'ETL Developer', 'CRM Developer', 'SharePoint Developer',
            'VoIP Engineer', 'Telecom Engineer', 'GIS Analyst', 'Bioinformatics Scientist', 'Robotics Engineer',
            'Firmware Engineer', 'Test Automation Engineer', 'Build Engineer', 'Virtualization Engineer', 'IT Compliance Analyst'
        ]
        it_perks = [
            'Flexible work hours', 'Remote work options', 'Health insurance', 'Paid certifications', 'Gym membership',
            'Free snacks and drinks', 'Team outings', 'Stock options', 'Annual bonus', 'Learning budget'
        ]
        for i in range(60):
            title = it_titles[i % len(it_titles)]
            category = random.choice([categories['Software Development'], categories['Network Security'], categories['Data Science'], categories['IT Support'], categories['IT']])
            experience_level = random.choice(['freshers', 'experienced'])
            Job.objects.create(
                title=title,
                company=company,
                category=category,
                description=f"{title} role in {category.name}. Work on exciting projects and cutting-edge technology.",
                requirements=f"- {random.choice(['B.Tech/BE in CS/IT', 'MCA', 'Relevant certification'])}\n- {random.randint(0, 5)}+ years experience\n- {random.choice(['Python', 'Java', 'Linux', 'AWS', 'Docker', 'Kubernetes'])}",
                responsibilities=f"- {random.choice(['Develop', 'Test', 'Deploy', 'Maintain'])} software solutions\n- Collaborate with cross-functional teams\n- Write clean, scalable code\n- Participate in code reviews",
                location=random.choice(['Remote', 'Bangalore', 'Chennai', 'Hyderabad', 'Pune', 'Delhi', 'Mumbai']),
                employment_type="full-time",
                experience_level=experience_level,
                salary_min=40000 + i * 1000,
                salary_max=60000 + i * 1000,
                is_remote=random.choice([True, False]),
                deadline=timezone.now().date() + timedelta(days=random.randint(15, 60))
            )
        self.stdout.write('Created 60 IT jobs.')

        # Non-IT Jobs
        self.stdout.write('Creating 60 Non-IT jobs...')
        nonit_titles = [
            'Marketing Executive', 'Sales Representative', 'HR Coordinator', 'Finance Analyst', 'Graphic Designer',
            'Customer Support Agent', 'Content Writer', 'Recruiter', 'Accountant', 'Business Development Manager',
            'Operations Manager', 'Office Assistant', 'PR Specialist', 'Event Coordinator', 'Administrative Assistant',
            'Social Media Manager', 'Copywriter', 'Brand Manager', 'Payroll Specialist', 'Legal Assistant',
            'Procurement Officer', 'Quality Analyst', 'Receptionist', 'Training Coordinator', 'Store Manager',
            'Logistics Coordinator', 'Customer Success Manager', 'Market Research Analyst', 'Sales Manager', 'Non-IT Specialist',
            # 30 more Non-IT job titles
            'Supply Chain Analyst', 'Purchasing Manager', 'Facilities Manager', 'Travel Coordinator', 'Export Manager',
            'Import Specialist', 'Insurance Advisor', 'Loan Officer', 'Bank Teller', 'Branch Manager',
            'Teacher', 'School Principal', 'Librarian', 'Research Assistant', 'Lab Technician',
            'Nurse', 'Pharmacist', 'Medical Representative', 'Dietician', 'Fitness Trainer',
            'Hotel Manager', 'Chef', 'Housekeeping Supervisor', 'Tour Guide', 'Event Planner',
            'Real Estate Agent', 'Interior Designer', 'Fashion Designer', 'Jewelry Designer', 'Artist'
        ]
        nonit_perks = [
            'Performance bonus', 'Health insurance', 'Paid time off', 'Employee discounts', 'Flexible schedule',
            'Free meals', 'Travel allowance', 'Annual retreat', 'Wellness programs', 'Training sessions'
        ]
        for i in range(60):
            title = nonit_titles[i % len(nonit_titles)]
            category = random.choice([categories['Marketing'], categories['Sales'], categories['HR'], categories['Finance'], categories['Design'], categories['Customer Support'], categories['Non-IT']])
            experience_level = random.choice(['freshers', 'experienced'])
            Job.objects.create(
                title=title,
                company=company,
                category=category,
                description=f"{title} position in {category.name}. Join a dynamic team and grow your career.",
                requirements=f"- {random.choice(['Any degree', 'MBA', 'Relevant diploma'])}\n- {random.randint(0, 5)}+ years experience\n- {random.choice(['MS Office', 'CRM', 'Communication skills', 'Teamwork'])}",
                responsibilities=f"- {random.choice(['Manage', 'Support', 'Coordinate', 'Organize'])} daily operations\n- Interact with clients/customers\n- Prepare reports\n- Meet targets",
                location=random.choice(['Remote', 'Chennai', 'Hyderabad', 'Pune', 'Delhi', 'Mumbai', 'Kolkata']),
                employment_type="full-time",
                experience_level=experience_level,
                salary_min=30000 + i * 800,
                salary_max=50000 + i * 800,
                is_remote=random.choice([True, False]),
                deadline=timezone.now().date() + timedelta(days=random.randint(15, 60))
            )
        self.stdout.write('Created 60 Non-IT jobs.')
        self.stdout.write(self.style.SUCCESS('Sample IT and Non-IT jobs created successfully!')) 