// IG Account Manager - Handles LocalStorage and UI interactions for user's own IG accounts

class IGAccountManager {
    constructor() {
        this.storageKey = 'ig_accounts';
        this.loadAccounts();
    }

    loadAccounts() {
        const stored = localStorage.getItem(this.storageKey);
        this.accounts = stored ? JSON.parse(stored) : [];
    }

    saveToLocalStorage() {
        localStorage.setItem(this.storageKey, JSON.stringify(this.accounts));
    }

    addAccount(username, password) {
        if (!username || !password) {
            return { success: false, message: 'Username and password required' };
        }
        
        if (this.accounts.some(acc => acc.username === username)) {
            return { success: false, message: 'Account already saved' };
        }

        this.accounts.push({
            id: Date.now(),
            username: username,
            password: password,
            createdAt: new Date().toISOString()
        });

        this.saveToLocalStorage();
        
        // Also save to server
        this.syncToServer();
        
        return { success: true, message: 'Account saved successfully' };
    }

    getAccounts() {
        return this.accounts;
    }

    deleteAccount(id) {
        this.accounts = this.accounts.filter(acc => acc.id !== id);
        this.saveToLocalStorage();
        this.syncToServer();
    }

    syncToServer() {
        fetch('/api/save-ig-account', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ accounts: this.accounts })
        }).catch(err => console.error('Sync error:', err));
    }

    renderAccounts(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        if (this.accounts.length === 0) {
            container.innerHTML = '<p style="color: #b0b0b0;">No saved IG accounts yet.</p>';
            return;
        }

        container.innerHTML = this.accounts.map(acc => `
            <div class="account-card">
                <div style="display: flex; align-items: center; justify-content: space-between;">
                    <div>
                        <input type="checkbox" class="account-checkbox" data-id="${acc.id}" data-username="${acc.username}">
                        <span class="account-username">${acc.username}</span>
                    </div>
                    <button class="delete-btn" onclick="igManager.deleteAccount(${acc.id}); igManager.renderAccounts('${containerId}')">
                        DELETE
                    </button>
                </div>
                <div style="font-size: 11px; color: #808080; margin-top: 10px;">
                    ${new Date(acc.createdAt).toLocaleDateString()}
                </div>
            </div>
        `).join('');
    }

    getSelectedAccounts() {
        const checkboxes = document.querySelectorAll('.account-checkbox:checked');
        return Array.from(checkboxes).map(cb => ({
            id: cb.dataset.id,
            username: cb.dataset.username
        }));
    }
}

// Initialize global manager
const igManager = new IGAccountManager();

// Form submission for adding accounts
document.addEventListener('DOMContentLoaded', function() {
    const addAccountForm = document.getElementById('addAccountForm');
    if (addAccountForm) {
        addAccountForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const username = document.getElementById('newUsername')?.value || '';
            const password = document.getElementById('newPassword')?.value || '';
            
            const result = igManager.addAccount(username, password);
            
            // Show message
            const msgBox = document.getElementById('accountMessage');
            if (msgBox) {
                msgBox.textContent = result.message;
                msgBox.className = result.success ? 'success-msg' : 'error-msg';
                msgBox.style.display = 'block';
                setTimeout(() => msgBox.style.display = 'none', 3000);
            }
            
            if (result.success) {
                addAccountForm.reset();
                igManager.renderAccounts('myAccounts');
            }
        });
    }

    // Initial render
    igManager.renderAccounts('myAccounts');
});
