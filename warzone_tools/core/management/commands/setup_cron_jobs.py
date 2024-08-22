# myapp/management/commands/setup_cron_jobs.py
from django.core.management.base import BaseCommand
from rq_scheduler import Scheduler
from redis import Redis
from battlefield_tracker.tasks import report_completed_battlefields, convert_historic_to_scheduled_battlefield, convert_scheduled_to_live_battlefield
from battlefield_tracker.models import ScanResult

class Command(BaseCommand):
    help = 'Setup RQ Scheduler cron jobs'

    def handle(self, *args, **options):
        scheduler = Scheduler(connection=Redis(host="redis"))
        
        # Clear existing jobs to avoid duplication
        for job in scheduler.get_jobs():
            job.delete()

        scheduler.cron(
            cron_string='* * * * *',
            func=report_completed_battlefields,
            repeat=None  # Run indefinitely
        )
        scheduler.cron(
            cron_string='* * * * *',
            func=convert_historic_to_scheduled_battlefield,
            repeat=None  # Run indefinitely
        )
        scheduler.cron(
            cron_string='* * * * *',
            func=convert_scheduled_to_live_battlefield,
            repeat=None  # Run indefinitely
        )

        scheduler.cron(
            cron_string='0 12 * * *',  # Cron time string format
            func=ScanResult.delete_old_records,
            repeat=None  # Run indefinitely
        )
        self.stdout.write(self.style.SUCCESS('Successfully scheduled cron jobs.'))