# Deployment Guide for CampLand

This guide explains how to deploy the CampLand camping booking system to Render.

## Prerequisites

- A GitHub repository with your code
- A Render account (free tier available)

## Deployment Steps

1. **Push your code to GitHub** (if not already done)
   
2. **Connect to Render**
   - Go to [render.com](https://render.com)
   - Sign in with your GitHub account
   - Click "New" and select "Blueprint"
   - Connect your GitHub repository
   - Render will automatically detect the `render.yaml` file

3. **Environment Variables**
   The following environment variables are automatically configured in `render.yaml`:
   - `SECRET_KEY` - Generated automatically by Render
   - `DEBUG` - Set to "false" for production
   - `ALLOWED_HOSTS` - Configured for Render domains
   - `DATABASE_URL` - Automatically provided by the PostgreSQL service
   - `PYTHON_VERSION` - Set to 3.11.0
   - `NODE_VERSION` - Set to 18

4. **Database**
   - A PostgreSQL database is automatically created and connected
   - Database migrations run automatically during deployment

5. **Static Files**
   - Tailwind CSS is built during deployment
   - Static files are collected and served via WhiteNoise

## Files Added/Modified for Deployment

- `render.yaml` - Render deployment configuration
- `requirements.txt` - Python dependencies including production packages
- `settings.py` - Updated with production-ready configuration
- `.env.example` - Environment variable documentation

## Services Created

1. **Web Service** (`campland-web`)
   - Python runtime
   - Free tier
   - Automatic SSL
   - Custom domain support

2. **Database Service** (`campland-db`)
   - PostgreSQL database
   - Free tier (1GB storage)
   - Automatic backups

## Post-Deployment

1. **Create Superuser**
   After deployment, you'll need to create an admin user. You can do this via the Render shell:
   ```bash
   python manage.py createsuperuser
   ```

2. **Populate Sample Data** (optional)
   ```bash
   python manage.py populate_sample_data
   ```

3. **Access Your Site**
   - Your site will be available at: `https://campland-web.onrender.com`
   - Admin interface: `https://campland-web.onrender.com/admin/`

## Troubleshooting

### Common Issues

1. **"ModuleNotFoundError: No module named 'app'"**
   - This means Render is using `gunicorn app:app` instead of our configured command
   - Solutions:
     - Ensure the `render.yaml` file is in the root directory
     - Check that the `startCommand` in render.yaml is: `gunicorn campland.wsgi:application`
     - Verify the Procfile contains: `web: gunicorn campland.wsgi:application`
     - Try manually setting the start command in Render dashboard under "Settings" → "Build & Deploy"

2. **Database Connection Issues**
   - Ensure the DATABASE_URL environment variable is set by the PostgreSQL service
   - Check that migrations completed successfully in the build logs

3. **Static Files Not Loading**
   - Verify that `npm run build:css` completed successfully
   - Check that `collectstatic` ran without errors
   - Ensure WhiteNoise is properly configured in settings.py

### Manual Override
If the YAML configuration is being ignored, you can manually override in the Render dashboard:
1. Go to your service settings
2. Under "Build & Deploy", set:
   - Build Command: `pip install -r requirements.txt && npm install && npm run build:css && python manage.py collectstatic --noinput && python manage.py migrate`
   - Start Command: `gunicorn campland.wsgi:application`

- Check the build logs in the Render dashboard
- Ensure all environment variables are properly set
- Verify that the database is connected and migrations completed
- Check static files are being served correctly

## Cost

Using the free tier:
- Web service: Free (with some limitations)
- PostgreSQL database: Free (1GB storage, sleeps after 90 days of inactivity)

For production use, consider upgrading to paid plans for better performance and reliability.