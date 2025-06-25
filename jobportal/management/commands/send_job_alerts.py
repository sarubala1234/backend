from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from jobportal.models import SavedSearch, Job
from django.conf import settings
from django.utils import timezone

class Command(BaseCommand):
    help = 'Send job alert emails to users based on their saved searches.'

    def handle(self, *args, **options):
        User = get_user_model()
        for saved_search in SavedSearch.objects.select_related('user').all():
            user = saved_search.user
            if not user.email:
                continue
            # Build job queryset based on saved search criteria
            jobs = Job.objects.filter(is_active=True)
            if saved_search.keyword:
                jobs = jobs.filter(title__icontains=saved_search.keyword)
            if saved_search.location:
                jobs = jobs.filter(location__icontains=saved_search.location)
            if saved_search.category:
                jobs = jobs.filter(category=saved_search.category)
            if saved_search.employment_type:
                jobs = jobs.filter(employment_type=saved_search.employment_type)
            if saved_search.experience_level:
                jobs = jobs.filter(experience_level=saved_search.experience_level)
            if saved_search.is_remote:
                jobs = jobs.filter(is_remote=True)
            # Only show jobs posted in the last 24 hours
            jobs = jobs.filter(created_at__gte=timezone.now()-timezone.timedelta(days=1))
            if not jobs.exists():
                continue
            # Build email content
            subject = 'New Job Alerts from Job Portal'
            message = f'Hi {user.get_full_name() or user.username},\n\nHere are new jobs matching your saved search:'
            for job in jobs:
                message += f"\n- {job.title} ({job.location}) - {job.get_employment_type_display()} - {job.get_experience_level_display()}\n  View: https://yourdomain.com/job/{job.id}/"
            message += '\n\nLogin to your dashboard for more details.'
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            self.stdout.write(self.style.SUCCESS(f'Sent job alert to {user.email}')) 