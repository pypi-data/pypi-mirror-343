/**
 * Dashboard Components JavaScript
 * Handles functionality for all dashboard components
 */

/**
 * Initialize a data table component
 * @param {string} id - Table ID
 * @param {Object} options - Configuration options
 */
function initDataTable(id, options = {}) {
    const tableContainer = document.getElementById(`${id}-container`);
    const table = document.getElementById(id);
    if (!table) return;
    
    const defaults = {
        sortable: false,
        searchable: false,
        pagination: false,
        itemsPerPage: 10
    };
    
    const config = { ...defaults, ...options };
    const rows = Array.from(table.querySelectorAll('tbody tr'));
    let filteredRows = [...rows];
    let currentPage = 1;
    
    // Sorting functionality
    if (config.sortable) {
        const headers = table.querySelectorAll('th[data-sort-col]');
        headers.forEach(header => {
            header.addEventListener('click', () => {
                const column = parseInt(header.getAttribute('data-sort-col'));
                const isAscending = header.getAttribute('data-sort-dir') !== 'asc';
                
                // Update sort direction
                headers.forEach(h => h.removeAttribute('data-sort-dir'));
                header.setAttribute('data-sort-dir', isAscending ? 'asc' : 'desc');
                
                // Update sort icons
                headers.forEach(h => {
                    const icon = h.querySelector('.sort-icon');
                    if (icon) {
                        icon.innerHTML = `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16V4m0 0L3 8m4-4l4 4m6 0v12m0 0l4-4m-4 4l-4-4" />`;
                    }
                });
                
                const sortIcon = header.querySelector('.sort-icon');
                if (sortIcon) {
                    sortIcon.innerHTML = isAscending 
                        ? `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7" />`
                        : `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />`;
                }
                
                // Sort rows
                filteredRows.sort((a, b) => {
                    const aValue = a.querySelectorAll('td')[column].textContent.trim();
                    const bValue = b.querySelectorAll('td')[column].textContent.trim();
                    
                    // Check if values are numbers
                    const aNum = parseFloat(aValue);
                    const bNum = parseFloat(bValue);
                    
                    if (!isNaN(aNum) && !isNaN(bNum)) {
                        return isAscending ? aNum - bNum : bNum - aNum;
                    }
                    
                    // Sort as strings
                    return isAscending 
                        ? aValue.localeCompare(bValue)
                        : bValue.localeCompare(aValue);
                });
                
                renderTable();
            });
        });
    }
    
    // Search functionality
    if (config.searchable) {
        const searchInput = document.getElementById(`${id}-search`);
        if (searchInput) {
            searchInput.addEventListener('input', () => {
                const searchTerm = searchInput.value.toLowerCase().trim();
                
                if (searchTerm === '') {
                    filteredRows = [...rows];
                } else {
                    filteredRows = rows.filter(row => {
                        const text = row.textContent.toLowerCase();
                        return text.includes(searchTerm);
                    });
                }
                
                currentPage = 1;
                renderTable();
            });
        }
    }
    
    // Pagination functionality
    if (config.pagination) {
        const prevBtn = document.getElementById(`${id}-prev`);
        const nextBtn = document.getElementById(`${id}-next`);
        const prevBtnMobile = document.getElementById(`${id}-prev-mobile`);
        const nextBtnMobile = document.getElementById(`${id}-next-mobile`);
        const pageNumbers = document.getElementById(`${id}-page-numbers`);
        
        if (prevBtn && nextBtn) {
            prevBtn.addEventListener('click', () => {
                if (currentPage > 1) {
                    currentPage--;
                    renderTable();
                }
            });
            
            nextBtn.addEventListener('click', () => {
                const totalPages = Math.ceil(filteredRows.length / config.itemsPerPage);
                if (currentPage < totalPages) {
                    currentPage++;
                    renderTable();
                }
            });
        }
        
        if (prevBtnMobile && nextBtnMobile) {
            prevBtnMobile.addEventListener('click', () => {
                if (currentPage > 1) {
                    currentPage--;
                    renderTable();
                }
            });
            
            nextBtnMobile.addEventListener('click', () => {
                const totalPages = Math.ceil(filteredRows.length / config.itemsPerPage);
                if (currentPage < totalPages) {
                    currentPage++;
                    renderTable();
                }
            });
        }
    }
    
    // Initial render
    renderTable();
    
    // Render table with current filters and pagination
    function renderTable() {
        const tbody = table.querySelector('tbody');
        tbody.innerHTML = '';
        
        if (filteredRows.length === 0) {
            const emptyRow = document.createElement('tr');
            const emptyCell = document.createElement('td');
            const colSpan = table.querySelectorAll('th').length;
            
            emptyCell.setAttribute('colspan', colSpan);
            emptyCell.className = 'px-6 py-4 text-center text-sm text-gray-500 dark:text-gray-400';
            emptyCell.textContent = 'No data available';
            
            emptyRow.appendChild(emptyCell);
            tbody.appendChild(emptyRow);
            
            updatePaginationInfo(0, 0, 0);
            return;
        }
        
        let start, end;
        
        if (config.pagination) {
            const totalPages = Math.ceil(filteredRows.length / config.itemsPerPage);
            start = (currentPage - 1) * config.itemsPerPage;
            end = Math.min(start + config.itemsPerPage, filteredRows.length);
            
            updatePaginationInfo(start + 1, end, filteredRows.length);
            updatePaginationControls(currentPage, totalPages);
        } else {
            start = 0;
            end = filteredRows.length;
        }
        
        // Add visible rows to the table
        for (let i = start; i < end; i++) {
            tbody.appendChild(filteredRows[i].cloneNode(true));
        }
    }
    
    // Update pagination information
    function updatePaginationInfo(start, end, total) {
        if (!config.pagination) return;
        
        const startEl = document.getElementById(`${id}-page-start`);
        const endEl = document.getElementById(`${id}-page-end`);
        const totalEl = document.getElementById(`${id}-total`);
        
        if (startEl) startEl.textContent = total > 0 ? start : 0;
        if (endEl) endEl.textContent = end;
        if (totalEl) totalEl.textContent = total;
    }
    
    // Update pagination controls
    function updatePaginationControls(current, total) {
        if (!config.pagination) return;
        
        const prevBtn = document.getElementById(`${id}-prev`);
        const nextBtn = document.getElementById(`${id}-next`);
        const prevBtnMobile = document.getElementById(`${id}-prev-mobile`);
        const nextBtnMobile = document.getElementById(`${id}-next-mobile`);
        const pageNumbers = document.getElementById(`${id}-page-numbers`);
        
        if (prevBtn) prevBtn.disabled = current <= 1;
        if (nextBtn) nextBtn.disabled = current >= total;
        if (prevBtnMobile) prevBtnMobile.disabled = current <= 1;
        if (nextBtnMobile) nextBtnMobile.disabled = current >= total;
        
        if (pageNumbers) {
            pageNumbers.textContent = `Page ${current} of ${total}`;
        }
    }
}

/**
 * Initialize modal functionality
 */
document.addEventListener('DOMContentLoaded', function() {
    // Find all modal close buttons
    const closeButtons = document.querySelectorAll('[data-modal-close]');
    closeButtons.forEach(button => {
        const modalId = button.getAttribute('data-modal-close');
        const modal = document.getElementById(modalId);
        const backdrop = document.getElementById(`${modalId}-backdrop`);
        
        if (modal && backdrop) {
            button.addEventListener('click', () => {
                modal.classList.add('hidden');
                backdrop.classList.add('hidden');
                document.body.classList.remove('overflow-hidden');
            });
        }
    });
    
    // Find all modal triggers
    const modalTriggers = document.querySelectorAll('[data-modal-target]');
    modalTriggers.forEach(trigger => {
        const modalId = trigger.getAttribute('data-modal-target');
        const modal = document.getElementById(modalId);
        const backdrop = document.getElementById(`${modalId}-backdrop`);
        
        if (modal && backdrop) {
            trigger.addEventListener('click', () => {
                modal.classList.remove('hidden');
                backdrop.classList.remove('hidden');
                document.body.classList.add('overflow-hidden');
            });
        }
    });
    
    // Close modal when clicking outside
    const modals = document.querySelectorAll('[role="dialog"]');
    modals.forEach(modal => {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                const modalId = modal.getAttribute('id');
                const backdrop = document.getElementById(`${modalId}-backdrop`);
                
                modal.classList.add('hidden');
                if (backdrop) backdrop.classList.add('hidden');
                document.body.classList.remove('overflow-hidden');
            }
        });
    });
    
    // Close modal with Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            const visibleModal = document.querySelector('[role="dialog"]:not(.hidden)');
            if (visibleModal) {
                const modalId = visibleModal.getAttribute('id');
                const backdrop = document.getElementById(`${modalId}-backdrop`);
                
                visibleModal.classList.add('hidden');
                if (backdrop) backdrop.classList.add('hidden');
                document.body.classList.remove('overflow-hidden');
            }
        }
    });
});

/**
 * Show a toast notification
 * @param {string} message - Notification message
 * @param {string} type - Notification type (success, error, warning, info)
 * @param {number} duration - Duration in milliseconds
 */
function showToast(message, type = 'info', duration = 3000) {
    // Create toast container if it doesn't exist
    let container = document.getElementById('toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'fixed bottom-4 right-4 z-50';
        document.body.appendChild(container);
    }
    
    // Create toast element
    const toastId = `toast-${Date.now()}`;
    const toast = document.createElement('div');
    toast.id = toastId;
    toast.className = 'transform transition-all duration-300 translate-y-2 opacity-0';
    
    // Set toast content based on type
    let bgColor, iconPath;
    switch (type) {
        case 'success':
            bgColor = 'bg-green-500';
            iconPath = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />';
            break;
        case 'error':
            bgColor = 'bg-red-500';
            iconPath = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />';
            break;
        case 'warning':
            bgColor = 'bg-yellow-500';
            iconPath = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />';
            break;
        case 'info':
        default:
            bgColor = 'bg-blue-500';
            iconPath = '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />';
            break;
    }
    
    toast.innerHTML = `
        <div class="rounded-lg shadow-lg p-4 mb-4 flex items-center ${bgColor} text-white">
            <div class="flex-shrink-0 mr-3">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    ${iconPath}
                </svg>
            </div>
            <div class="flex-1">
                ${message}
            </div>
            <button type="button" class="ml-4 flex-shrink-0 text-white focus:outline-none" onclick="this.parentNode.parentNode.remove()">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
            </button>
        </div>
    `;
    
    // Add toast to container
    container.appendChild(toast);
    
    // Animate in
    setTimeout(() => {
        toast.classList.remove('translate-y-2', 'opacity-0');
    }, 10);
    
    // Auto remove after duration
    setTimeout(() => {
        toast.classList.add('translate-y-2', 'opacity-0');
        setTimeout(() => {
            toast.remove();
        }, 300);
    }, duration);
    
    return toastId;
}
