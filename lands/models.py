from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Land(models.Model):
    """Model for camping land plots"""
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('maintenance', 'Under Maintenance'),
        ('unavailable', 'Unavailable'),
    ]
    
    name = models.CharField(max_length=200, help_text="Name of the camping plot")
    description = models.TextField(help_text="Detailed description of the plot")
    size = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        help_text="Size in square meters",
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    capacity = models.PositiveIntegerField(
        help_text="Maximum number of people",
        validators=[MinValueValidator(1)]
    )
    image = models.ImageField(
        upload_to='lands/', 
        blank=True, 
        null=True,
        help_text="Image of the camping plot"
    )
    amenities = models.TextField(
        blank=True,
        help_text="Available amenities (e.g., water, electricity, fire pit)"
    )
    price_per_night = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=50.00,
        help_text="Price per night for this specific plot",
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='available'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Land Plot"
        verbose_name_plural = "Land Plots"
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} - {self.get_status_display()}"
    
    def is_available(self):
        """Check if the land is available for booking"""
        return self.status == 'available'

