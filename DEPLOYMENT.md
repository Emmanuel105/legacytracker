# Render Deployment Guide for Legacy Academy Tracking System

## Prerequisites

Before deploying, ensure you have:
1. A GitHub repository with the code
2. A Render account (free tier is fine)
3. The main branch pushed to GitHub

## Step 1: Create PostgreSQL Database on Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"PostgreSQL"**
3. Configure the database:
   - **Name**: `legacy-academy-db`
   - **Database**: `legacy_academy_db`
   - **User**: `legacy_user`
   - **Region**: Choose closest to you
   - **Plan**: Free
4. Click **"Create Database"**
5. Wait for database to be created (takes 1-2 minutes)
6. Copy the **Internal Database URL** for later use

## Step 2: Deploy Web Service

### Option A: Using render.yaml (Recommended)

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Blueprint"**
3. Connect your GitHub repository
4. Select the `main` branch
5. Render will detect the `render.yaml` file
6. Click **"Apply"**

### Option B: Manual Setup

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure:
   - **Name**: `legacy-academy-tracking`
   - **Branch**: `main`
   - **Runtime**: Python 3
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn attendance_system.wsgi:application --bind 0.0.0.0:$PORT`

## Step 3: Set Environment Variables

In your web service settings, add these environment variables:

| Key | Value | Description |
|-----|-------|-------------|
| `DATABASE_URL` | (Internal Database URL from Step 1) | Database connection |
| `SECRET_KEY` | (Generate a secure key) | Django secret key |
| `DEBUG` | `False` | Production setting |
| `ALLOWED_HOSTS` | `.onrender.com` | Allowed domains |
| `PYTHON_VERSION` | `3.11.0` | Python version |

## Step 4: Connect Database to Web Service

1. In your web service, go to **"Environment"** tab
2. For `DATABASE_URL`:
   - Click **"Add Environment Variable"**
   - Key: `DATABASE_URL`
   - Click **"Add from database"**
   - Select your PostgreSQL database
   - Save

## Step 5: Deploy

1. Click **"Manual Deploy"** → **"Deploy latest commit"**
2. Monitor the deployment logs
3. Wait for "Build successful" and "Live" status

## Step 6: Verify Deployment

Once deployed, test these URLs:
- Root: `https://legacy-academy-tracking.onrender.com/`
- Login: `https://legacy-academy-tracking.onrender.com/login/`
- Admin: `https://legacy-academy-tracking.onrender.com/secure-admin-panel/`

### Default Credentials
- **Superuser**: `admin` / `admin123`
- **School Admin**: `admin_bauleni` / `testpass123`

## Troubleshooting

### 1. Site shows "Not Found"
- Check that the web service is "Live"
- Verify the URL is correct
- Check deployment logs for errors

### 2. 500 Server Error
- Check that `DATABASE_URL` is set correctly
- Verify database is created and running
- Check logs in Render dashboard

### 3. Database Connection Failed
- Ensure PostgreSQL database is created
- Verify `DATABASE_URL` environment variable
- Check that database is in same region as web service

### 4. Static Files Not Loading
- Run deployment again to trigger `collectstatic`
- Check that WhiteNoise is configured correctly

### 5. Migrations Failed
- Check database connection
- Look for migration errors in build logs
- May need to manually run migrations

## Important Notes

1. **Free Tier Limitations**:
   - Database: 90 days of activity
   - Web Service: Spins down after 15 minutes of inactivity
   - First request after spin-down takes ~30 seconds

2. **Security**:
   - Change default passwords immediately after deployment
   - Use strong `SECRET_KEY` in production
   - Enable HTTPS (automatic on Render)

3. **Monitoring**:
   - Check logs regularly in Render dashboard
   - Set up alerts for service health
   - Monitor database usage

## Post-Deployment Steps

1. **Change default passwords**:
   ```
   - Login as admin
   - Go to admin panel
   - Change all default user passwords
   ```

2. **Configure school settings**:
   ```
   - Login as school admin
   - Configure school profile
   - Set up zones
   - Add users
   ```

3. **Test core functionality**:
   ```
   - Student enrollment
   - Attendance marking
   - Report generation
   ```

## Support

If deployment fails:
1. Check build logs in Render dashboard
2. Verify all environment variables are set
3. Ensure database is created and connected
4. Check GitHub repository is up to date