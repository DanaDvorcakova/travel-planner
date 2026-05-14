// =========================
// UI FEATURES
// =========================

function initSidebar() {
    window.toggleSidebar = function () {
        document.getElementById("sidebar")?.classList.toggle("active");
        document.getElementById("overlay")?.classList.toggle("active");
    };

    document.addEventListener("click", function (e) {
        const sidebar = document.getElementById("sidebar");
        const toggle = document.querySelector(".menu-toggle");

        if (!sidebar || !toggle) return;

        if (
            sidebar.classList.contains("active") &&
            !sidebar.contains(e.target) &&
            !toggle.contains(e.target)
        ) {
            sidebar.classList.remove("active");
            document.getElementById("overlay")?.classList.remove("active");
        }
    });
}

// =========================
// LIVE SEARCH
// =========================
function initLiveSearch() {
    const input = document.getElementById("searchInput");
    if (!input) return;

    input.addEventListener("input", function () {
        const q = this.value.toLowerCase();

        document.querySelectorAll(".card").forEach(card => {
            const match = card.innerText.toLowerCase().includes(q);
            card.style.display = match ? "" : "none";
        });

        // ❌ FIXED: do NOT auto-clear input instantly (this was breaking UX)
    });
}

// =========================
// SHOW MORE REVIEWS
// =========================
function initShowMoreReviews() {
    const btn = document.getElementById("showMoreReviewsBtn");
    if (!btn) return;

    btn.addEventListener("click", () => {
        document.querySelectorAll(".extra-review").forEach(el => {
            el.classList.remove("d-none");
        });
        btn.style.display = "none";
    });
}

// =========================
// TOGGLE ALL (BOOTSTRAP)
// =========================
function initToggleAll() {
    window.toggleAll = function (show) {
        document.querySelectorAll(".collapse").forEach(el => {
            const instance = bootstrap.Collapse.getOrCreateInstance(el, {
                toggle: false
            });
            show ? instance.show() : instance.hide();
        });
    };
}

// =========================
// AUTO HIDE TEXT (FIXED)
// =========================
function initAutoHideText() {
    const el = document.querySelector(".auto-hide-text");
    if (!el) return;

    setTimeout(() => {
        el.style.transition = "opacity 0.6s ease";
        el.style.opacity = "0";

        setTimeout(() => {
            el.remove();
        }, 600);

    }, 4000);
}

// =========================
// CAROUSEL
// =========================
window.scrollDestinations = function (direction) {
    const container = document.getElementById("destinationsCarousel");
    if (!container) return;

    const scrollAmount = container.offsetWidth * 0.8;

    container.scrollBy({
        left: direction * scrollAmount,
        behavior: "smooth"
    });
};

// =========================
// AUTO DISMISS ALERTS (Django messages)
// =========================
function initAutoDismissAlerts() {
    const alerts = document.querySelectorAll('.alert');

    alerts.forEach(alert => {
        // Add Bootstrap dismiss class if missing
        if (!alert.classList.contains('fade')) alert.classList.add('fade', 'show');

        // Auto-dismiss after 3 seconds
        setTimeout(() => {
            // Get or create Bootstrap Alert instance
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            bsAlert.close();
        }, 3000);
    });
}

// Back to Top Button
function initBackToTop() {
    const backToTopBtn = document.getElementById('backToTopBtn');
    if (!backToTopBtn) return;

    window.addEventListener('scroll', () => {
        if (window.scrollY > 200) {
            backToTopBtn.style.display = "flex";
            backToTopBtn.style.alignItems = "center";
            backToTopBtn.style.justifyContent = "center";
        } else {
            backToTopBtn.style.display = "none";
        }
    });

    backToTopBtn.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
}