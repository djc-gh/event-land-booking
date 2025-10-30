from django.contrib import admin
from .models import Booking, PriceSetting


class PriceSettingAdmin(admin.ModelAdmin):
    list_display = ['price_per_night', 'effective_from', 'is_active', 'created_at']
    list_filter = ['is_active', 'effective_from']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Price Information', {
            'fields': ('price_per_night', 'effective_from', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class BookingAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'guest_name', 
        'land', 
        'check_in', 
        'check_out', 
        'total_nights',
        'total_price',
        'status',
        'created_at'
    ]
    list_filter = ['status', 'check_in', 'check_out', 'created_at']
    search_fields = ['guest_name', 'guest_email', 'guest_phone', 'land__name']
    list_editable = ['status']
    readonly_fields = ['total_nights', 'total_price', 'created_at', 'updated_at']
    date_hierarchy = 'check_in'
    
    fieldsets = (
        ('Land Information', {
            'fields': ('land',)
        }),
        ('Guest Information', {
            'fields': ('guest_name', 'guest_email', 'guest_phone', 'number_of_guests')
        }),
        ('Booking Dates', {
            'fields': ('check_in', 'check_out')
        }),
        ('Pricing', {
            'fields': ('price_per_night', 'total_nights', 'total_price')
        }),
        ('Additional Information', {
            'fields': ('special_requests', 'status')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Optimize queries"""
        qs = super().get_queryset(request)
        return qs.select_related('land')

