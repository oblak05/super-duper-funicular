# 🚀 Vercel Deployment Guide - IG FFS Cyberpunk

**Complete step-by-step guide to deploy IG FFS on Vercel**

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [GitHub Repository Setup](#github-repository-setup)
3. [Vercel Account Creation](#vercel-account-creation)
4. [Deploy to Vercel](#deploy-to-vercel)
5. [Verification & Testing](#verification--testing)
6. [Troubleshooting](#troubleshooting)
7. [Advanced Configuration](#advanced-configuration)

---

## ✅ Prerequisites

Before deploying to Vercel, make sure you have:

- ✅ GitHub account (for code hosting)
- ✅ Vercel account (free at vercel.com)
- ✅ Git installed locally
- ✅ Code pushed to GitHub repository
- ✅ Python 3.8+ support
- ✅ All dependencies in `requirements.txt`

---

## 🌐 GitHub Repository Setup

### Step 1: Ensure Code is Pushed to GitHub

```bash
# Navigate to your project
cd super-duper-funicular

# Check git status
git status

# Add all changes
git add -A

# Commit changes
git commit -m "Prepare for Vercel deployment"

# Push to GitHub
git push origin main
```

### Step 2: Verify GitHub Repository

1. Go to https://github.com
2. Navigate to your repository: `https://github.com/oblak05/super-duper-funicular`
3. Ensure all files are present:
   - `app.py`
   - `v2.py`
   - `requirements.txt`
   - `templates/` folder
   - `static/` folder
   - `data/` folder

---

## 🔐 Vercel Account Creation

### Step 1: Create Vercel Account

1. Go to https://vercel.com
2. Click **"Sign Up"**
3. Choose **"Continue with GitHub"**
4. Authorize Vercel to access GitHub
5. Complete registration

### Step 2: Install Vercel CLI (Optional)

```bash
# Install Vercel CLI globally
npm install -g vercel

# Or using Yarn
yarn global add vercel
```

---

## 🚀 Deploy to Vercel

### Method 1: Deploy via Web Dashboard (Easiest)

#### Step 1: Go to Vercel Dashboard

1. Login to https://vercel.com/dashboard
2. Click **"New Project"**

#### Step 2: Import GitHub Repository

1. Select **"Import Git Repository"**
2. Paste your repo URL: `https://github.com/oblak05/super-duper-funicular`
3. Click **"Continue"**

#### Step 3: Configure Project

**Project Settings:**
- **Project Name**: `ig-ffs` (or your preferred name)
- **Framework**: Select **"Other"** (Python)
- **Root Directory**: Leave blank or set to current directory

**Environment Variables:**
- Click **"Environment Variables"**
- Add the following:

```
FLASK_ENV=production
FLASK_APP=app.py
SECRET_KEY=QXZI_CYBERPUNK_2026_SECRET_KEY_CHANGE_IN_PRODUCTION
```

#### Step 4: Create Vercel Config File

Create a file named `vercel.json` in your project root:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ],
  "env": {
    "FLASK_ENV": "production",
    "PYTHONUNBUFFERED": "1"
  }
}
```

#### Step 5: Deploy

1. Click **"Deploy"**
2. Wait 2-5 minutes for build to complete
3. You'll get a unique URL: `https://ig-ffs.vercel.app`

### Method 2: Deploy via Vercel CLI

```bash
# Login to Vercel
vercel login

# Navigate to project directory
cd super-duper-funicular

# Deploy
vercel

# Follow prompts:
# - Link to existing project? No
# - What's your project's name? ig-ffs
# - In which directory is your code? ./
# - Want to modify vercel.json? No
```

---

## ✅ Verification & Testing

### Step 1: Visit Deployed URL

After deployment, visit your app:

```
https://ig-ffs.vercel.app
```

### Step 2: Test All Pages

✅ **Home Page**: `https://ig-ffs.vercel.app/`  
✅ **Account Center**: `https://ig-ffs.vercel.app/accounts-center`  
✅ **Boost Page**: `https://ig-ffs.vercel.app/boost`  
✅ **Report Page**: `https://ig-ffs.vercel.app/report`  
✅ **Admin Panel**: `https://ig-ffs.vercel.app/admin`  

### Step 3: Test Admin Login

1. Go to Admin Panel
2. **Username**: `gueverro`
3. **Password**: `kalbo123`
4. Verify dashboard loads

### Step 4: Test Account Management

1. Go to Account Center
2. Add test account:
   - Username: `test_account`
   - Password: `test_password`
3. Verify account is saved locally

---

## 🔧 Troubleshooting

### Issue 1: "Module not found" Error

**Problem**: Flask or dependencies missing

**Solution**:
```bash
# Check requirements.txt includes all packages
pip install -r requirements.txt

# If missing, add them:
pip install flask requests rich

# Update requirements
pip freeze > requirements.txt

# Commit and push
git add -A
git commit -m "Fix requirements.txt"
git push

# Redeploy
vercel --prod
```

### Issue 2: 502 Bad Gateway

**Problem**: Python runtime error

**Solution**:
1. Check Vercel logs: Dashboard → Project → Deployments → View Logs
2. Look for Python import errors
3. Ensure `v2.py` is syntactically correct:
   ```bash
   python -m py_compile v2.py
   ```
4. Fix errors and redeploy

### Issue 3: Static Files Not Loading

**Problem**: CSS/JS not working

**Solution**:
1. Ensure `static/` folder exists
2. Check file paths in templates:
   ```python
   <link rel="stylesheet" href="/static/css/cyberpunk.css">
   <script src="/static/js/ig-account-manager.js"></script>
   ```
3. Redeploy:
   ```bash
   git add -A
   git commit -m "Fix static files"
   git push
   ```

### Issue 4: Database Errors (all_ig_accounts.json)

**Problem**: Cannot write to `data/` folder

**Solution**:
Since Vercel uses ephemeral storage:
- Accounts saved in session will be lost after redeploy
- For persistent storage, upgrade to Vercel Enterprise or use external database
- For now, use **LocalStorage** in browser for temporary storage

### Issue 5: Admin Password Not Working

**Problem**: Admin login fails

**Solution**:
1. Verify credentials in `templates/admin-panel.html`:
   ```javascript
   const ADMIN_USERNAME = 'gueverro';
   const ADMIN_PASSWORD = 'kalbo123';
   ```
2. Check browser console (F12) for errors
3. Clear browser cache and try again

---

## 📊 Advanced Configuration

### Custom Domain

1. Go to Vercel Dashboard
2. Select your project
3. Go to **Settings** → **Domains**
4. Add your domain: `ig-ffs.yourdomain.com`
5. Follow DNS configuration steps

### Environment-Specific Settings

Create `.env.local` for local development:

```env
FLASK_ENV=development
FLASK_DEBUG=True
```

Create `.env.production` for production:

```env
FLASK_ENV=production
FLASK_DEBUG=False
```

### Auto-Redeploy on Push

**Enabled by default!**

Each push to `main` branch automatically redeploys:

```bash
git push origin main
# Vercel automatically builds and deploys
```

Disable auto-deploy:
1. Vercel Dashboard → Project → Git
2. Disable "Auto-deploy on push"

### Monitoring & Logs

View deployment logs:

1. **Vercel Dashboard** → Project → **Deployments**
2. Click on latest deployment
3. View **Build Logs** and **Runtime Logs**

---

## 📝 Production Checklist

Before going live, ensure:

- ✅ Change Flask secret key in `app.py`:
  ```python
  app.secret_key = 'YOUR_SECURE_RANDOM_KEY_HERE'
  ```

- ✅ Change admin password in `templates/admin-panel.html`:
  ```javascript
  const ADMIN_USERNAME = 'your_username';
  const ADMIN_PASSWORD = 'your_secure_password';
  ```

- ✅ Set `FLASK_ENV=production` in Vercel environment variables

- ✅ Test all features work on deployed version

- ✅ Set custom domain (if using)

- ✅ Enable HTTPS (automatic with Vercel)

- ✅ Add Google Analytics (optional)

---

## 🎯 Final URLs

After successful deployment:

```
🏠 Home: https://ig-ffs.vercel.app/
📱 Mobile: Fully responsive, works on all devices
🌐 Custom Domain: https://ig-ffs.yourdomain.com (if configured)
📊 Vercel Dashboard: https://vercel.com/oblak05/ig-ffs
```

---

## 🆘 Support

If you encounter issues:

1. **View Logs**: Vercel Dashboard → Deployments → View Logs
2. **Check GitHub**: Ensure all files are pushed
3. **Verify requirements.txt**: All dependencies listed
4. **Test locally first**: `python app.py` should work locally
5. **Contact Support**: Vercel Dashboard → Support

---

## 📚 Additional Resources

- **Vercel Python Documentation**: https://vercel.com/docs/concepts/functions/serverless-functions/python
- **Flask on Vercel**: https://vercel.com/guides/deploying-a-python-flask-app-with-vercel
- **Vercel Docs**: https://vercel.com/docs
- **Python Buildpacks**: https://github.com/vercel/community/discussions

---

## 🔄 Continuous Updates

To update your deployed app:

1. Make changes locally
2. Test with `python app.py`
3. Commit changes:
   ```bash
   git add -A
   git commit -m "Update feature"
   git push origin main
   ```
4. **Vercel automatically redeploys** in 1-2 minutes

---

## 🎉 Congratulations!

Your IG FFS Cyberpunk app is now live on Vercel! 

Access it at: **https://ig-ffs.vercel.app**

Share the link with friends and watch the real-time logs in action! 🚀

---

**Made with 🔥 | Cyberpunk 2026 | Production Ready**