// =========================
// LEAFLET MAP
// =========================
function initMap() {
    const el = document.getElementById("map");
    if (!el || typeof L === "undefined") return;

    const lat = parseFloat(el.dataset.lat);
    const lon = parseFloat(el.dataset.lon);

    if (window._map) window._map.remove();

    const map = L.map("map").setView([lat, lon], 6);
    window._map = map;

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: "&copy; OpenStreetMap"
    }).addTo(map);

    let places = [];
    try {
        places = JSON.parse(el.dataset.places || "[]");
    } catch (e) {
        console.error("Places JSON error:", e);
    }

    const markerLayer = L.layerGroup().addTo(map);

    function renderMarkers(day = "all") {
        markerLayer.clearLayers();
        const filtered = places.filter(p => day === "all" || (p.date && p.date === day));
        const bounds = [];

        filtered.forEach(p => {
            const plat = parseFloat(p.lat);
            const plon = parseFloat(p.lon);
            if (isNaN(plat) || isNaN(plon)) return;

            bounds.push([plat, plon]);
            const marker = L.marker([plat, plon]).addTo(markerLayer);
            marker.bindPopup(`<b>${p.name}</b><br>${p.title || ""}<br>${p.date || ""}<br><a href="https://www.google.com/maps/search/?api=1&query=${plat},${plon}" target="_blank">Open in Google Maps</a>`);
        });

        if (bounds.length) {
            const group = L.latLngBounds(bounds);
            map.fitBounds(group, { padding: [60, 60] });
            if (map.getZoom() > 12) map.setZoom(12);
        } else {
            map.setView([lat, lon], 7);
            L.marker([lat, lon]).addTo(markerLayer).bindPopup("Destination").openPopup();
        }
        map.invalidateSize();
    }

    const filter = document.getElementById("dayFilter");
    if (filter) {
        filter.innerHTML = `<option value="all">All Days</option>`; // reset
        const days = [...new Set(places.map(p => p.date).filter(d => d))].sort();
        days.forEach(d => {
            const opt = document.createElement("option");
            opt.value = d;
            opt.textContent = d;
            filter.appendChild(opt);
        });

        filter.addEventListener("change", () => renderMarkers(filter.value));
    }

    // Always render all markers initially
    renderMarkers("all");
}