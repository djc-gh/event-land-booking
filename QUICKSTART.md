# Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Activate Virtual Environment & Create Admin Account
```bash
# First, activate the virtual environment
source .venv/bin/activate

# Then create superuser
python manage.py createsuperuser
```
Follow prompts to create your admin username, email, and password.

**Note:** You must activate the virtual environment before running any Django commands!

### Step 2: Start the Server
```bash
./start.sh
```
Or manually:
```bash
python manage.py runserver
```

### Step 3: Access the Application

**Main Website:**
- URL: http://127.0.0.1:8000/
- Browse camping plots
- Search by dates
- Make bookings

**Admin Panel:**
- URL: http://127.0.0.1:8000/admin/
- Login with superuser credentials
- Manage plots, bookings, and pricing

## ✅ What's Already Done

- ✓ Django project configured
- ✓ Database migrated
- ✓ 10 sample camping plots added
- ✓ Price setting ($50/night) configured
- ✓ All templates created with Tailwind CSS
- ✓ Booking system fully functional
- ✓ Admin panel customized

## 📋 Key Pages

1. **Home** (`/`) - Hero section with quick search
2. **About** (`/about/`) - Company story and mission
3. **Rules** (`/rules/`) - Camping rules and guidelines
4. **Contact** (`/contact/`) - Contact form and information
5. **Search** (`/bookings/search/`) - Find available plots by date
6. **Booking** (`/bookings/book/<id>/`) - Complete booking form
7. **Confirmation** - Booking confirmation page

## 🎨 Color Theme

- Primary: **#e14d2a** (Orange-Red)
- No pink colors used ✓
- Modern, clean design

## 💡 Tips

### Adding More Plots
1. Go to Admin Panel
2. Click "Land Plots" → "Add Land Plot"
3. Fill in details (name, description, size, capacity, amenities)
4. Upload image (optional)
5. Set status to "Available"
6. Save

### Managing Bookings
1. All bookings appear in "Bookings" section
2. Change status: Pending → Confirmed → Completed
3. View guest details and special requests
4. Contact guests via email/phone shown in booking

### Adjusting Prices
1. Go to "Price Settings"
2. Add new price setting
3. Set effective date
4. Mark as "Active"
5. Older prices remain for historical bookings

## 🔧 Development Commands

**Important: Always activate the virtual environment first!**
```bash
# Activate virtual environment (do this first!)
source .venv/bin/activate
```

Then run any of these commands:
```bash
# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver

# Build CSS (production)
npm run build:css

# Watch CSS (development - auto-rebuild)
npm run watch:css

# Add sample data (if needed again)
python manage.py populate_sample_data
```

## 📱 Test the Booking Flow

1. Visit homepage
2. Enter check-in date (today or later)
3. Enter check-out date (after check-in)
4. Click "Search Available Plots"
5. Browse available plots
6. Click "Book This Plot" on any plot
7. Fill in guest information
8. Submit booking request
9. View confirmation page
10. Check admin panel to see the booking

## 🎯 Project Structure Highlights

```
Key Files:
├── campland/settings.py    # Django settings
├── lands/models.py         # Land plot model
├── bookings/models.py      # Booking & pricing models
├── bookings/views.py       # Search & booking logic
├── templates/              # All HTML templates
│   ├── base.html          # Base template with navbar
│   ├── home.html          # Homepage
│   └── bookings/          # Booking templates
└── static/css/            # Tailwind CSS files
```

## 🐛 Troubleshooting

**CSS not loading?**
```bash
npm run build:css
python manage.py runserver
```

**Database issues?**
```bash
python manage.py migrate
python manage.py populate_sample_data
```

**Port already in use?**
```bash
python manage.py runserver 8080
```

## 🌟 Features Implemented

✓ Date-based availability search
✓ Real-time booking conflict detection
✓ Guest booking without account
✓ Admin plot management (add/remove/status)
✓ Admin booking management
✓ Adjustable pricing from admin
✓ Responsive modern design
✓ All core pages (Home, About, Rules, Contact)
✓ Form validation
✓ Success messages
✓ Mobile-friendly navigation

---

**Need help?** Check README.md for detailed documentation.
