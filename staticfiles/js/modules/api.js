// =========================
// API (SAVE / TRIP)
// =========================

// Save Places
function initSavePlaces() {
    const container = document.querySelector("[data-save-url]");
    if (!container) return;

    const url = container.dataset.saveUrl;

    document.querySelectorAll(".save-btn").forEach(btn => {
        if (btn.dataset.listenerAdded) return; // avoid double binding
        btn.dataset.listenerAdded = "1";

        btn.addEventListener("click", async function () {
            if (this.dataset.saved === "1") return;

            const card = this.closest(".card, .place-card");
            const actions = card?.querySelector(".action-buttons");

            try {
                const res = await fetch(url, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": getCookie("csrftoken"),
                        "Content-Type": "application/x-www-form-urlencoded"
                    },
                    body: new URLSearchParams({
                        name: this.dataset.name,
                        lat: this.dataset.lat,
                        lon: this.dataset.lon
                    })
                });

                const data = await res.json();

                if (data.success) {
                    this.dataset.saved = "1";
                    this.innerText = "Saved ✓";
                    this.classList.add("btn-secondary");
                    this.classList.remove("btn-primary");

                    if (actions) actions.classList.remove("d-none");

                    showToast("📍 Saved to your places!");
                } else {
                    showToast(data.error || "Error saving place");
                }
            } catch (err) {
                console.error(err);
                showToast("Server error");
            }
        });
    });
}

// Add place to a trip
function initAddToTrip() {
    document.querySelectorAll(".add-to-trip-btn").forEach(btn => {
        if (btn.dataset.listenerAdded) return;
        btn.dataset.listenerAdded = "1";

        btn.addEventListener("click", async function () {
            const card = this.closest(".card");
            const tripSelect = card.querySelector(".trip-select");
            const tripId = tripSelect?.value;

            if (!tripId) return showToast("Please select a trip");

            try {
                const res = await fetch("/add-place-to-trip-ajax/", {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": getCookie("csrftoken"),
                        "Content-Type": "application/x-www-form-urlencoded"
                    },
                    body: new URLSearchParams({
                        place_id: this.dataset.placeId,
                        trip_id: tripId
                    })
                });

                const data = await res.json();

                if (data.success) {
                    showToast(`Added to ${data.trip_name || "trip"}`);
                    this.innerText = "Added ✓";
                    this.disabled = true;
                } else {
                    showToast(data.error || "Failed to add place");
                }
            } catch (err) {
                console.error(err);
                showToast("Server error");
            }
        });
    });
}

// Auto-hide text after X seconds (e.g., instructions on search page)
function initAutoHideText(selector = ".auto-hide-text", delay = 5000) {
    const el = document.querySelector(selector);
    if (!el) return;

    setTimeout(() => {
        el.style.transition = "opacity 0.6s ease";
        el.style.opacity = "0";

        setTimeout(() => el.remove(), 600);
    }, delay);
}