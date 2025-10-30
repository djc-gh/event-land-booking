from django.contrib import admin
from django import forms
from .models import Land
from bookings.models import PriceSetting


class LandAdminForm(forms.ModelForm):
    """Custom form for Land admin with price dropdown"""
    price_choice = forms.ModelChoiceField(
        queryset=PriceSetting.objects.all().order_by('-price_per_night'),
        required=True,
        widget=forms.Select(),
        label="Price per Night (from Price Settings)",
        help_text="Select a price from available price settings"
    )
    
    class Meta:
        model = Land
        fields = '__all__'
        exclude = ['price_per_night']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize the queryset display
        self.fields['price_choice'].queryset = PriceSetting.objects.all().order_by('-price_per_night')
        self.fields['price_choice'].label_from_instance = lambda obj: f"${obj.price_per_night}/night (from {obj.effective_from})"
        
        # Pre-select current price if editing
        if self.instance.pk and self.instance.price_per_night:
            try:
                price_setting = PriceSetting.objects.get(price_per_night=self.instance.price_per_night)
                self.fields['price_choice'].initial = price_setting
            except PriceSetting.DoesNotExist:
                pass
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        # Extract the decimal price from the selected PriceSetting
        price_setting = self.cleaned_data.get('price_choice')
        if price_setting:
            instance.price_per_night = price_setting.price_per_night
        if commit:
            instance.save()
        return instance


class LandAdmin(admin.ModelAdmin):
    form = LandAdminForm
    list_display = ['name', 'size', 'capacity', 'price_per_night', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'description', 'amenities']
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at', 'price_per_night']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'image')
        }),
        ('Details', {
            'fields': ('size', 'capacity', 'amenities')
        }),
        ('Pricing', {
            'fields': ('price_choice', 'price_per_night'),
            'description': 'Select the price per night for this specific RV site from available price settings'
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

