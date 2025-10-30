"""
URL configuration for campland project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Import models and admin classes
from campland.admin import DashboardAdminSite
from lands.models import Land
from lands.admin import LandAdmin
from bookings.models import Booking, PriceSetting
from bookings.admin import BookingAdmin, PriceSettingAdmin
from django.contrib.auth.models import User, Group

# Create custom admin site instance
admin_site = DashboardAdminSite(name='admin')

# Register all models to the custom admin site
admin_site.register(Land, LandAdmin)
admin_site.register(Booking, BookingAdmin)
admin_site.register(PriceSetting, PriceSettingAdmin)
admin_site.register(User)
admin_site.register(Group)

urlpatterns = [
    path('admin/', admin_site.urls),
    path('', include('core.urls')),
    path('bookings/', include('bookings.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

