from django.contrib import admin

# Register your models here.
from .models import BattlefieldCompletion, ScheduledBattlefield, LiveBattlefield, ScanResult, AM_System, CG_System

@admin.register(BattlefieldCompletion)
class BattlefieldCompletionAdmin(admin.ModelAdmin):
    list_display = ('system', 'completion_time', 'winner', 'defender', "converted_to_scheduled")
    ordering = ('-completion_time',)  # Orders by completion time, newest first

@admin.register(ScheduledBattlefield)
class ScheduledBattlefieldAdmin(admin.ModelAdmin):
    list_display = ('system', 'expected_time', 'defender', 'fc')
    ordering = ('-expected_time',)

@admin.register(LiveBattlefield)
class LiveBattlefieldAdmin(admin.ModelAdmin):
    list_display = ('system','spawn_time', 'defender', 'fc')
    ordering = ('-spawn_time',)

@admin.register(ScanResult)
class ScanResultAdmin(admin.ModelAdmin):
    list_display = ('time', 'result_string')
    ordering = ('-time',)

@admin.register(CG_System)
class CGSystemAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'contested', 'caldari_objectives_advantage', 'gallente_objectives_advantage', 'caldari_systems_advantage', 'gallente_systems_advantage','base_advantage', 'last_updated')
    search_fields = ('name', 'status')
    list_filter = ('status', 'last_updated')
    ordering = ('name',)

@admin.register(AM_System)
class AMSystemAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'contested', 'amarr_objectives_advantage', 'minmatar_objectives_advantage', 'amarr_systems_advantage', 'minmatar_systems_advantage','base_advantage', 'last_updated')
    search_fields = ('name', 'status')
    list_filter = ('status', 'last_updated')
    ordering = ('name',)