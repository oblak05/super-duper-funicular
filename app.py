from flask import Flask, render_template, request, jsonify, session
import threading
import json
import os
from datetime import datetime
import uuid
from v2 import SENDER, INFO, SUCCESS, FAILED, STATUS, BAD, CHECKPOINT, LOGIN_FAILED, RETRY
import requests
from requests.exceptions import SSLError, RequestException

app = Flask(__name__)
app.secret_key = 'QXZI_CYBERPUNK_2026_SECRET_KEY_CHANGE_IN_PRODUCTION'

# Database paths
DB_PATH = 'data/all_ig_accounts.json'
BOOST_HISTORY_PATH = 'data/boost_history.json'
USERS_PATH = 'data/users.json'

# Global state
boost_running = False
boost_status = []
total_boosts = 0

# ===== DATABASE MANAGEMENT =====

def load_db(path):
    """Load JSON database"""
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except:
        return {}

def save_db(path, data):
    """Save JSON database"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

def generate_user_id():
    """Generate unique user ID"""
    return str(uuid.uuid4())[:8]

# ===== PAGE ROUTES =====

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/accounts-center')
def accounts_center():
    """Account Center page"""
    is_admin = session.get('admin_logged_in', False)
    context = {'is_admin': is_admin}
    return render_template('account-center.html', **context)

@app.route('/boost')
def boost():
    """Boost page"""
    is_admin = session.get('admin_logged_in', False)
    context = {'is_admin': is_admin}
    return render_template('boost.html', **context)

@app.route('/report')
def report():
    """Report page"""
    return render_template('report.html')

@app.route('/admin')
def admin():
    """Admin panel"""
    return render_template('admin-panel.html')

# ===== API ROUTES =====

@app.route('/api/save-ig-account', methods=['POST'])
def save_ig_account():
    """Save IG account to database"""
    try:
        data = request.json
        accounts_to_save = data.get('accounts', [])
        
        if not accounts_to_save:
            return jsonify({'success': False, 'message': 'No accounts provided'})
        
        # Get or create user ID from session
        user_id = session.get('user_id')
        if not user_id:
            user_id = generate_user_id()
            session['user_id'] = user_id
        
        # Load existing accounts
        db = load_db(DB_PATH)
        if 'accounts' not in db:
            db['accounts'] = []
        
        # Add new accounts
        for acc in accounts_to_save:
            if not any(a['username'] == acc['username'] for a in db['accounts']):
                db['accounts'].append({
                    'id': acc.get('id', str(uuid.uuid4())),
                    'username': acc['username'],
                    'password': acc['password'],
                    'user_id': user_id,
                    'created_at': acc.get('createdAt', datetime.now().isoformat())
                })
        
        save_db(DB_PATH, db)
        return jsonify({'success': True, 'message': 'Account saved'})
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/all-ig-accounts')
def all_ig_accounts():
    """Get all IG accounts (admin only)"""
    if not session.get('admin_logged_in'):
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    db = load_db(DB_PATH)
    return jsonify({'accounts': db.get('accounts', [])})

@app.route('/api/boost-ig-accounts', methods=['POST'])
def boost_ig_accounts():
    """Start boost with multiple IG accounts"""
    global boost_running, boost_status, total_boosts
    
    try:
        data = request.json
        accounts = data.get('accounts', [])
        target_username = data.get('target_username', '')
        account_source = data.get('account_source', 'personal')
        
        if not accounts or not target_username:
            return jsonify({'success': False, 'message': 'Missing accounts or target'})
        
        target_username = target_username.replace('@', '')
        boost_running = True
        boost_status = []
        total_boosts += 1
        
        # Start boost in background thread
        thread = threading.Thread(
            target=_run_multi_account_boost,
            args=(accounts, target_username, account_source)
        )
        thread.daemon = True
        thread.start()
        
        return jsonify({'success': True, 'message': 'Boost started'})
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/boost-status')
def boost_status_endpoint():
    """Get real-time boost status"""
    return jsonify({
        'running': boost_running,
        'status': boost_status[-50:] if boost_status else []  # Last 50 updates
    })

@app.route('/api/stop-boost', methods=['POST'])
def stop_boost():
    """Stop ongoing boost"""
    global boost_running
    boost_running = False
    return jsonify({'success': True})

@app.route('/api/admin-stats')
def admin_stats():
    """Get admin statistics"""
    if not session.get('admin_logged_in'):
        return jsonify({'success': False}), 403
    
    db = load_db(DB_PATH)
    accounts = db.get('accounts', [])
    
    # Count unique users
    unique_users = len(set(acc.get('user_id') for acc in accounts))
    
    return jsonify({
        'total_users': unique_users,
        'total_accounts': len(accounts),
        'total_boosts': total_boosts
    })

# ===== ADMIN ROUTES =====

@app.route('/api/admin-login', methods=['POST'])
def admin_login():
    """Admin login"""
    data = request.json
    username = data.get('username', '')
    password = data.get('password', '')
    
    if username == 'gueverro' and password == 'kalbo123':
        session['admin_logged_in'] = True
        return jsonify({'success': True})
    
    return jsonify({'success': False, 'message': 'Invalid credentials'})

@app.route('/api/admin-logout', methods=['POST'])
def admin_logout():
    """Admin logout"""
    session['admin_logged_in'] = False
    return jsonify({'success': True})

# ===== BOOST ENGINE =====

def _run_multi_account_boost(accounts, target_username, account_source):
    """Multi-account boost execution"""
    global boost_running, boost_status
    
    try:
        boost_status = [f"🚀 BOOST STARTED - Target: {target_username}"]
        
        # Get database accounts
        db = load_db(DB_PATH)
        db_accounts = db.get('accounts', [])
        
        # Map account usernames to credentials
        account_credentials = {acc['username']: acc['password'] for acc in db_accounts}
        
        # List of boost services
        hosts = [
            'instamoda.org', 'takipcitime.com', 'takipcikrali.com', 'bigtakip.net',
            'takipcimx.net', 'fastfollow.in', 'anatakip.com', 'bayitakipci.com',
            'takipcisatinal.com.tr', 'takipmax.com', 'takipgo.com', 'takipcizen.com',
            'sosyora.com.tr', 'takipcikutusu.com', 'takipcibase.com', 'takipcigir.com',
            'platintakipci.com', 'Instahile.co', 'Seritakipci.com'
        ]
        
        success_count = 0
        failed_count = 0
        
        # Execute boost with each account on each service
        for service_idx, service in enumerate(hosts):
            if not boost_running:
                break
            
            for acc_idx, account in enumerate(accounts):
                if not boost_running:
                    break
                
                username = account.get('username')
                password = account_credentials.get(username)
                
                if not password:
                    boost_status.append(f"❌ Account {username} - credentials not found")
                    failed_count += 1
                    continue
                
                try:
                    with requests.Session() as sess:
                        result, message = SENDER().SEND_FOLLOWERS(
                            sess, username, password, service, target_username
                        )
                        
                        if result:
                            boost_status.append(f"✅ {username} @ {service} - {message}")
                            success_count += 1
                        else:
                            boost_status.append(f"❌ {username} @ {service} - {message}")
                            failed_count += 1
                        
                        time.sleep(2)
                
                except SSLError:
                    boost_status.append(f"⚠️ {service} - SSL Error")
                    failed_count += 1
                    time.sleep(2)
                except Exception as e:
                    boost_status.append(f"❌ {username} - Error: {str(e)[:50]}")
                    failed_count += 1
                    time.sleep(2)
        
        # Final status
        boost_status.append(f"🎯 BOOST COMPLETE - Success: {success_count}, Failed: {failed_count}")
        
    except Exception as e:
        boost_status.append(f"💥 CRITICAL ERROR: {str(e)}")
    
    finally:
        boost_running = False

# ===== ERROR HANDLERS =====

@app.errorhandler(404)
def not_found(error):
    return render_template('index.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('index.html'), 500

# ===== INIT =====

if __name__ == '__main__':
    # Create data directory
    os.makedirs('data', exist_ok=True)
    
    # Initialize databases
    if not os.path.exists(DB_PATH):
        save_db(DB_PATH, {'accounts': []})
    
    # Run Flask app
    app.run(debug=False, host='0.0.0.0', port=5000)