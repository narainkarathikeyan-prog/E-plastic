from django.contrib import admin
from .models import PlasticType, CollectionCenter, WasteSubmission, RecyclingData, DataMiningReport

@admin.register(PlasticType)
class PlasticTypeAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'recyclable', 'hazard_level']

@admin.register(CollectionCenter)
class CollectionCenterAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'state', 'capacity_kg', 'is_active']
    list_filter = ['is_active', 'state']

@admin.register(WasteSubmission)
class WasteSubmissionAdmin(admin.ModelAdmin):
    list_display = ['id', 'submitter_name', 'plastic_type', 'weight_kg', 'status', 'submitted_at']
    list_filter = ['status', 'plastic_type']
    search_fields = ['submitter_name', 'submitter_email']
    # Put this line inside your existing WasteSubmissionAdmin class
    actions = ['mark_as_collected', 'mark_as_processing', 'mark_as_recycled', 'mark_as_rejected']

    @admin.action(description='Mark selected submissions as Collected')
    def mark_as_collected(self, request, queryset):
        queryset.update(status='collected')

    @admin.action(description='Mark selected submissions as Processing')
    def mark_as_processing(self, request, queryset):
        queryset.update(status='processing')

    @admin.action(description='Mark selected submissions as Recycled')
    def mark_as_recycled(self, request, queryset):
        queryset.update(status='recycled')

    @admin.action(description='Mark selected submissions as Rejected')
    def mark_as_rejected(self, request, queryset):
        queryset.update(status='rejected')
@admin.register(RecyclingData)
class RecyclingDataAdmin(admin.ModelAdmin):
    list_display = ['month', 'year', 'total_collected_kg', 'total_recycled_kg']

@admin.register(DataMiningReport)
class DataMiningReportAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'trend', 'created_at']
