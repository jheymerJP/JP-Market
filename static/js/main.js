document.addEventListener('DOMContentLoaded', function() {
    // Page loader
    const loader = document.getElementById('pageLoader');
    if (loader) {
        setTimeout(() => loader.classList.add('hidden'), 500);
        setTimeout(() => loader.remove(), 1000);
    }

    // Auto-dismiss alerts
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-15px)';
            alert.style.transition = 'all 0.4s ease';
            setTimeout(() => alert.remove(), 400);
        }, 4500);
    });

    // Scroll to top button
    const scrollTopBtn = document.getElementById('scrollTop');
    if (scrollTopBtn) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 400) {
                scrollTopBtn.style.display = 'flex';
                scrollTopBtn.style.opacity = '1';
            } else {
                scrollTopBtn.style.display = 'none';
                scrollTopBtn.style.opacity = '0';
            }
        });
    }

    // Scroll animations
    const animateElements = document.querySelectorAll('[data-animate]');
    if (animateElements.length > 0) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry, index) => {
                if (entry.isIntersecting) {
                    setTimeout(() => {
                        entry.target.style.opacity = '1';
                        entry.target.style.transform = 'translateY(0)';
                    }, index * 80);
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

        animateElements.forEach(el => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(30px)';
            el.style.transition = 'all 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94)';
            observer.observe(el);
        });
    }

    // Quantity buttons in cart
    const quantityForms = document.querySelectorAll('.quantity-form');
    quantityForms.forEach(function(form) {
        const buttons = form.querySelectorAll('.qty-btn');
        buttons.forEach(function(btn) {
            btn.addEventListener('click', function(e) {
                const value = parseInt(this.value);
                if (value < 1) {
                    e.preventDefault();
                }
            });
        });
    });

    // Smooth image loading
    const images = document.querySelectorAll('img');
    images.forEach(img => {
        img.addEventListener('load', function() {
            this.style.opacity = '1';
        });
        if (img.complete) {
            img.style.opacity = '1';
        } else {
            img.style.opacity = '0';
            img.style.transition = 'opacity 0.4s ease';
        }
    });
});

// Mobile menu toggle
function toggleMobileMenu() {
    const menu = document.getElementById('mobileMenu');
    menu.classList.toggle('active');

    let overlay = document.querySelector('.mobile-menu-overlay');
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.className = 'mobile-menu-overlay';
        overlay.onclick = () => toggleMobileMenu();
        document.body.appendChild(overlay);
    }
    overlay.style.display = menu.classList.contains('active') ? 'block' : 'none';
    document.body.style.overflow = menu.classList.contains('active') ? 'hidden' : '';
}
