from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from datetime import datetime, timedelta, date
from calendar import monthcalendar, month_name
from lands.models import Land
from .models import Booking, PriceSetting


def search_availability(request):
    """Search for available camping plots"""
    available_lands = []
    booked_lands = []
    check_in = None
    check_out = None
    total_nights = 0
    
    if request.GET.get('check_in') and request.GET.get('check_out'):
        check_in_str = request.GET.get('check_in')
        check_out_str = request.GET.get('check_out')
        
        try:
            check_in = datetime.strptime(check_in_str, '%Y-%m-%d').date()
            check_out = datetime.strptime(check_out_str, '%Y-%m-%d').date()
            
            # Validate dates
            if check_out <= check_in:
                messages.error(request, 'Check-out date must be after check-in date.')
            elif check_in < timezone.now().date():
                messages.error(request, 'Check-in date cannot be in the past.')
            else:
                # Calculate nights
                total_nights = (check_out - check_in).days
                
                # Get all available lands
                all_lands = Land.objects.filter(status='available')
                
                # Separate lands into available and booked
                for land in all_lands:
                    # Check if there are any overlapping bookings
                    overlapping_bookings = Booking.objects.filter(
                        land=land,
                        status__in=['pending', 'confirmed'],
                        check_in__lt=check_out,
                        check_out__gt=check_in
                    ).exists()
                    
                    if not overlapping_bookings:
                        available_lands.append(land)
                    else:
                        booked_lands.append(land)
                
                if not available_lands and not booked_lands:
                    messages.info(request, 'No camping plots found. Please try different dates.')
        
        except ValueError:
            messages.error(request, 'Invalid date format. Please use the date picker.')
    
    context = {
        'available_lands': available_lands,
        'booked_lands': booked_lands,
        'check_in': check_in,
        'check_out': check_out,
        'total_nights': total_nights,
        'today': timezone.now().date(),
    }
    
    return render(request, 'bookings/search.html', context)


def booking_form(request, land_id):
    """Booking form for a specific land"""
    land = get_object_or_404(Land, id=land_id, status='available')
    
    # Get dates from query parameters
    check_in_str = request.GET.get('check_in')
    check_out_str = request.GET.get('check_out')
    
    if not check_in_str or not check_out_str:
        messages.error(request, 'Please select check-in and check-out dates.')
        return redirect('search_availability')
    
    try:
        check_in = datetime.strptime(check_in_str, '%Y-%m-%d').date()
        check_out = datetime.strptime(check_out_str, '%Y-%m-%d').date()
    except ValueError:
        messages.error(request, 'Invalid date format.')
        return redirect('search_availability')
    
    # Validate dates
    if check_out <= check_in:
        messages.error(request, 'Check-out date must be after check-in date.')
        return redirect('search_availability')
    
    if check_in < timezone.now().date():
        messages.error(request, 'Check-in date cannot be in the past.')
        return redirect('search_availability')
    
    # Check availability
    overlapping_bookings = Booking.objects.filter(
        land=land,
        status__in=['pending', 'confirmed'],
        check_in__lt=check_out,
        check_out__gt=check_in
    ).exists()
    
    if overlapping_bookings:
        messages.error(request, 'This plot is no longer available for the selected dates.')
        return redirect('search_availability')
    
    total_nights = (check_out - check_in).days
    price_per_night = land.price_per_night  # Use plot's price instead of global price
    total_price = price_per_night * total_nights
    
    if request.method == 'POST':
        # Get form data with new field names
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        guest_name = f"{first_name} {last_name}"
        guest_email = request.POST.get('guest_email')
        number_of_persons = request.POST.get('number_of_persons')
        number_of_children = request.POST.get('number_of_children', 0)
        site_location = request.POST.get('site_location', '')
        event_summary = request.POST.get('event_summary', '')
        
        # Store phone in special_requests for now (since we don't have a phone field in model)
        special_requests = f"Site Location Preference: {site_location}\n"
        special_requests += f"Number of Children: {number_of_children}\n"
        special_requests += f"Event Type: {event_summary}"
        
        try:
            number_of_guests = int(number_of_persons)
            
            # Validate capacity
            if number_of_guests > land.capacity:
                messages.error(
                    request, 
                    f'Number of guests ({number_of_guests}) exceeds plot capacity ({land.capacity}).'
                )
            else:
                # Create booking
                booking = Booking.objects.create(
                    land=land,
                    guest_name=guest_name,
                    guest_email=guest_email,
                    guest_phone='',  # We'll store additional info in special_requests
                    number_of_guests=number_of_guests,
                    check_in=check_in,
                    check_out=check_out,
                    price_per_night=price_per_night,
                    special_requests=special_requests,
                    status='pending'
                )
                
                messages.success(
                    request,
                    f'Booking request submitted successfully! Booking ID: {booking.id}. '
                    'We will contact you soon to confirm your reservation.'
                )
                return redirect('booking_confirmation', booking_id=booking.id)
        
        except (ValueError, TypeError):
            messages.error(request, 'Invalid number of guests.')
    
    context = {
        'land': land,
        'check_in': check_in,
        'check_out': check_out,
        'total_nights': total_nights,
        'price_per_night': price_per_night,
        'total_price': total_price,
    }
    
    return render(request, 'bookings/booking_form.html', context)


def booking_confirmation(request, booking_id):
    """Booking confirmation page"""
    booking = get_object_or_404(Booking, id=booking_id)
    
    context = {
        'booking': booking,
    }
    
    return render(request, 'bookings/confirmation.html', context)


def land_availability_calendar(request, land_id):
    """Display availability calendar for a specific land"""
    land = get_object_or_404(Land, id=land_id, status='available')
    
    # Get month and year from request or use current
    year = int(request.GET.get('year', timezone.now().year))
    month = int(request.GET.get('month', timezone.now().month))
    
    # Handle month navigation
    if month < 1:
        month = 12
        year -= 1
    elif month > 12:
        month = 1
        year += 1
    
    # Get calendar data
    cal = monthcalendar(year, month)
    
    # Get all bookings for this land
    bookings = Booking.objects.filter(
        land=land,
        status__in=['pending', 'confirmed']
    )
    
    # Create a set of booked dates
    booked_dates = set()
    for booking in bookings:
        current_date = booking.check_in
        while current_date < booking.check_out:
            booked_dates.add(current_date)
            current_date += timedelta(days=1)
    
    # Enhance calendar with status info
    enhanced_cal = []
    today = timezone.now().date()
    
    for week in cal:
        enhanced_week = []
        for day in week:
            if day == 0:
                enhanced_week.append({
                    'day': 0,
                    'date': None,
                    'status': 'other_month',
                    'is_booked': False,
                    'is_past': False,
                })
            else:
                current_date = date(year, month, day)
                is_booked = current_date in booked_dates
                is_past = current_date < today
                
                status = 'past' if is_past else 'booked' if is_booked else 'available'
                
                enhanced_week.append({
                    'day': day,
                    'date': current_date,
                    'status': status,
                    'is_booked': is_booked,
                    'is_past': is_past,
                })
        enhanced_cal.append(enhanced_week)
    
    # Navigation dates
    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1
    
    context = {
        'land': land,
        'enhanced_cal': enhanced_cal,
        'month': month,
        'year': year,
        'current_year': year,
        'month_name': month_name[month],
        'prev_month': prev_month,
        'prev_year': prev_year,
        'next_month': next_month,
        'next_year': next_year,
        'today': today,
    }
    
    return render(request, 'bookings/availability_calendar.html', context)