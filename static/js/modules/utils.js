// =========================
// UTILS
// =========================

function onReady(callback) {
    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", callback);
    } else {
        callback();
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie) {
        const cookies = document.cookie.split(";");
        for (let c of cookies) {
            c = c.trim();
            if (c.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(c.split("=")[1]);
                break; // stop after finding the cookie
            }
        }
    }
    return cookieValue;
}

// =========================
// SHOW TOAST (Bootstrap 5)
// =========================
function showToast(message) {
    // Create toast container if it doesn't exist
    let container = document.querySelector(".toast-container");
    if (!container) {
        container = document.createElement("div");
        container.className = "toast-container position-fixed bottom-0 end-0 p-3";
        document.body.appendChild(container);
    }

    // Create toast element
    const toastEl = document.createElement("div");
    toastEl.className = "toast align-items-center text-bg-success border-0";
    toastEl.setAttribute("role", "alert");
    toastEl.setAttribute("aria-live", "assertive");
    toastEl.setAttribute("aria-atomic", "true");

    toastEl.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
    `;

    container.appendChild(toastEl);

    // Initialize Bootstrap toast with auto-hide (2.5 seconds)
    const bsToast = new bootstrap.Toast(toastEl, { delay: 2500 });
    bsToast.show();

    // Remove from DOM after hidden
    toastEl.addEventListener("hidden.bs.toast", () => toastEl.remove());
}