from django.contrib import admin
from .models import SolarSystem, FactionAdvantage, SolarSystemDelta, FactionAdvantageDelta, BattlefieldCompletion, ScheduledBattlefield

@admin.register(SolarSystem)
class SolarSystemAdmin(admin.ModelAdmin):
    list_display = ('solarsystem_id', 'owner_faction', 'occupier_faction', 'contested_status', 'contested_amount')
    search_fields = ('solarsystem_id', 'owner_faction', 'occupier_faction', 'contested_status')
    list_filter = ('owner_faction', 'occupier_faction', 'contested_status')

@admin.register(FactionAdvantage)
class FactionAdvantageAdmin(admin.ModelAdmin):
    list_display = ('solar_system', 'faction_id', 'terrain_amount', 'dynamic_amount', 'total_amount')
    search_fields = ('solar_system__solarsystem_id', 'faction_id')
    list_filter = ('faction_id',)

@admin.register(SolarSystemDelta)
class SolarSystemDeltaAdmin(admin.ModelAdmin):
    list_display = ('solar_system', 'timestamp', 'owner_faction', 'occupier_faction', 'contested_status', 'contested_amount')
    search_fields = ('solar_system__solarsystem_id',)
    list_filter = ('owner_faction', 'occupier_faction', 'contested_status')

@admin.register(FactionAdvantageDelta)
class FactionAdvantageDeltaAdmin(admin.ModelAdmin):
    list_display = ('faction_advantage', 'timestamp', 'terrain_amount', 'dynamic_amount', 'total_amount')
    search_fields = ('faction_advantage__solar_system__solarsystem_id', 'faction_advantage__faction_id')
    list_filter = ('faction_advantage__faction_id',)

@admin.register(BattlefieldCompletion)
class BattlefieldCompletionAdmin(admin.ModelAdmin):
    list_display = ('completion_time', 'winner', 'defender', 'solar_system', 'fc')
    search_fields = ('solar_system__solarsystem_id', 'winner', 'defender')
    list_filter = ('winner', 'defender')

@admin.register(ScheduledBattlefield)
class ScheduledBattlefieldAdmin(admin.ModelAdmin):
    list_display = ('battlefield_type', 'defender', 'fc', 'spawn_time', 'expected_time', 'is_between_downtime_and_four_hours_after')
    search_fields = ('defender', 'fc', 'battlefield_type')
    list_filter = ('battlefield_type', 'defender', 'is_between_downtime_and_four_hours_after')