from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone


def home(request):
    """Home page view"""
    context = {
        'today': timezone.now().date()
    }
    return render(request, 'home.html', context)


def about(request):
    """About page view"""
    return render(request, 'about.html')


def rules(request):
    """Rules page view"""
    return render(request, 'rules.html')


def contact(request):
    """Contact page view"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # In a real application, you would send an email here
        # For now, we'll just show a success message
        messages.success(
            request, 
            f'Thank you {name}! Your message has been received. We will get back to you soon.'
        )
        return redirect('contact')
    
    return render(request, 'contact.html')

