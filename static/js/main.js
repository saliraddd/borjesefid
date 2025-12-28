// Borj Sefid - Flight Booking System
// Main JavaScript File

// DOM Ready
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Initialize event listeners
    setupSearchForm();
    setupFilters();
    setupBookingForm();
    setupSortButtons();
}

// Search Form Setup
function setupSearchForm() {
    const searchForm = document.querySelector('.search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            // Form validation can be added here
            console.log('Search form submitted');
        });
    }
}

// Filter Setup
function setupFilters() {
    const filterForm = document.querySelector('.filter-form');
    if (filterForm) {
        const inputs = filterForm.querySelectorAll('input, select');
        inputs.forEach(input => {
            input.addEventListener('change', function() {
                // Auto-submit filter form on change
                // Uncomment to enable
                // filterForm.submit();
            });
        });
    }
}

// Booking Form Setup
function setupBookingForm() {
    const bookingForm = document.querySelector('.booking-form');
    if (bookingForm) {
        bookingForm.addEventListener('submit', function(e) {
            if (!validateBookingForm()) {
                e.preventDefault();
                showAlert('Please fill all required fields', 'error');
            }
        });
    }
}

// Validate Booking Form
function validateBookingForm() {
    const requiredFields = document.querySelectorAll('input[required], select[required], textarea[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            isValid = false;
            field.style.borderColor = '#e74c3c';
            field.addEventListener('focus', function() {
                this.style.borderColor = '';
            });
        }
    });
    
    return isValid;
}

// Sort Buttons Setup
function setupSortButtons() {
    const sortButtons = document.querySelectorAll('.sort-btn');
    sortButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            sortButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            // Navigate to sort URL
            window.location.href = this.href;
        });
    });
}

// Show Alert Message
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;
    alertDiv.style.position = 'fixed';
    alertDiv.style.top = '100px';
    alertDiv.style.right = '20px';
    alertDiv.style.zIndex = '1000';
    alertDiv.style.maxWidth = '400px';
    
    document.body.appendChild(alertDiv);
    
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

// Format Currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('fa-IR', {
        style: 'currency',
        currency: 'IRR'
    }).format(amount);
}

// Format Date
function formatDate(dateString) {
    const options = { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric',
        locale: 'fa-IR'
    };
    return new Date(dateString).toLocaleDateString('fa-IR', options);
}

// Format Time
function formatTime(dateString) {
    const options = { 
        hour: '2-digit', 
        minute: '2-digit',
        locale: 'fa-IR'
    };
    return new Date(dateString).toLocaleTimeString('fa-IR', options);
}

// Smooth Scroll
function smoothScroll(target) {
    const element = document.querySelector(target);
    if (element) {
        element.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

// Add to Favorites (for future use)
function addToFavorites(flightId) {
    // TODO: Implement favorites functionality
    console.log('Added flight', flightId, 'to favorites');
}

// Print Booking
function printBooking(bookingCode) {
    const printWindow = window.open('', '', 'width=800,height=600');
    const booking = document.querySelector(`[data-booking="${bookingCode}"]`);
    
    if (booking) {
        printWindow.document.write('<html><head><title>Print Booking</title></head><body>');
        printWindow.document.write(booking.innerHTML);
        printWindow.document.write('</body></html>');
        printWindow.document.close();
        printWindow.print();
    }
}

// Cancel Booking with Confirmation
function cancelBooking(bookingId) {
    if (confirm('آیا مطمئن هستید که می‌خواهید این رزرو را لغو کنید؟')) {
        window.location.href = `/bookings/${bookingId}/cancel/`;
    }
}

// Filter Flights by Price
function filterByPrice(minPrice, maxPrice) {
    const flights = document.querySelectorAll('.flight-result');
    
    flights.forEach(flight => {
        const priceElement = flight.querySelector('.price');
        if (priceElement) {
            const price = parseInt(priceElement.textContent);
            
            if (price >= minPrice && price <= maxPrice) {
                flight.style.display = 'block';
            } else {
                flight.style.display = 'none';
            }
        }
    });
}

// Get Query Parameter
function getQueryParameter(param) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
}

// Update query string
function updateQueryString(key, value) {
    const urlParams = new URLSearchParams(window.location.search);
    urlParams.set(key, value);
    window.history.pushState({}, '', `${window.location.pathname}?${urlParams}`);
}

// Export functions for use in templates
window.bookingApp = {
    smoothScroll,
    addToFavorites,
    printBooking,
    cancelBooking,
    filterByPrice,
    getQueryParameter,
    updateQueryString,
    formatCurrency,
    formatDate,
    formatTime,
    showAlert
};
