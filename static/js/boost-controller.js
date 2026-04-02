// Boost Controller - Handles boost operations and real-time tracking

class BoostController {
    constructor() {
        this.isRunning = false;
        this.boostStatus = [];
        this.pollInterval = null;
    }

    async startBoost(selectedAccounts, targetUsername, accountSource = 'personal') {
        if (!targetUsername || selectedAccounts.length === 0) {
            this.showMessage('error', 'Please select IG accounts and enter target username');
            return;
        }

        this.isRunning = true;
        this.boostStatus = [];
        this.updateUI();

        try {
            const response = await fetch('/api/boost-ig-accounts', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    accounts: selectedAccounts,
                    target_username: targetUsername,
                    account_source: accountSource
                })
            });

            const data = await response.json();
            
            if (data.success) {
                this.showMessage('success', '✅ Boost started successfully!');
                this.showStatusTracker();
                this.pollBoostStatus();
            } else {
                this.showMessage('error', data.message || 'Failed to start boost');
            }
        } catch (error) {
            this.showMessage('error', 'Error connecting to server: ' + error.message);
        }
    }

    async pollBoostStatus() {
        this.pollInterval = setInterval(async () => {
            try {
                const response = await fetch('/api/boost-status');
                const data = await response.json();
                
                if (data.status && data.status.length > 0) {
                    this.boostStatus = data.status;
                    this.renderStatus();
                }

                if (!data.running) {
                    clearInterval(this.pollInterval);
                    this.isRunning = false;
                    this.updateUI();
                }
            } catch (error) {
                console.error('Status poll error:', error);
            }
        }, 1000); // Update every 1 second for live feel
    }

    stopBoost() {
        fetch('/api/stop-boost', { method: 'POST' });
        this.isRunning = false;
        if (this.pollInterval) clearInterval(this.pollInterval);
        this.updateUI();
    }

    renderStatus() {
        const statusContainer = document.getElementById('statusItems');
        if (!statusContainer) return;

        const html = this.boostStatus.map((status, i) => {
            const timestamp = new Date().toLocaleTimeString();
            const icon = this.getStatusIcon(status);
            const className = this.getStatusClass(status);
            
            return `<div class="status-item ${className}">
                <div style="flex: 1;">
                    <span class="status-time">${timestamp}</span>
                    <span class="status-text">${icon} ${status}</span>
                </div>
            </div>`;
        }).reverse().join('');

        statusContainer.innerHTML = html;
        
        // Auto-scroll to bottom
        const tracker = document.getElementById('boostStatus');
        if (tracker) {
            tracker.scrollTop = tracker.scrollHeight;
        }
    }

    getStatusIcon(status) {
        if (status.includes('Success') || status.includes('BOOST STARTED') || status.includes('successfully')) return '✅';
        if (status.includes('Error') || status.includes('ERROR') || status.includes('Failed')) return '❌';
        if (status.includes('Login') || status.includes('LOGIN')) return '🔐';
        if (status.includes('Token') || status.includes('Forgery')) return '🔑';
        if (status.includes('COMPLETE') || status.includes('completed')) return '🎯';
        if (status.includes('Checkpoint')) return '⚠️';
        if (status.includes('Processing')) return '⏳';
        if (status.includes('SSL') || status.includes('Connection')) return '🌐';
        return '→';
    }

    getStatusClass(status) {
        if (status.includes('Success') || status.includes('successfully')) return 'status-success';
        if (status.includes('Error') || status.includes('ERROR') || status.includes('Failed')) return 'status-error';
        if (status.includes('COMPLETE')) return 'status-complete';
        if (status.includes('Checkpoint') || status.includes('warning')) return 'status-warning';
        return 'status-info';
    }

    showStatusTracker() {
        const tracker = document.getElementById('boostStatus');
        if (tracker) {
            tracker.style.display = 'block';
        }
    }

    updateUI() {
        const startBtn = document.getElementById('startBoostBtn');
        const stopBtn = document.getElementById('stopBoostBtn');
        
        if (startBtn) startBtn.disabled = this.isRunning;
        if (stopBtn) stopBtn.disabled = !this.isRunning;
        
        if (this.isRunning) {
            if (stopBtn) stopBtn.style.display = 'block';
        } else {
            if (stopBtn) stopBtn.style.display = 'none';
        }
    }

    showMessage(type, message) {
        const msgBox = document.getElementById('boostMessage') || this.createMessageBox();
        msgBox.textContent = message;
        msgBox.className = type + '-msg';
        msgBox.style.display = 'block';
        setTimeout(() => msgBox.style.display = 'none', 4000);
    }

    createMessageBox() {
        const box = document.createElement('div');
        box.id = 'boostMessage';
        box.style.position = 'fixed';
        box.style.top = '100px';
        box.style.left = '50%';
        box.style.transform = 'translateX(-50%)';
        box.style.zIndex = '1000';
        document.body.appendChild(box);
        return box;
    }
}

const boostController = new BoostController();

// Tab switching
function switchTab(tabName) {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('[data-tab]').forEach(t => {
        t.style.display = t.dataset.tab === tabName ? 'block' : 'none';
    });
    event.target.classList.add('active');
}

// Start boost handler
function handleStartBoost() {
    let selectedAccounts = [];
    const accountSource = document.getElementById('accountSource')?.value || 'personal';

    if (accountSource === 'personal') {
        selectedAccounts = igManager.getSelectedAccounts();
    } else {
        // Get selected from admin all accounts
        const checkboxes = document.querySelectorAll('.all-account-checkbox:checked');
        selectedAccounts = Array.from(checkboxes).map(cb => ({
            id: cb.dataset.id,
            username: cb.dataset.username
        }));
    }

    const targetUsername = document.getElementById('targetUsername')?.value || '';
    boostController.isRunning = true;
    boostController.updateUI();
    boostController.startBoost(selectedAccounts, targetUsername, accountSource);
}

// Admin logout
function adminLogout() {
    sessionStorage.removeItem('adminLoggedIn');
    window.location.href = '/admin';
}
