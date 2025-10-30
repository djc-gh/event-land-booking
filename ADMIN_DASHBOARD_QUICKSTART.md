# Admin Dashboard - Quick Start

## View the Analytics Dashboard

1. **Start the server:**
   ```bash
   cd /home/ubuntu/Desktop/ubupay/event-site-booking
   source .venv/bin/activate
   python manage.py runserver
   ```

2. **Open admin in browser:**
   ```
   http://localhost:8000/admin/
   ```

3. **Login with your admin credentials**

4. **See the dashboard immediately:**
   - Analytics metrics cards (revenue, bookings, occupancy, etc.)
   - Interactive charts (bookings timeline, revenue, status distribution)
   - Recent bookings table
   - Upcoming bookings table
   - Top performing sites
   - All integrated into the standard admin interface

## What You'll See

### Top Section - Analytics Dashboard
- **Key Metrics**: Revenue, bookings, sites, pending, occupancy, average value, stay length
- **30/90 Day Stats**: Period-specific metrics
- **Interactive Charts**: 
  - Booking Timeline (30 days)
  - Revenue Timeline (30 days)
  - Booking Status Distribution
  - Site Status Distribution
- **Top Performers**: Sites by bookings and revenue
- **Recent Bookings**: Last 10 bookings
- **Upcoming Bookings**: Next 30 days

### Bottom Section - Standard Django Admin
- All your usual admin apps (Lands, Bookings, Price Settings)
- All functionality unchanged

## Key Metrics Explained

| Metric | Meaning |
|--------|---------|
| Total Revenue | All-time revenue from confirmed/completed bookings |
| Total Bookings | Count of all bookings across all statuses |
| Available Sites | Total number of RV plots/sites |
| Pending Bookings | Bookings waiting for admin confirmation |
| Occupancy Rate | Percentage of available capacity booked (last 30 days) |
| Avg Booking Value | Average revenue per confirmed booking |
| Avg Stay Length | Average number of nights per booking |

## Chart Legend

- **Booking Timeline**: Shows how many bookings were created each day
- **Revenue Timeline**: Shows daily revenue from confirmed bookings
- **Booking Status**: Shows breakdown of Pending/Confirmed/Completed/Cancelled
- **Site Status**: Shows how many sites are Available vs Booked

## Customization

To add more analytics or change calculations:
1. Edit `campland/admin.py` - modify the `index()` method
2. Add new metrics in the context dictionary
3. Update `templates/admin/index.html` to display new data

## Performance Notes

- Dashboard loads instantly (all calculations server-side)
- Charts render client-side using Chart.js
- Suitable for hundreds of bookings
- Data updates on each page load (real-time)

## Tips

- Dashboard data is **read-only** from this view (editing is in the standard admin panels below)
- All metrics are calculated from actual database records
- No data is cached - metrics are always current
- Admin-only access (requires login and staff permissions)

---

**Questions?** Check `ADMIN_DASHBOARD_INTEGRATED.md` for technical details.
