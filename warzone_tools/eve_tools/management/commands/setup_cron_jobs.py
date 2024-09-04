# myapp/management/commands/setup_cron_jobs.py
from django.core.management.base import BaseCommand
from rq_scheduler import Scheduler
from redis import Redis
from eve_tools.tasks import report_completed_battlefields, create_downtime_scheduled_battlefields, delete_non_downtime_battlefields
from datetime import timedelta
from django.conf import settings

class Command(BaseCommand):
    help = 'Setup RQ Scheduler cron jobs'

    def handle(self, *args, **options):
        REDIS_PASSWORD = settings.REDIS_PASSWORD
        scheduler = Scheduler(connection=Redis(host="redis", password=REDIS_PASSWORD))
        
        # Clear existing jobs to avoid duplication
        for job in scheduler.get_jobs():
            job.delete()

        scheduler.cron(
            cron_string='*/1 * * * *',
            func=report_completed_battlefields,
            repeat=None,  # Run indefinitely
            timeout=600,
            result_ttl=timedelta(hours=18).total_seconds(),
        )
        
        scheduler.cron(
            cron_string='0 7 * * *',
            func=create_downtime_scheduled_battlefields,
            repeat=None,  # Run indefinitely
            timeout=600,
            result_ttl=timedelta(hours=18).total_seconds(),
        )
        
        scheduler.cron(
            cron_string='0 11 * * *',
            func=delete_non_downtime_battlefields,
            repeat=None,  # Run indefinitely
            timeout=600,
            result_ttl=timedelta(hours=18).total_seconds(),
        )
        
        self.stdout.write(self.style.SUCCESS('Successfully scheduled cron jobs.'))
