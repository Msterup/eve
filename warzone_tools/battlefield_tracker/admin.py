from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import ScanResult, BattlefieldCompletion

@admin.register(ScanResult)
class ScanResultAdmin(admin.ModelAdmin):
    list_display = ('time', 'result_string')
    search_fields = ('result_string',)

@admin.register(BattlefieldCompletion)
class BattlefieldCompletionAdmin(admin.ModelAdmin):
    list_display = ('time', 'winner', 'system')
    list_filter = ('winner', 'system')
    search_fields = ('system', 'winner')
    ordering = ('-time',)