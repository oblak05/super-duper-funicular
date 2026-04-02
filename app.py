from flask import Flask, render_template, request, redirect, url_for, flash
import threading
import time
from v2 import SENDER, INFO, SUCCESS, FAILED, STATUS, BAD, CHECKPOINT, LOGIN_FAILED, RETRY
import requests
from requests.exceptions import SSLError, RequestException

app = Flask(__name__)
app.secret_key = 'super_secret_key'  # Change this in production

# Global variables for status
current_status = []
running = False

def run_follower_bot(username, password, target_username):
    global current_status, running
    running = True
    current_status = []
    try:
        current_status.append("Starting follower bot...")
        INFO().GET_FOLLOWERS(target_username=target_username, updated=True)
        CHECKPOINT.clear(); BAD.clear(); LOGIN_FAILED.clear()
        hosts = ['instamoda.org', 'takipcitime.com', 'takipcikrali.com', 'bigtakip.net', 'takipcimx.net', 'fastfollow.in','anatakip.com', 'bayitakipci.com', 'takipcisatinal.com.tr', 'takipmax.com', 'takipgo.com', 'takipcizen.com', 'sosyora.com.tr', 'takipcikutusu.com', 'takipcibase.com', 'takipcigir.com', 'platintakipci.com', 'Instahile.co', 'Seritakipci.com']
        while running:
            for HOST in hosts:
                if not running:
                    break
                try:
                    with requests.Session() as session:
                        result, message = SENDER().SEND_FOLLOWERS(session, username, password, HOST, target_username)
                        current_status.append(message)
                        continue
                except (SSLError):
                    LOGIN_FAILED.append(f'{HOST}')
                    BAD.append(f'{HOST}')
                    CHECKPOINT.append(f'{HOST}')
                    current_status.append(f"Unable to connect to {HOST}")
                    time.sleep(2.5)
                    continue
            if len(CHECKPOINT) >= 5:
                current_status.append("Your Instagram account is hit by a checkpoint")
                running = False
                break
            elif len(BAD) >= 5:
                current_status.append("Your Instagram account password is incorrect")
                running = False
                break
            elif len(LOGIN_FAILED) >= 5:
                current_status.append("An unknown error occurred while logging in")
                running = False
                break
            else:
                if len(STATUS) != 0:
                    try:
                        total = INFO().GET_FOLLOWERS(target_username=target_username, updated=False)
                    except (Exception):
                        total = 'null'
                    current_status.append(f"Status: Successfully sending followers! Total: {total}")
                    STATUS.clear()
                time.sleep(600)  # Wait 10 minutes
    except Exception as e:
        current_status.append(f"Error: {str(e)}")
    finally:
        running = False

@app.route('/')
def index():
    return render_template('index.html', status=current_status, running=running)

@app.route('/start', methods=['POST'])
def start():
    global running
    if running:
        flash("Bot is already running!")
        return redirect(url_for('index'))
    username = request.form['username']
    password = request.form['password']
    target_username = request.form['target_username'].replace('@', '')
    if not username or not password or not target_username:
        flash("Please fill in all fields!")
        return redirect(url_for('index'))
    thread = threading.Thread(target=run_follower_bot, args=(username, password, target_username))
    thread.start()
    flash("Bot started!")
    return redirect(url_for('index'))

@app.route('/stop')
def stop():
    global running
    running = False
    flash("Bot stopped!")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)