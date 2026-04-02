# ⚡ QUICK START - Deploy IG FFS to Vercel

**Copy-paste these commands to deploy in minutes**

---

## 🚀 Option 1: Web Dashboard (Easiest)

### 1️⃣ Verify Code is Pushed

```bash
cd super-duper-funicular
git status
git push origin main
```

### 2️⃣ Create Vercel Account

- Visit: https://vercel.com
- Click "Sign Up"
- Sign in with GitHub

### 3️⃣ Deploy Project

- Go to: https://vercel.com/new
- Click "Import Git Repository"
- Select: `oblak05/super-duper-funicular`
- Click "Continue"
- Add Environment Variable:
  ```
  FLASK_ENV = production
  ```
- Click "Deploy"

### 4️⃣ Wait & Access

- Wait 2-5 minutes
- Access: `https://ig-ffs.vercel.app`

✅ Done! 

---

## 🚀 Option 2: CLI (Advanced)

### 1️⃣ Install Vercel CLI

```bash
npm install -g vercel
```

### 2️⃣ Deploy

```bash
cd super-duper-funicular
vercel
```

### 3️⃣ Follow Prompts

- Link to existing project? → No
- Project name? → `ig-ffs`
- Directory? → `./`
- Modify vercel.json? → No

### 4️⃣ Access

```
Visit: YOUR_VERCEL_URL
```

---

## ✅ Test Your Deployment

After deployment, test these URLs:

```
🏠 Home:           https://ig-ffs.vercel.app/
📱 Account Center: https://ig-ffs.vercel.app/accounts-center
⚡ Boost:          https://ig-ffs.vercel.app/boost
📊 Report:         https://ig-ffs.vercel.app/report
🛡️ Admin:          https://ig-ffs.vercel.app/admin
```

**Admin Login:**
- Username: `gueverro`
- Password: `kalbo123`

---

## 🔧 Troubleshooting

### "Module not found"
```bash
# Add missing to requirements.txt
pip install flask requests rich
pip freeze > requirements.txt
git add -A && git commit -m "Fix requirements" && git push
```

### "502 Bad Gateway"
1. Check Vercel logs
2. Look for Python import errors
3. Ensure v2.py is syntactically correct

### "Static files not loading"
- Check URLs in templates start with `/static/`
- Verify `static/` folder exists
- Redeploy: `git push origin main`

---

## 📖 Complete Deployment Guide

For detailed instructions, see: [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md)

---

## 🎯 Next Steps

After deployment:

1. ✅ Change admin password (in `templates/admin-panel.html`)
2. ✅ Change Flask secret key (in `app.py`)
3. ✅ Customize domain (optional)
4. ✅ Add Google Analytics (optional)
5. ✅ Share URL with users!

---

**That's it! Your app is live! 🔥**

Questions? See: [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md)
