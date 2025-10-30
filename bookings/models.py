from django.db import models
from django.core.validators import MinValueValidator, EmailValidator
from django.utils import timezone
from lands.models import Land
from decimal import Decimal


class PriceSetting(models.Model):
    """Model for managing booking prices"""
    price_per_night = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        help_text="Price per night for booking"
    )
    effective_from = models.DateField(
        default=timezone.now,
        help_text="Date when this price becomes effective"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Price Setting"
        verbose_name_plural = "Price Settings"
        ordering = ['-effective_from']
    
    def __str__(self):
        return f"${self.price_per_night}/night (from {self.effective_from})"
    
    @classmethod
    def get_current_price(cls):
        """Get the current active price"""
        today = timezone.now().date()
        price_setting = cls.objects.filter(
            is_active=True,
            effective_from__lte=today
        ).first()
        return price_setting.price_per_night if price_setting else Decimal('50.00')


class Booking(models.Model):
    """Model for camping bookings"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    # Land being booked
    land = models.ForeignKey(
        Land,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    
    # Guest information
    guest_name = models.CharField(max_length=200)
    guest_email = models.EmailField(validators=[EmailValidator()])
    guest_phone = models.CharField(max_length=20)
    number_of_guests = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Number of people"
    )
    
    # Booking dates
    check_in = models.DateField()
    check_out = models.DateField()
    
    # Pricing
    price_per_night = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    total_nights = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    
    # Additional information
    special_requests = models.TextField(blank=True)
    
    # Status and timestamps
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.guest_name} - {self.land.name} ({self.check_in} to {self.check_out})"
    
    def save(self, *args, **kwargs):
        """Calculate total nights and price before saving"""
        if self.check_in and self.check_out:
            delta = self.check_out - self.check_in
            self.total_nights = delta.days
            self.total_price = self.price_per_night * self.total_nights
        super().save(*args, **kwargs)
    
    def clean(self):
        """Validate booking dates"""
        from django.core.exceptions import ValidationError
        
        if self.check_in and self.check_out:
            if self.check_out <= self.check_in:
                raise ValidationError("Check-out date must be after check-in date")
            
            if self.check_in < timezone.now().date():
                raise ValidationError("Check-in date cannot be in the past")
        
        if self.number_of_guests and self.land:
            if self.number_of_guests > self.land.capacity:
                raise ValidationError(
                    f"Number of guests ({self.number_of_guests}) exceeds land capacity ({self.land.capacity})"
                )

