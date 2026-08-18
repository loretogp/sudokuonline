// Cookie consent banner behavior (Google Consent Mode v2). The "consent
// default" gtag() call that blocks storage until the user decides lives
// inline in <head> on every page (must run before gtag.js/adsbygoogle.js
// load) — this module only handles the banner UI and the consent update.

const STORAGE_KEY = "cookie_consent_v1";

function applyConsent(granted) {
  gtag("consent", "update", {
    ad_storage: granted ? "granted" : "denied",
    ad_user_data: granted ? "granted" : "denied",
    ad_personalization: granted ? "granted" : "denied",
    analytics_storage: granted ? "granted" : "denied",
  });
}

function showBanner() {
  const banner = document.getElementById("cookie-banner");
  if (banner) banner.hidden = false;
}

function hideBanner() {
  const banner = document.getElementById("cookie-banner");
  if (banner) banner.hidden = true;
}

const saved = localStorage.getItem(STORAGE_KEY);
if (saved === "granted") {
  applyConsent(true);
} else if (saved === "denied") {
  applyConsent(false);
} else {
  showBanner();
}

document.getElementById("cookie-accept")?.addEventListener("click", () => {
  localStorage.setItem(STORAGE_KEY, "granted");
  applyConsent(true);
  hideBanner();
});

document.getElementById("cookie-reject")?.addEventListener("click", () => {
  localStorage.setItem(STORAGE_KEY, "denied");
  applyConsent(false);
  hideBanner();
});

// Reopens the banner so a returning visitor can change their choice.
document.getElementById("cookie-settings-link")?.addEventListener("click", (event) => {
  event.preventDefault();
  showBanner();
});
