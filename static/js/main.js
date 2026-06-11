// // EcoChain - Main JS

// Mobile nav toggle
const navToggle = document.getElementById('navToggle');
const mobileMenu = document.getElementById('mobileMenu');
if (navToggle && mobileMenu) {
    navToggle.addEventListener('click', () => {
        mobileMenu.classList.toggle('open');
    });
}

// Auto-dismiss messages after 5 seconds
document.querySelectorAll('.message').forEach(msg => {
    setTimeout(() => { msg.remove(); }, 5000);
});

// Intersection observer for fade-in animations
const animateEls = document.querySelectorAll('.step-card, .plastic-card, .dashboard-card');
const fadeIn = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('fade-in');
        }
    });
});
animateEls.forEach(el => fadeIn.observe(el));
// --- NEW CODE TO POPULATE DROPDOWNS ---
document.addEventListener("DOMContentLoaded", () => {
    // 1. Data arrays matching database integer IDs exactly
    const plasticTypes = [
        { id: 1, name: "PET (Type 1) - Water Bottles" },
        { id: 2, name: "HDPE (Type 2) - Milk Jugs" },
        { id: 3, name: "PVC (Type 3) - Pipes" },
        { id: 4, name: "LDPE (Type 4) - Plastic Bags" },
        { id: 5, name: "PP (Type 5) - Bottle Caps" },
        { id: 6, name: "PS (Type 6) - Foam Containers" }
    ];

    const collectionCenters = [
        { id: 1, name: "Downtown Recycling Hub" },
        { id: 2, name: "Northside Eco Center" },
        { id: 3, name: "East Green Point Drop-off" },
        { id: 4, name: "Westside Waste Facility" }
    ];

    // 2. Select elements by their accurate template order
    const selectElements = document.querySelectorAll("select");
    
    if (selectElements.length >= 2) {
        const plasticDropdown = selectElements[0]; // First dropdown element
        const centerDropdown = selectElements[1];  // Second dropdown element

        // Reset the default placeholders cleanly
        plasticDropdown.innerHTML = '<option value="">-- Select Type --</option>';
        centerDropdown.innerHTML = '<option value="">-- Select Center --</option>';

        // 3. Inject numeric ID choices into Plastic Type
        plasticTypes.forEach(type => {
            const option = document.createElement("option");
            option.value = type.id; 
            option.textContent = type.name;
            plasticDropdown.appendChild(option);
        });

        // 4. Inject numeric ID choices into Collection Center
        collectionCenters.forEach(center => {
            const option = document.createElement("option");
            option.value = center.id; 
            option.textContent = center.name;
            centerDropdown.appendChild(option);
        });
    }
});