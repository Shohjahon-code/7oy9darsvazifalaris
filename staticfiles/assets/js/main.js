/* ===== ShopStyle – Main JS ===== */

// ── Cart (localStorage) ─────────────────────────────────────────────────────
function getCart() {
    return JSON.parse(localStorage.getItem('cart') || '[]');
}
function saveCart(cart) {
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartBadge();
}
function updateCartBadge() {
    const cart = getCart();
    const total = cart.reduce((s, i) => s + i.qty, 0);
    document.querySelectorAll('.cart-badge').forEach(el => {
        el.textContent = total;
        el.style.display = total > 0 ? 'flex' : 'none';
    });
}
function addToCart(id, name, price, image) {
    const cart = getCart();
    const idx = cart.findIndex(i => i.id === id);
    if (idx > -1) {
        cart[idx].qty += 1;
    } else {
        cart.push({ id, name, price, image, qty: 1 });
    }
    saveCart(cart);
    showToast(`"${name}" savatga qo'shildi!`);
}

// ── Toast ───────────────────────────────────────────────────────────────────
function showToast(msg) {
    let t = document.getElementById('toast');
    if (!t) {
        t = document.createElement('div');
        t.id = 'toast';
        t.style.cssText = `
            position:fixed; bottom:24px; right:24px; z-index:9999;
            background:linear-gradient(135deg,#6c63ff,#a78bfa);
            color:#fff; padding:14px 22px; border-radius:12px;
            font-weight:600; font-size:14px;
            box-shadow:0 8px 30px rgba(108,99,255,0.4);
            transform:translateY(80px); opacity:0;
            transition:all 0.35s cubic-bezier(.34,1.56,.64,1);
            max-width:320px;
        `;
        document.body.appendChild(t);
    }
    t.textContent = '🛍️  ' + msg;
    setTimeout(() => { t.style.transform = 'translateY(0)'; t.style.opacity = '1'; }, 10);
    setTimeout(() => { t.style.transform = 'translateY(80px)'; t.style.opacity = '0'; }, 2800);
}

// ── Navbar scroll ───────────────────────────────────────────────────────────
window.addEventListener('scroll', () => {
    const nav = document.getElementById('main-nav');
    if (!nav) return;
    if (window.scrollY > 50) {
        nav.classList.add('scrolled');
        nav.style.background = 'rgba(15,15,26,0.97)';
        nav.style.boxShadow = '0 4px 30px rgba(0,0,0,0.4)';
    } else {
        nav.classList.remove('scrolled');
        nav.style.background = 'rgba(15,15,26,0.8)';
        nav.style.boxShadow = 'none';
    }
});

// ── Mobile menu ─────────────────────────────────────────────────────────────
function toggleMobileMenu() {
    const m = document.getElementById('mobile-menu');
    if (m) m.classList.toggle('hidden');
}

// ── Product image gallery ────────────────────────────────────────────────────
function switchMainImage(src, el) {
    const main = document.getElementById('main-img');
    if (main) {
        main.style.opacity = '0';
        setTimeout(() => { main.src = src; main.style.opacity = '1'; }, 180);
    }
    document.querySelectorAll('.thumb-item').forEach(t => t.classList.remove('selected'));
    if (el) el.classList.add('selected');
}

// ── Qty controls ─────────────────────────────────────────────────────────────
function changeQty(delta) {
    const el = document.getElementById('qty-val');
    if (el) el.textContent = Math.max(1, parseInt(el.textContent) + delta);
}

// Init
document.addEventListener('DOMContentLoaded', updateCartBadge);
