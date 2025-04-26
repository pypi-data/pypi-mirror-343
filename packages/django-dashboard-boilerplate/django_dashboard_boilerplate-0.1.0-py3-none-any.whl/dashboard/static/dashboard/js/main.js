/**
 * Main JavaScript file for the Dashboard
 * Handles all interactive functionality
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initSidebar();
    initThemeToggle();
    initDropdowns();
});

/**
 * Sidebar functionality
 * Handles opening and closing the sidebar on mobile devices
 */
function initSidebar() {
    const sidebar = document.getElementById('sidebar');
    const sidebarOverlay = document.getElementById('sidebarOverlay');
    const openSidebarBtn = document.getElementById('openSidebarBtn');
    const closeSidebarBtn = document.getElementById('closeSidebarBtn');
    
    if (!sidebar || !sidebarOverlay || !openSidebarBtn || !closeSidebarBtn) return;
    
    // Check if we should hide sidebar on page load (mobile view)
    function checkScreenSize() {
        if (window.innerWidth < 768) { // md breakpoint in Tailwind
            sidebar.classList.add('-translate-x-full');
            sidebarOverlay.classList.add('hidden');
        } else {
            sidebar.classList.remove('-translate-x-full');
        }
    }
    
    // Run on page load
    checkScreenSize();
    
    // Run on resize
    window.addEventListener('resize', checkScreenSize);
    
    // Open sidebar
    openSidebarBtn.addEventListener('click', function() {
        sidebar.classList.remove('-translate-x-full');
        sidebarOverlay.classList.remove('hidden');
        document.body.classList.add('overflow-hidden', 'md:overflow-auto'); // Prevent scrolling on mobile when sidebar is open
    });
    
    // Close sidebar (button or overlay click)
    function closeSidebar() {
        sidebar.classList.add('-translate-x-full');
        sidebarOverlay.classList.add('hidden');
        document.body.classList.remove('overflow-hidden', 'md:overflow-auto');
    }
    
    closeSidebarBtn.addEventListener('click', closeSidebar);
    sidebarOverlay.addEventListener('click', closeSidebar);
}

/**
 * Theme toggle functionality
 * Switches between light and dark mode
 */
function initThemeToggle() {
    const themeToggle = document.getElementById('themeToggle');
    
    if (!themeToggle) return;
    
    // Check for saved theme preference or use system preference
    if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        document.documentElement.classList.add('dark');
    } else {
        document.documentElement.classList.remove('dark');
    }
    
    // Toggle theme
    themeToggle.addEventListener('click', function() {
        if (document.documentElement.classList.contains('dark')) {
            document.documentElement.classList.remove('dark');
            localStorage.theme = 'light';
        } else {
            document.documentElement.classList.add('dark');
            localStorage.theme = 'dark';
        }
    });
}

/**
 * Dropdown functionality
 * Handles user menu and notification dropdowns
 */
function initDropdowns() {
    initDropdown('userMenuBtn', 'userMenuDropdown');
    initDropdown('notificationBtn', 'notificationDropdown');
}

function initDropdown(btnId, dropdownId) {
    const btn = document.getElementById(btnId);
    const dropdown = document.getElementById(dropdownId);
    
    if (!btn || !dropdown) return;
    
    // Toggle dropdown
    btn.addEventListener('click', function(e) {
        e.stopPropagation();
        dropdown.classList.toggle('hidden');
    });
    
    // Close dropdown when clicking outside
    document.addEventListener('click', function(e) {
        if (!dropdown.contains(e.target) && !btn.contains(e.target)) {
            dropdown.classList.add('hidden');
        }
    });
}

/**
 * Create a card element
 * @param {string} title - Card title
 * @param {string} content - Card content (HTML allowed)
 * @param {string} className - Additional CSS classes
 * @returns {HTMLElement} - Card element
 */
function createCard(title, content, className = '') {
    const card = document.createElement('div');
    card.className = `bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 border border-gray-200 dark:border-gray-700 ${className}`;
    
    if (title) {
        const titleEl = document.createElement('h2');
        titleEl.className = 'text-lg font-semibold text-gray-800 dark:text-white mb-4';
        titleEl.textContent = title;
        card.appendChild(titleEl);
    }
    
    if (content) {
        const contentEl = document.createElement('div');
        contentEl.className = 'text-gray-600 dark:text-gray-400';
        contentEl.innerHTML = content;
        card.appendChild(contentEl);
    }
    
    return card;
}

/**
 * Show a notification toast
 * @param {string} message - Notification message
 * @param {string} type - Notification type (success, error, warning, info)
 * @param {number} duration - Duration in milliseconds
 */
function showNotification(message, type = 'info', duration = 3000) {
    const container = document.createElement('div');
    container.className = 'fixed bottom-4 right-4 z-50';
    
    const toast = document.createElement('div');
    toast.className = 'rounded-lg shadow-lg p-4 mb-4 flex items-center transition-opacity duration-500';
    
    // Set background color based on type
    switch (type) {
        case 'success':
            toast.classList.add('bg-green-500', 'text-white');
            break;
        case 'error':
            toast.classList.add('bg-red-500', 'text-white');
            break;
        case 'warning':
            toast.classList.add('bg-yellow-500', 'text-white');
            break;
        case 'info':
        default:
            toast.classList.add('bg-blue-500', 'text-white');
            break;
    }
    
    // Add icon based on type
    const icon = document.createElement('div');
    icon.className = 'flex-shrink-0 mr-3';
    
    let iconSvg = '';
    switch (type) {
        case 'success':
            iconSvg = '<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" /></svg>';
            break;
        case 'error':
            iconSvg = '<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>';
            break;
        case 'warning':
            iconSvg = '<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>';
            break;
        case 'info':
        default:
            iconSvg = '<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>';
            break;
    }
    
    icon.innerHTML = iconSvg;
    toast.appendChild(icon);
    
    // Add message
    const messageEl = document.createElement('div');
    messageEl.className = 'flex-1';
    messageEl.textContent = message;
    toast.appendChild(messageEl);
    
    // Add close button
    const closeBtn = document.createElement('button');
    closeBtn.className = 'ml-4 flex-shrink-0 text-white focus:outline-none';
    closeBtn.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>';
    closeBtn.addEventListener('click', function() {
        container.remove();
    });
    toast.appendChild(closeBtn);
    
    container.appendChild(toast);
    document.body.appendChild(container);
    
    // Auto remove after duration
    setTimeout(function() {
        toast.classList.add('opacity-0');
        setTimeout(function() {
            container.remove();
        }, 500);
    }, duration);
}
