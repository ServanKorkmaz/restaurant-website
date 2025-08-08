// Main JavaScript for Nawarat Thai Restaurant

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', function() {
    initMenuFilters();
    initMenuSearch();
    initSmoothScroll();
    initLazyLoading();
    initCateringForm();
    initAccessibility();
    initSortable();
});

// Menu Filtering
function initMenuFilters() {
    const filterButtons = document.querySelectorAll('.filter-btn');
    const menuItems = document.querySelectorAll('.dish-card');
    
    if (!filterButtons.length) return;
    
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            const category = this.dataset.category;
            
            // Update active button
            filterButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            // Filter items
            menuItems.forEach(item => {
                if (category === 'alle' || item.dataset.category === category) {
                    item.parentElement.style.display = '';
                    item.parentElement.classList.add('fade-in');
                } else {
                    item.parentElement.style.display = 'none';
                }
            });
        });
    });
}

// Menu Search
function initMenuSearch() {
    const searchInput = document.getElementById('menuSearch');
    const menuItems = document.querySelectorAll('.dish-card');
    
    if (!searchInput) return;
    
    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        
        menuItems.forEach(item => {
            const name = item.dataset.name || '';
            const description = item.querySelector('.card-text')?.textContent.toLowerCase() || '';
            
            if (name.includes(searchTerm) || description.includes(searchTerm)) {
                item.parentElement.style.display = '';
                item.parentElement.classList.add('fade-in');
            } else {
                item.parentElement.style.display = 'none';
            }
        });
        
        // Update results count
        const visibleItems = document.querySelectorAll('.dish-card:not([style*="display: none"])').length;
        const resultsText = document.getElementById('searchResults');
        if (resultsText) {
            if (searchTerm) {
                resultsText.textContent = `${visibleItems} resultater funnet`;
            } else {
                resultsText.textContent = '';
            }
        }
    });
}

// Smooth Scroll
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href === '#') return;
            
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                const offset = 80; // Account for fixed header
                const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - offset;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// Lazy Loading Enhancement
function initLazyLoading() {
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    
                    // Load image
                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                        img.removeAttribute('data-src');
                    }
                    
                    // Add fade-in effect
                    img.classList.add('fade-in');
                    observer.unobserve(img);
                }
            });
        }, {
            rootMargin: '50px'
        });
        
        // Observe all lazy images
        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }
}

// Catering Form Handling
function initCateringForm() {
    const form = document.getElementById('cateringForm');
    if (!form) return;
    
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const submitBtn = form.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        
        // Show loading state
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Sender...';
        
        try {
            const formData = new FormData(form);
            const response = await fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            
            if (response.ok) {
                // Success
                showAlert('success', 'Takk for din forespørsel! Vi tar kontakt innen 24 timer.');
                form.reset();
                
                // Close modal if exists
                const modal = bootstrap.Modal.getInstance(document.getElementById('cateringModal'));
                if (modal) {
                    setTimeout(() => modal.hide(), 2000);
                }
            } else {
                // Error
                const data = await response.json();
                showAlert('error', data.message || 'Noe gikk galt. Vennligst prøv igjen.');
            }
        } catch (error) {
            showAlert('error', 'Kunne ikke sende forespørsel. Vennligst sjekk internettforbindelsen.');
        } finally {
            // Reset button
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalText;
        }
    });
}

// Show Alert Message
function showAlert(type, message) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type === 'success' ? 'success' : 'danger'} alert-dismissible fade show position-fixed top-0 start-50 translate-middle-x mt-3`;
    alertDiv.style.zIndex = '9999';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

// Accessibility Enhancements
function initAccessibility() {
    // Handle keyboard navigation for menu
    document.addEventListener('keydown', function(e) {
        // ESC key closes modals
        if (e.key === 'Escape') {
            const modals = document.querySelectorAll('.modal.show');
            modals.forEach(modal => {
                const bsModal = bootstrap.Modal.getInstance(modal);
                if (bsModal) bsModal.hide();
            });
        }
    });
    
    // Improve focus visibility
    document.body.classList.add('js-focus-visible');
    
    // Add ARIA labels to icons
    document.querySelectorAll('i[class*="fa-"]').forEach(icon => {
        if (!icon.getAttribute('aria-label') && !icon.getAttribute('aria-hidden')) {
            icon.setAttribute('aria-hidden', 'true');
        }
    });
}

// Sortable for Admin
function initSortable() {
    const sortableList = document.getElementById('sortableMenu');
    if (!sortableList || typeof Sortable === 'undefined') return;
    
    new Sortable(sortableList, {
        animation: 150,
        handle: '.sortable-handle',
        ghostClass: 'dragging',
        onEnd: async function(evt) {
            const items = [];
            sortableList.querySelectorAll('.sortable-item').forEach((item, index) => {
                items.push({
                    id: item.dataset.id,
                    order: index + 1
                });
            });
            
            // Send new order to server
            try {
                const response = await fetch('/admin/menu/reorder', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': document.querySelector('meta[name="csrf-token"]')?.content
                    },
                    body: JSON.stringify({ items })
                });
                
                if (response.ok) {
                    showAlert('success', 'Rekkefølge oppdatert');
                }
            } catch (error) {
                showAlert('error', 'Kunne ikke oppdatere rekkefølge');
            }
        }
    });
}

// Fade-in Animation
const fadeInObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
        }
    });
}, {
    threshold: 0.1
});

// Observe elements with fade-in class
document.querySelectorAll('.fade-in-up').forEach(el => {
    fadeInObserver.observe(el);
});

// Utility Functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Performance: Defer non-critical scripts
if ('requestIdleCallback' in window) {
    requestIdleCallback(() => {
        // Load analytics or other non-critical scripts here
    });
}