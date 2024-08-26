# myapp/management/commands/setup_cron_jobs.py
from django.core.management.base import BaseCommand
from rq_scheduler import Scheduler
from redis import Redis
from battlefield_tracker.tasks import report_completed_battlefields, convert_historic_to_scheduled_battlefield, convert_scheduled_to_live_battlefield, create_downtime_scheduled_battlefields 
from battlefield_tracker.models import ScanResult
from datetime import timedelta


class Command(BaseCommand):
    help = 'Setup RQ Scheduler cron jobs'

    def handle(self, *args, **options):
        scheduler = Scheduler(connection=Redis(host="redis"))
        
        # Clear existing jobs to avoid duplication
        for job in scheduler.get_jobs():
            job.delete()

        factions = ['caldari', 'amarr']

        # Schedule report_completed_battlefields for each faction
        for faction in factions:
            scheduler.cron(
                cron_string='*/1 * * * *',
                func=report_completed_battlefields,
                args=[faction, "Frontline"],  # Pass faction as argument
                repeat=None,  # Run indefinitely
                timeout=600,
                result_ttl=timedelta(hours=18).total_seconds(),

            )
        # Schedule report_completed_battlefields for each faction
        for faction in factions:
            scheduler.cron(
                cron_string='*/10 * * * *',
                func=report_completed_battlefields,
                args=[faction, "Command Operations"],  # Pass faction as argument
                repeat=None,  # Run indefinitely
                timeout=600,
                result_ttl=timedelta(hours=18).total_seconds(),
            )
        # Schedule report_completed_battlefields for each faction
        scheduler.cron(
            cron_string='45 * * * *',
            func=report_completed_battlefields,
            args=[faction, "Rearguard"],  # Pass faction as argument
            repeat=None,  # Run indefinitely
            timeout=600,
            result_ttl=timedelta(hours=18).total_seconds(),
        )
        scheduler.cron(
            cron_string='15 * * * *',
            func=report_completed_battlefields,
            args=[faction, "Rearguard"],  # Pass faction as argument
            repeat=None,  # Run indefinitely
            timeout=600,
            result_ttl=timedelta(hours=18).total_seconds(),
        )

        # Schedule conversion and cleanup tasks
        scheduler.cron(
            cron_string='*/1 * * * *',
            func=convert_historic_to_scheduled_battlefield,
            repeat=None  # Run indefinitely
        )
        scheduler.cron(
            cron_string='*/1 * * * *',
            func=convert_scheduled_to_live_battlefield,
            repeat=None,  # Run indefinitely
            result_ttl=timedelta(hours=18).total_seconds(),
        )

        # Schedule create_downtime_scheduled_battlefields to run every day at 9 AM
        scheduler.cron(
            cron_string='0 9 * * *',
            func=create_downtime_scheduled_battlefields,
            repeat=None,  # Run indefinitely
            result_ttl=timedelta(hours=18).total_seconds(),
        )

        # Schedule ScanResult.delete_old_records to run every day at 11 AM
        scheduler.cron(
            cron_string='0 11 * * *',  # Cron time string format
            func=ScanResult.delete_old_records,
            repeat=None,  # Run indefinitely
            result_ttl=timedelta(hours=18).total_seconds(),
            kwargs={'days': 3},  # Ensure 'days' argument is passed correctly
        )

        self.stdout.write(self.style.SUCCESS('Successfully scheduled cron jobs.'))
