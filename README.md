# CampLand - Camping Land Booking Web Application

A modern Django web application for booking camping plots with Tailwind CSS styling.

## Features

- 🏕️ Browse and search available camping plots by date range
- 📅 Real-time availability checking
- 💳 Simple booking process (no user account required)
- 🎨 Modern UI/UX with Tailwind CSS
- 🔐 Admin panel for managing:
  - Camping plots (add, remove, set status)
  - Booking requests
  - Pricing settings
- 📱 Fully responsive design
- 🎯 Core pages: Home, About, Rules, Contact Us

## Tech Stack

- **Backend**: Django 5.2.7
- **Frontend**: Tailwind CSS 3.4
- **Database**: SQLite (development)
- **Python**: 3.12.3

## Installation & Setup

### 1. Prerequisites
- Python 3.12+
- Node.js and npm
- Virtual environment (already created in `.venv`)

### 2. Install Dependencies

The virtual environment and Python packages are already installed. If you need to reinstall:

```bash
# Activate virtual environment
source .venv/bin/activate

# Install Python packages
pip install django pillow django-tailwind python-decouple
```

Install Node.js dependencies:

```bash
npm install
```

### 3. Build Tailwind CSS

```bash
npm run build:css
```

For development with auto-rebuild:

```bash
npm run watch:css
```

### 4. Database Setup

Migrations are already applied. To reset:

```bash
python manage.py migrate
```

### 5. Create Admin Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to create your admin account.

### 6. Run Development Server

```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000/

## Admin Panel Setup

1. Access admin panel at: http://127.0.0.1:8000/admin/
2. Log in with your superuser credentials

### Add Price Settings

1. Go to **Price Settings** in admin
2. Click **Add Price Setting**
3. Set price per night (e.g., $50.00)
4. Set effective date (today's date)
5. Check "Is active"
6. Save

### Add Camping Plots

1. Go to **Land Plots** in admin
2. Click **Add Land Plot**
3. Fill in details:
   - **Name**: e.g., "Lakeside Plot A"
   - **Description**: Describe the plot
   - **Size**: e.g., 100.00 (square meters)
   - **Capacity**: e.g., 4 (people)
   - **Amenities**: e.g., "Electricity, Water, Fire Pit, Picnic Table"
   - **Status**: Available
   - **Image**: Upload an image (optional)
4. Save

Repeat to add multiple plots.

### View Bookings

- All booking requests appear in **Bookings** section
- You can change status (Pending → Confirmed → Completed)
- Filter by date, status, and search by guest name

## Project Structure

```
event-site-booking/
├── campland/              # Django project settings
│   ├── settings.py        # Project configuration
│   ├── urls.py           # Main URL routing
│   └── wsgi.py
├── core/                  # Core app (static pages)
│   ├── views.py          # Home, About, Rules, Contact
│   └── urls.py
├── lands/                 # Land management app
│   ├── models.py         # Land model
│   ├── admin.py          # Land admin
│   └── migrations/
├── bookings/              # Booking management app
│   ├── models.py         # Booking & PriceSetting models
│   ├── views.py          # Search & booking logic
│   ├── admin.py          # Booking admin
│   └── urls.py
├── templates/             # HTML templates
│   ├── base.html         # Base template
│   ├── home.html         # Homepage
│   ├── about.html        # About page
│   ├── rules.html        # Rules page
│   ├── contact.html      # Contact page
│   └── bookings/
│       ├── search.html          # Search availability
│       ├── booking_form.html    # Booking form
│       └── confirmation.html    # Booking confirmation
├── static/                # Static files
│   ├── css/
│   │   ├── input.css     # Tailwind source
│   │   └── output.css    # Compiled CSS
│   ├── js/
│   └── images/
├── media/                 # Uploaded files
├── manage.py
├── package.json          # npm dependencies
└── tailwind.config.js    # Tailwind configuration
```

## Usage Guide

### For Users (Website Visitors)

1. **Browse**: Visit the homepage to see features
2. **Search**: Select check-in and check-out dates
3. **View Results**: See available camping plots
4. **Book**: Click "Book This Plot" on desired plot
5. **Fill Form**: Enter guest information
6. **Confirm**: Review and submit booking request
7. **Wait**: Receive confirmation email within 24 hours

### For Administrators

1. **Manage Plots**: 
   - Add new plots with details and images
   - Update status (Available/Maintenance/Unavailable)
   - Edit amenities and capacity

2. **Review Bookings**:
   - View all booking requests
   - Change status (Pending → Confirmed)
   - Contact guests via email/phone

3. **Adjust Pricing**:
   - Create new price settings
   - Set effective dates
   - Activate/deactivate prices

## Color Scheme

- **Primary Color**: #e14d2a (Orange-Red)
- **Primary Dark**: #c43e1d
- **Primary Light**: #f56b42
- **No pink colors used** ✓

## Key Features

### Date-Based Availability Search
- Real-time checking of plot availability
- Prevents double-booking
- Validates date ranges

### No-Account Booking
- Users can book without creating accounts
- Simple form with guest information
- Email confirmation system ready

### Admin Dashboard
- Full CRUD operations on plots
- Booking management with status tracking
- Flexible pricing system
- Search and filter capabilities

### Responsive Design
- Mobile-first approach
- Modern, clean interface
- Smooth transitions and animations
- Accessible navigation

## Development Commands

```bash
# Run development server
python manage.py runserver

# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Build CSS (production)
npm run build:css

# Watch CSS (development)
npm run watch:css

# Collect static files (production)
python manage.py collectstatic
```

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers

## Future Enhancements

- Email notifications
- Payment integration
- SMS confirmations
- Calendar view
- Reviews and ratings
- Photo gallery
- Weather integration
- Map integration

## License

This project is created for CampLand camping site booking system.

## Support

For issues or questions:
- Email: info@campland.com
- Phone: (555) 123-4567
