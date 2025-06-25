from django.core.management.base import BaseCommand
from jobportal.models import Company, Job

class Command(BaseCommand):
    help = 'Delete all jobs and companies with "demo" in their name (case-insensitive).'

    def handle(self, *args, **options):
        demo_companies = Company.objects.filter(name__icontains='demo')
        demo_jobs = Job.objects.filter(company__in=demo_companies)
        job_count = demo_jobs.count()
        company_count = demo_companies.count()
        demo_jobs.delete()
        demo_companies.delete()
        self.stdout.write(self.style.SUCCESS(f'Deleted {job_count} jobs and {company_count} demo company(ies).')) 