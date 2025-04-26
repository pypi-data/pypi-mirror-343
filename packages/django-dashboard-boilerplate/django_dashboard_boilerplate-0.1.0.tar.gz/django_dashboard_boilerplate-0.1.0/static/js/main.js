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
 * Create a reusable card component
 * @param {string} title - Card title
 * @param {string} content - Card content
 * @param {string} className - Additional CSS classes
 * @returns {HTMLElement} - Card element
 */
function createCard(title, content, className = '') {
    const card = document.createElement('div');
    card.className = `bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 border border-gray-200 dark:border-gray-700 ${className}`;
    
    if (title) {
        const titleEl = document.createElement('h3');
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
        default:
            toast.classList.add('bg-primary-500', 'text-white');
    }
    
    toast.innerHTML = `
        <div class="mr-3">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="${type === 'success' ? 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z' : 'M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z'}" />
            </svg>
        </div>
        <div>${message}</div>
        <button class="ml-auto text-white hover:text-gray-200">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
        </button>
    `;
    
    container.appendChild(toast);
    document.body.appendChild(container);
    
    // Close button functionality
    const closeBtn = toast.querySelector('button');
    closeBtn.addEventListener('click', function() {
        container.remove();
    });
    
    // Auto-remove after duration
    setTimeout(function() {
        toast.classList.add('opacity-0');
        setTimeout(function() {
            container.remove();
        }, 500);
    }, duration);
}