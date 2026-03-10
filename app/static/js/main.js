/**
 * AgriSense — Main JavaScript
 * Handles navigation toggle, scroll effects, and page interactions
 */

document.addEventListener('DOMContentLoaded', function () {
    // ── Mobile Navigation Toggle ──────────────────────
    const navToggle = document.getElementById('nav-toggle');
    const navLinks = document.getElementById('nav-links');

    if (navToggle && navLinks) {
        navToggle.addEventListener('click', function () {
            navLinks.classList.toggle('nav__links--open');
            const isOpen = navLinks.classList.contains('nav__links--open');
            navToggle.setAttribute('aria-expanded', isOpen);
        });

        // Close menu when clicking a link
        navLinks.querySelectorAll('.nav__link').forEach(function (link) {
            link.addEventListener('click', function () {
                navLinks.classList.remove('nav__links--open');
            });
        });
    }

    // ── Scroll-based nav background ───────────────────
    const nav = document.getElementById('main-nav');
    if (nav) {
        var lastScroll = 0;
        window.addEventListener('scroll', function () {
            var scrollY = window.scrollY;
            if (scrollY > 40) {
                nav.style.borderBottomColor = 'rgba(255,255,255,0.1)';
            } else {
                nav.style.borderBottomColor = 'rgba(255,255,255,0.07)';
            }
            lastScroll = scrollY;
        }, { passive: true });
    }

    // ── Fade in elements on scroll ────────────────────
    var observerOptions = {
        threshold: 0.12,
        rootMargin: '0px 0px -40px 0px',
    };

    var fadeObserver = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                fadeObserver.unobserve(entry.target);
            }
        });
    }, observerOptions);

    var fadeElements = document.querySelectorAll(
        '.feature-card, .crop-tag, .recent-card, .history-card, .info-block, .about-block, .dash-stat-card, .chart-card'
    );
    fadeElements.forEach(function (el) {
        el.style.opacity = '0';
        el.style.transform = 'translateY(16px)';
        el.style.transition = 'opacity 0.5s cubic-bezier(0.16, 1, 0.3, 1), transform 0.5s cubic-bezier(0.16, 1, 0.3, 1)';
        fadeObserver.observe(el);
    });

    // Stagger the animation for grid items
    var gridContainers = document.querySelectorAll(
        '.features__grid, .crops-grid, .recent-grid, .history-grid, .about-grid, .dash-stats, .dash-charts'
    );
    gridContainers.forEach(function (container) {
        var children = container.children;
        for (var i = 0; i < children.length; i++) {
            children[i].style.transitionDelay = (i * 60) + 'ms';
        }
    });

    // ── Auto-dismiss flash messages ───────────────────
    var flashes = document.querySelectorAll('.flash');
    flashes.forEach(function (flash) {
        setTimeout(function () {
            flash.style.opacity = '0';
            flash.style.transform = 'translateY(-12px)';
            setTimeout(function () {
                if (flash.parentNode) flash.parentNode.removeChild(flash);
            }, 300);
        }, 5000);
    });
});
