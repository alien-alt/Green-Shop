/* =====================================================
   Green Leaf — Main JavaScript
   Только базовая логика: бургер-меню + переключение паролей
   ===================================================== */

document.addEventListener('DOMContentLoaded', function() {
  initMobileMenu();
  initPasswordToggles();
  initOptionButtons();
});

// =====================================================
// Mobile Menu
// =====================================================
function initMobileMenu() {
  const burgerBtn = document.querySelector('.burger-btn');
  const mobileMenu = document.querySelector('.mobile-menu');
  
  if (!burgerBtn || !mobileMenu) return;
  
  burgerBtn.addEventListener('click', function() {
    this.classList.toggle('active');
    mobileMenu.classList.toggle('active');
    document.body.style.overflow = mobileMenu.classList.contains('active') ? 'hidden' : '';
  });
  
  mobileMenu.querySelectorAll('a').forEach(function(link) {
    link.addEventListener('click', function() {
      burgerBtn.classList.remove('active');
      mobileMenu.classList.remove('active');
      document.body.style.overflow = '';
    });
  });
}

// =====================================================
// Password Toggle (для login.html и register.html)
// =====================================================
function initPasswordToggles() {
  document.querySelectorAll('.password-toggle').forEach(function(toggle) {
    toggle.addEventListener('click', function() {
      var input = this.parentElement.querySelector('input');
      var type = input.getAttribute('type') === 'password' ? 'text' : 'password';
      input.setAttribute('type', type);
      
      var svg = this.querySelector('svg');
      if (type === 'text') {
        svg.innerHTML = '<path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/>';
      } else {
        svg.innerHTML = '<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/>';
      }
    });
  });
}

// =====================================================
// Option Buttons (для product.html — переключение опций)
// =====================================================
function initOptionButtons() {
  document.querySelectorAll('.product-option-values').forEach(function(group) {
    group.querySelectorAll('.option-btn').forEach(function(btn) {
      btn.addEventListener('click', function() {
        group.querySelectorAll('.option-btn').forEach(function(b) {
          b.classList.remove('active');
        });
        this.classList.add('active');
      });
    });
  });
}


// My caode
document.addEventListener("DOMContentLoaded", function () {
  const addToCartBtn = document.querySelector('[value="add_item"]');

  if (addToCartBtn) {
    addToCartBtn.addEventListener("click", async function () {
      const slug = this.dataset.slug;

      const response = await fetch("/cart/add-item/", {  // укажи свой url
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({
          product_slug: slug,
          action: "add_item",
        }),
      });

      const data = await response.json();

      if (data.success) {
        // меняем кнопку на "В корзине" без перезагрузки
        addToCartBtn.textContent = "В корзине";
        addToCartBtn.classList.remove("btn-primary");
        addToCartBtn.classList.add("btn-in");
        addToCartBtn.disabled = true;
      }
    });
  }

  // хелпер для получения CSRF токена
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      for (const cookie of document.cookie.split(";")) {
        const c = cookie.trim();
        if (c.startsWith(name + "=")) {
          cookieValue = decodeURIComponent(c.slice(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
});


document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".cart-item-remove").forEach(function (btn) {
    btn.addEventListener("click", async function () {
      const slug = this.dataset.slug;
      const cartItem = this.closest(".cart-item");

      const response = await fetch("/cart/remove-item/", {  // замени на свой URL
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({
          product_slug: slug,
        }),
      });

      const data = await response.json();

      if (data.success) {
        cartItem.remove();  // убираем элемент из DOM без перезагрузки
      }
    });
  });
});

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    for (const cookie of document.cookie.split(";")) {
      const c = cookie.trim();
      if (c.startsWith(name + "=")) {
        cookieValue = decodeURIComponent(c.slice(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
