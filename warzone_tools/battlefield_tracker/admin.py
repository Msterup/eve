from django.contrib import admin

# Register your models here.
from .models import BattlefieldCompletion, ScheduledBattlefield, LiveBattlefield, ScanResult

@admin.register(BattlefieldCompletion)
class BattlefieldCompletionAdmin(admin.ModelAdmin):
    list_display = ('system', 'completion_time', 'winner', 'defender', "converted_to_scheduled")
    ordering = ('-completion_time',)  # Orders by completion time, newest first

@admin.register(ScheduledBattlefield)
class ScheduledBattlefieldAdmin(admin.ModelAdmin):
    list_display = ('expected_time', 'defender', 'fc')
    ordering = ('-expected_time',)

@admin.register(LiveBattlefield)
class LiveBattlefieldAdmin(admin.ModelAdmin):
    list_display = ('spawn_time', 'defender', 'fc')
    ordering = ('-spawn_time',)

@admin.register(ScanResult)
class ScanResultAdmin(admin.ModelAdmin):
    list_display = ('time', 'result_string')
    ordering = ('-time',)