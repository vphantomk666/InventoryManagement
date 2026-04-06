// Footer modal functions
function showAboutUs() {
    document.getElementById("aboutModal").classList.add("active");
}

function closeAboutUs() {
    document.getElementById("aboutModal").classList.remove("active");
}

function showTerms() {
    document.getElementById("termsModal").classList.add("active");
}

function closeTerms() {
    document.getElementById("termsModal").classList.remove("active");
}

function showPrivacy() {
    document.getElementById("privacyModal").classList.add("active");
}

function closePrivacy() {
    document.getElementById("privacyModal").classList.remove("active");
}

// Close modals when clicking outside
document.getElementById("aboutModal").addEventListener("click", (e) => {
    if (e.target.id === "aboutModal") closeAboutUs();
});

document.getElementById("termsModal").addEventListener("click", (e) => {
    if (e.target.id === "termsModal") closeTerms();
});

document.getElementById("privacyModal").addEventListener("click", (e) => {
    if (e.target.id === "privacyModal") closePrivacy();
});
