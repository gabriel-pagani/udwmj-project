document.addEventListener('DOMContentLoaded', function() {
    const accountTrigger = document.getElementById('account-trigger');
    const accountDropdown = document.getElementById('account-dropdown');
    
    if (accountTrigger && accountDropdown) {
        accountTrigger.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            accountDropdown.classList.toggle('show');
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', function(e) {
            if (!accountTrigger.contains(e.target) && !accountDropdown.contains(e.target)) {
                accountDropdown.classList.remove('show');
            }
        });

        // Close dropdown when pressing Escape
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                accountDropdown.classList.remove('show');
            }
        });
    }
});