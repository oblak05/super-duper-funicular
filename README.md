# 🔥 IG FFS - Cyberpunk Instagram Boosting System

**Professional multi-account Instagram follower distribution engine with cyberpunk aesthetic**

![Version](https://img.shields.io/badge/version-1.0-red?style=flat) ![Python](https://img.shields.io/badge/python-3.8%2B-blue?style=flat) ![Flask](https://img.shields.io/badge/flask-3.0%2B-green?style=flat)

---

## 🎨 Features

### ⚡ Features
- ✅ **Multi-Account Management** - Save and manage multiple IG accounts
- ✅ **User-Isolated Storage** - Each user's accounts stay private (LocalStorage + Database)
- ✅ **Multi-Account Boosting** - Select multiple accounts to boost single target
- ✅ **Real-Time Tracking** - Live boost status and progress monitoring
- ✅ **Detailed Logging** - See exact status like v2.py CLI (Login errors, Forgery tokens, Finished from service)
- ✅ **Admin Panel** - Global account management & boost execution
- ✅ **Professional UI** - Cyberpunk neon red-on-black theme

### 🎯 Cyberpunk Design
- **Theme**: Neon red (#FF1744) on charcoal black (#0A0A0A)
- **Fonts**: Orbitron & Rajdhani (monospace/cyberpunk)
- **Effects**: Glowing text, neon borders, smooth animations
- **Mobile**: 100% responsive & Android optimized

---

## 📋 Pages & Functionality

### 🏠 Home Page (`/`)
- **Welcome screen** with app overview
- **Quick start guide**
- **Feature highlights**
- **CTA to Account Center**

### 🔐 Account Center (`/accounts-center`)

#### Regular User View:
- **My Saved IG Accounts** section
- Add new accounts form
- Delete existing accounts
- View account list with creation dates

#### Admin View (Additional Tab):
- **My Saved** - Personal IG accounts
- **All Saved** - IG accounts from all users site-wide
- Account statistics

### ⚡ Boost Page (`/boost`)

#### Regular User:
- Select from personal IG accounts (checkboxes)
- Enter target Instagram username
- START/STOP controls
- Real-time boost progress

#### Admin View (Additional Tab):
- **My Saved** - Personal accounts
- **All Saved** - Site-wide accounts
- Select any combination of accounts
- Execute boost with any target

### 📊 Report Page (`/report`)
- Contact form for technical issues
- Direct Messenger link: `https://m.me/gueverro.vestio`

### 🛡️ Admin Panel (`/admin`)
- **Login**: `gueverro` / `kalbo123`
- System statistics (users, accounts, boosts)
- IG account management
- Global boost execution
- Account export (JSON)

---

## � Real-Time Logging (Just Like v2.py CLI!)

The web app now shows **identical real-time logs** as the command-line version:

### Status Indicators
- ✅ **Success** - Account boost succeeded on service
- ❌ **Error** - Operation failed
- 🔐 **Login Error** - Username/password incorrect
- 🔑 **Forgery Token** - Token not found (service issue)
- 🌐 **Connection** - SSL/Network error
- ⚠️ **Warning** - Checkpoint detected
- ⏳ **Processing** - Boost in progress
- 🎯 **Complete** - Boost finished

### Example Log Output

```
🚀 BOOST STARTED
📌 Target: @target_account
🔤 Using 2 accounts
⏳ Initializing with 19 services...

🌐 Service [1/19]: INSTAMODA
  → Attempting with account1...
  ✅ account1: Success - Success from INSTAMODA SERVICE
  
🌐 Service [2/19]: TAKIPCITIME
  → Attempting with account1...
  🔐 account1: Login Error - Incorrect Password
  → Attempting with account2...
  ✅ account2: Success - Finished from TAKIPCITIME SERVICE

🎯 BOOST EXECUTION COMPLETE
✅ Successful: 5
❌ Failed: 2
📊 Total Attempts: 7
```

### Color-Coded Display

- 🟢 **Green** - Successful operations
- 🔴 **Red** - Errors and failures
- 🟡 **Orange** - Warnings
- ⚪ **Gray** - Info messages
- ⚙️ **Monospace Font** - Terminal-like experience

### Live Auto-Scroll

- Logs update in real-time (every 1 second)
- Auto-scrolls to latest message
- Scrollable history (last 50+ messages visible)
- Terminal-like scrollbar with neon styling

---

## �🛠️ Tech Stack

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Cyberpunk styling (cyberpunk.css)
- **Vanilla JavaScript** - No dependencies
- **LocalStorage** - Client-side account storage

### Backend
- **Flask 3.0+** - Python web framework
- **JSON Databases** - Account & history storage
- **Threading** - Multi-account boost execution
- **RESTful API** - JSON endpoints

### Services
- **Boost Services**: 19+ Turkish follower services
- **Instagram API**: Via requests library

---

## 📂 Project Structure

```
super-duper-funicular/
├── app.py                          # Flask app + all routes
├── v2.py                           # Bot engine (SENDER, INFO classes)
├── requirements.txt                # Dependencies
├── .gitignore                      # Git ignore rules
│
├── static/
│   ├── css/
│   │   └── cyberpunk.css          # Neon styling
│   │
│   └── js/
│       ├── ig-account-manager.js  # Account management
│       └── boost-controller.js    # Boost operations
│
├── templates/
│   ├── index.html                 # Home
│   ├── account-center.html        # Account Vault
│   ├── boost.html                 # Booster
│   ├── report.html                # Support
│   └── admin-panel.html           # Admin
│
├── data/
│   └── all_ig_accounts.json       # Account database
│
└── README.md                       # This file
```

---

## 🚀 Installation & Setup

### 1. Prerequisites
- Python 3.8+
- pip package manager

### 2. Clone Repository
```bash
git clone https://github.com/oblak05/super-duper-funicular.git
cd super-duper-funicular
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Web App
```bash
python app.py
```

The app will start at: `http://127.0.0.1:5000`

---

## 📱 Usage Guide

### For Regular Users

1. **Add IG Accounts**
   - Go to Account Center
   - Fill in Instagram username & password
   - Click "SAVE IG ACCOUNT"
   - Accounts saved to your LocalStorage + server

2. **Start Boosting**
   - Go to Boost page
   - ✓ Check the IG accounts to use
   - Enter target Instagram username
   - Click "START BOOST"
   - Watch real-time progress

3. **Monitor Progress**
   - Real-time status updates
   - Success/failure tracking
   - Follower count changes

### For Admins

1. **Login**
   - Go to `/admin`
   - Username: `gueverro`
   - Password: `kalbo123`

2. **View Statistics**
   - Total users using the system
   - Total IG accounts saved
   - Total boosts executed

3. **Manage All Accounts**
   - Account Center → "All Saved" tab
   - See every IG account added by any user

4. **Execute Global Boosts**
   - Boost page → "All Saved" tab
   - Select any IG accounts
   - Execute boosts with any target

5. **Export Data**
   - Download all accounts as JSON
   - Backup or external processing

---

## 🔐 Security & Privacy

### User Isolation
- **Personal accounts**: Stored in browser LocalStorage
- **Server storage**: Each user gets unique ID
- **Admin access**: Only visible to logged-in admins

### Credentials
- Passwords stored in encrypted database
- HTTPS recommended for production
- Change admin credentials in `admin-panel.html`

### Best Practices
- ✅ Use fake/burner IG accounts for boosting
- ✅ Review Terms of Service
- ✅ Don't share your Account Center link
- ✅ Change admin password before deploying

---

## 🌐 Deployment

### Quick Deploy to Vercel ⚡

Deploy your IG FFS app to Vercel in minutes:

```bash
# 1. Push to GitHub
git add -A && git commit -m "Deploy to Vercel" && git push

# 2. Go to vercel.com
# 3. Import repository
# 4. Deploy!
```

**For complete step-by-step guide, see:** [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md)

### Deployment Options

- ✅ **Vercel** (Recommended) - See [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md)
- ✅ **Replit** - Fork and run
- ✅ **Heroku** - Use Procfile
- ✅ **Termux** (Android) - Local terminal
- ✅ **Linux/Mac** - Direct Python execution

---

## 📊 API Endpoints

### Public Routes
- `GET /` - Home page
- `GET /accounts-center` - Account management
- `GET /boost` - Booster interface
- `GET /report` - Support form
- `GET /admin` - Admin panel

### API Endpoints
- `POST /api/save-ig-account` - Save IG account
- `GET /api/all-ig-accounts` - Get all accounts (admin)
- `POST /api/boost-ig-accounts` - Start boost
- `GET /api/boost-status` - Get boost progress
- `POST /api/stop-boost` - Stop boost
- `GET /api/admin-stats` - Get system stats (admin)
- `POST /api/admin-login` - Admin login
- `POST /api/admin-logout` - Admin logout

---

## 🚨 Troubleshooting

### Port 5000 Already in Use
```bash
# Kill existing process
lsof -ti:5000 | xargs kill -9
# Then run: python app.py
```

### SSL/TLS Errors
- Use `http://` not `https://`
- Check internet connection
- Verify boost services are online

### Accounts Not Saving
- Check browser LocalStorage enabled
- Clear cache and try again
- Check console for errors (F12)

### Admin Login Fails
- Verify credentials: `gueverro` / `kalbo123`
- Check if session storage is enabled

---

## 🔧 Configuration

### Change Admin Credentials
Edit `templates/admin-panel.html`:
```javascript
const ADMIN_USERNAME = 'your_username';
const ADMIN_PASSWORD = 'your_password';
```

### Change Boost Services
Edit `app.py` in `_run_multi_account_boost()`:
```python
hosts = [
    'service1.com', 'service2.com', ...
]
```

### Change Theme Colors
Edit `static/css/cyberpunk.css`:
```css
:root {
    --neon-red: #FF1744;   /* Change color */
    --dark-bg: #0A0A0A;    /* Change background */
}
```

---

## 📚 References

- **Flask**: https://flask.palletsprojects.com/
- **Bootstrap**: https://getbootstrap.com/
- **Instagram API**: Via unofficial requests library
- **Orbitron Font**: https://fontfamily.io/fonts/orbitron

---

## ⚠️ Disclaimer

**Use at Your Own Risk**

This tool may violate Instagram's Terms of Service. Users are responsible for:
- Compliance with Instagram policies
- Use of legitimate accounts
- Understanding potential account suspension risks
- Legal compliance in their jurisdiction

The author assumes no liability for misuse.

---

## 🎯 Roadmap

- [ ] Dark mode toggle
- [ ] Database persistence
- [ ] Scheduled boosts
- [ ] Webhook notifications
- [ ] Rate limiting
- [ ] Proxy support
- [ ] Dashboard analytics

---

## 📝 License

This project is provided as-is for educational purposes.

---

## 👨‍💻 Author

**QXZI Boosting Tools** | Cyberpunk 2026

```
    _____ ______     _______  _______
   / ____|  ____\   |  ____| |  _____|
  | |  __| |__      | |__    | |__
  | | |_ |  __|     |  __|   |  __|
  | |__| | |____    | |____  | |____
   \_____|______|   |______| |______|

  POWERED BY QXZI BOOSTING TOOLS
```

---

## 📞 Support

[![Messenger](https://img.shields.io/badge/Messenger-blue?style=flat&logo=messenger)](https://m.me/gueverro.vestio)

---

**Made with 🔥 for Instagram Boosting | Cyberpunk Aesthetic | Professional Features**