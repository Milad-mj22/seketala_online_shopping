from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Complaint


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display  = ('id', 'name', 'phone', 'subject', 'status', 'created_at')
    list_filter   = ('status', 'subject', 'created_at')
    search_fields = ('name', 'phone', 'email', 'order_id', 'message')
    readonly_fields = ('name', 'phone', 'email', 'order_id', 'subject',
                       'message', 'ip_address', 'user_agent', 'created_at')
    list_per_page = 50

    actions = ['mark_in_progress', 'mark_resolved', 'mark_rejected']

    @admin.action(description='علامت‌گذاری به عنوان در حال بررسی')
    def mark_in_progress(self, request, queryset):
        queryset.update(status='in_progress')

    @admin.action(description='علامت‌گذاری به عنوان حل شده')
    def mark_resolved(self, request, queryset):
        queryset.update(status='resolved')

    @admin.action(description='علامت‌گذاری به عنوان رد شده')
    def mark_rejected(self, request, queryset):
        queryset.update(status='rejected')