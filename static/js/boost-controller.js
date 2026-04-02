// Boost Controller - Handles boost operations and real-time tracking

class BoostController {
    constructor() {
        this.isRunning = false;
        this.boostStatus = [];
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
                this.showMessage('success', 'Boost started successfully!');
                this.pollBoostStatus();
            } else {
                this.showMessage('error', data.message || 'Failed to start boost');
            }
        } catch (error) {
            this.showMessage('error', 'Error connecting to server: ' + error.message);
        }

        this.isRunning = false;
        this.updateUI();
    }

    async pollBoostStatus() {
        const interval = setInterval(async () => {
            try {
                const response = await fetch('/api/boost-status');
                const data = await response.json();
                
                if (data.status) {
                    this.boostStatus = data.status;
                    this.renderStatus();
                }

                if (!data.running) {
                    clearInterval(interval);
                }
            } catch (error) {
                console.error('Status poll error:', error);
            }
        }, 2000);
    }

    stopBoost() {
        fetch('/api/stop-boost', { method: 'POST' });
        this.isRunning = false;
        this.updateUI();
    }

    renderStatus() {
        const statusContainer = document.getElementById('boostStatus');
        if (!statusContainer) return;

        statusContainer.innerHTML = this.boostStatus.map((status, i) => `
            <div class="status-item">
                <span class="status-label">${status.service || `Attempt ${i + 1}`}</span>
                <span class="status-value">${status.result || 'Processing...'}</span>
            </div>
        `).join('');
    }

    updateUI() {
        const startBtn = document.getElementById('startBoostBtn');
        const stopBtn = document.getElementById('stopBoostBtn');
        
        if (startBtn) startBtn.disabled = this.isRunning;
        if (stopBtn) stopBtn.disabled = !this.isRunning;
    }

    showMessage(type, message) {
        const msgBox = document.getElementById('boostMessage') || this.createMessageBox();
        msgBox.textContent = message;
        msgBox.className = type + '-msg';
        msgBox.style.display = 'block';
        setTimeout(() => msgBox.style.display = 'none', 3000);
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
    boostController.startBoost(selectedAccounts, targetUsername, accountSource);
}

// Admin logout
function adminLogout() {
    sessionStorage.removeItem('adminLoggedIn');
    window.location.href = '/admin';
}
