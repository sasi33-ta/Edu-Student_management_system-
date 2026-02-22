/* EduManage SMS — main.js */

// ── THEME ──────────────────────────────────────────────────────────
function initTheme() {
  const saved = getCookie('theme') || 'dark';
  document.documentElement.setAttribute('data-theme', saved);
  updateThemeBtn(saved);
}

function toggleTheme() {
  const cur  = document.documentElement.getAttribute('data-theme') || 'dark';
  const next = cur === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', next);
  setCookie('theme', next, 365);
  updateThemeBtn(next);
  // sync with server
  fetch('/students/toggle-theme/', {
    method: 'POST',
    headers: { 'X-CSRFToken': getCookie('csrftoken') }
  }).catch(() => {});
}

function updateThemeBtn(theme) {
  const btn = document.getElementById('themeToggle');
  if (btn) btn.textContent = theme === 'dark' ? '☀️' : '🌙';
}

// ── SIDEBAR (mobile) ───────────────────────────────────────────────
function toggleSidebar() {
  document.getElementById('sidebar').classList.toggle('open');
}

// ── PASSWORD VISIBILITY ────────────────────────────────────────────
function togglePwd(id, btn) {
  const inp = document.getElementById(id);
  if (!inp) return;
  const show = inp.type === 'password';
  inp.type = show ? 'text' : 'password';
  btn.textContent = show ? '🙈' : '👁';
}

// ── ALERTS AUTO-DISMISS ────────────────────────────────────────────
function initAlerts() {
  document.querySelectorAll('.alert').forEach(el => {
    setTimeout(() => {
      el.style.transition = 'opacity .5s';
      el.style.opacity = '0';
      setTimeout(() => el.remove(), 500);
    }, 4500);
  });
}

// ── COUNTER ANIMATION ──────────────────────────────────────────────
function animateCounters() {
  document.querySelectorAll('[data-count]').forEach(el => {
    const target = parseInt(el.dataset.count, 10);
    let cur = 0;
    const step = Math.max(1, Math.ceil(target / 35));
    const t = setInterval(() => {
      cur = Math.min(cur + step, target);
      el.textContent = cur;
      if (cur >= target) clearInterval(t);
    }, 28);
  });
}

// ── GRADE BAR ANIMATION ────────────────────────────────────────────
function animateBars() {
  document.querySelectorAll('.gb-fill[data-width]').forEach(el => {
    requestAnimationFrame(() => {
      setTimeout(() => {
        el.style.transition = 'width 1.2s ease';
        el.style.width = el.dataset.width + '%';
      }, 100);
    });
  });
}

// ── PHOTO PREVIEW ──────────────────────────────────────────────────
function initPhotoPreview() {
  const inp = document.querySelector('input[type="file"][accept="image/*"]');
  const preview = document.getElementById('photoPreview');
  const placeholder = document.getElementById('photoPlaceholder');
  if (!inp || !preview) return;

  inp.addEventListener('change', () => {
    const file = inp.files[0];
    if (!file) return;
    if (file.size > 5 * 1024 * 1024) {
      alert('Photo must be under 5MB.'); inp.value = ''; return;
    }
    const reader = new FileReader();
    reader.onload = e => {
      preview.src = e.target.result;
      preview.style.display = 'block';
      if (placeholder) placeholder.style.display = 'none';
    };
    reader.readAsDataURL(file);
  });
}

// ── SEARCH DEBOUNCE ────────────────────────────────────────────────
function initSearchDebounce() {
  const inp = document.getElementById('searchInput');
  if (!inp) return;
  let timer;
  inp.addEventListener('input', () => {
    clearTimeout(timer);
    timer = setTimeout(() => inp.closest('form').submit(), 600);
  });
}

// ── FILL DEMO CREDS ────────────────────────────────────────────────
function fillCreds(u, p) {
  const uf = document.getElementById('loginUsername');
  const pf = document.getElementById('loginPassword');
  if (uf) uf.value = u;
  if (pf) pf.value = p;
}

// ── COOKIES ────────────────────────────────────────────────────────
function getCookie(name) {
  const val = `; ${document.cookie}`;
  const parts = val.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
  return null;
}

function setCookie(name, value, days) {
  const d = new Date();
  d.setTime(d.getTime() + days * 86400000);
  document.cookie = `${name}=${value};expires=${d.toUTCString()};path=/`;
}

// ── INIT ───────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initAlerts();
  animateCounters();
  animateBars();
  initPhotoPreview();
  initSearchDebounce();
});
