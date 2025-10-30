from django.contrib import admin
from django.db.models import Sum, Count, Q, Avg, F
from datetime import timedelta, datetime
from django.utils import timezone
from lands.models import Land
from bookings.models import Booking, PriceSetting


class DashboardAdminSite(admin.AdminSite):
    """Custom admin site with integrated analytics dashboard"""
    site_header = "RIVIÈRE RV PARK Administration"
    site_title = "RIVIÈRE RV PARK Admin"
    index_title = "Dashboard & Analytics"
    
    def index(self, request, extra_context=None):
        """Override admin index to include dashboard analytics"""
        
        # Calculate analytics
        today = timezone.now().date()
        last_30_days = today - timedelta(days=30)
        last_90_days = today - timedelta(days=90)
        
        # Overall Statistics
        total_bookings = Booking.objects.count()
        total_lands = Land.objects.count()
        total_revenue = Booking.objects.filter(status__in=['confirmed', 'completed']).aggregate(Sum('total_price'))['total_price__sum'] or 0
        pending_bookings = Booking.objects.filter(status='pending').count()
        
        # Booking Status Distribution
        status_distribution = Booking.objects.values('status').annotate(count=Count('id')).order_by('status')
        
        # Land Status Distribution
        land_status = Land.objects.values('status').annotate(count=Count('id')).order_by('status')
        
        # Recent Bookings (last 10)
        recent_bookings = Booking.objects.select_related('land').order_by('-created_at')[:10]
        
        # Last 30 Days Bookings
        bookings_last_30 = Booking.objects.filter(created_at__gte=last_30_days)
        bookings_30_count = bookings_last_30.count()
        revenue_30 = bookings_last_30.filter(status__in=['confirmed', 'completed']).aggregate(Sum('total_price'))['total_price__sum'] or 0
        
        # Last 90 Days Bookings
        bookings_last_90 = Booking.objects.filter(created_at__gte=last_90_days)
        bookings_90_count = bookings_last_90.count()
        revenue_90 = bookings_last_90.filter(status__in=['confirmed', 'completed']).aggregate(Sum('total_price'))['total_price__sum'] or 0
        
        # Occupancy Rate
        total_land_days = total_lands * 30  # 30 days
        booked_nights = Booking.objects.filter(
            status__in=['pending', 'confirmed', 'completed'],
            check_in__gte=last_30_days
        ).aggregate(Sum('total_nights'))['total_nights__sum'] or 0
        occupancy_rate = (booked_nights / total_land_days * 100) if total_land_days > 0 else 0
        
        # Average Booking Value
        avg_booking_value = Booking.objects.filter(status__in=['confirmed', 'completed']).aggregate(Avg('total_price'))['total_price__avg'] or 0
        avg_booking_nights = Booking.objects.aggregate(Avg('total_nights'))['total_nights__avg'] or 0
        
        # Top Performing Lands (by bookings)
        top_lands = Land.objects.annotate(
            booking_count=Count('bookings')
        ).order_by('-booking_count')[:5]
        
        # Top Lands by Revenue
        top_lands_revenue = Land.objects.annotate(
            total_revenue=Sum('bookings__total_price')
        ).filter(total_revenue__isnull=False).order_by('-total_revenue')[:5]
        
        # Upcoming Bookings (next 30 days)
        upcoming_bookings = Booking.objects.filter(
            check_in__gte=today,
            check_in__lte=today + timedelta(days=30),
            status__in=['pending', 'confirmed']
        ).select_related('land').order_by('check_in')[:10]
        
        # Booking Timeline Data (for charts) - Last 30 days
        booking_timeline = []
        for i in range(30, -1, -1):
            date = today - timedelta(days=i)
            count = Booking.objects.filter(created_at__date=date).count()
            booking_timeline.append({
                'date': date.strftime('%m-%d'),
                'count': count
            })
        
        # Revenue Timeline Data (for charts) - Last 30 days
        revenue_timeline = []
        for i in range(30, -1, -1):
            date = today - timedelta(days=i)
            rev = Booking.objects.filter(
                created_at__date=date,
                status__in=['confirmed', 'completed']
            ).aggregate(Sum('total_price'))['total_price__sum'] or 0
            revenue_timeline.append({
                'date': date.strftime('%m-%d'),
                'revenue': float(rev)
            })
        
        # Prepare extra context with analytics data
        analytics_context = {
            'total_bookings': total_bookings,
            'total_lands': total_lands,
            'total_revenue': float(total_revenue),
            'pending_bookings': pending_bookings,
            'status_distribution': list(status_distribution),
            'land_status': list(land_status),
            'recent_bookings': recent_bookings,
            'upcoming_bookings': upcoming_bookings,
            'bookings_30_count': bookings_30_count,
            'revenue_30': float(revenue_30),
            'bookings_90_count': bookings_90_count,
            'revenue_90': float(revenue_90),
            'occupancy_rate': round(occupancy_rate, 2),
            'avg_booking_value': float(avg_booking_value),
            'avg_booking_nights': round(avg_booking_nights, 2),
            'top_lands': top_lands,
            'top_lands_revenue': top_lands_revenue,
            'booking_timeline': booking_timeline,
            'revenue_timeline': revenue_timeline,
            'today': today,
        }
        
        if extra_context is None:
            extra_context = {}
        extra_context.update(analytics_context)
        
        return super().index(request, extra_context=extra_context)
