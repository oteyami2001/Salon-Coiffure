// Firm Portfolio Site — header, mobile menu, hero slideshow
(function () {
  var header = document.querySelector('.site-header');
  var isHome = document.body.classList.contains('home');
  function onScroll() {
    if (!header || !isHome) return;
    header.classList.toggle('is-solid', window.scrollY > 80);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  var toggle = document.querySelector('.menu-toggle');
  var nav = document.querySelector('.nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      if (isHome) header.classList.toggle('is-solid', open || window.scrollY > 80);
    });
  }

  var slides = Array.prototype.slice.call(document.querySelectorAll('.hero .slide'));
  var dots = Array.prototype.slice.call(document.querySelectorAll('.hero-dots button'));
  var caption = document.querySelector('.hero-caption');
  if (slides.length > 1) {
    var i = 0, timer;
    var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    function show(n) {
      slides[i].classList.remove('is-active'); if (dots[i]) dots[i].classList.remove('is-active');
      i = (n + slides.length) % slides.length;
      slides[i].classList.add('is-active'); if (dots[i]) dots[i].classList.add('is-active');
      if (caption) caption.textContent = slides[i].getAttribute('data-caption') || '';
    }
    function start() { if (!reduce) timer = setInterval(function () { show(i + 1); }, 6000); }
    dots.forEach(function (d, n) {
      d.addEventListener('click', function () { clearInterval(timer); show(n); start(); });
    });
    start();
  }

  // Formulaire de contact -> message WhatsApp pré-rempli
  var form = document.querySelector('form[data-whatsapp]');
  if (form) {
    form.addEventListener('submit', function (ev) {
      ev.preventDefault();
      var lines = [form.getAttribute('data-intro') || ''];
      Array.prototype.forEach.call(form.elements, function (el) {
        if (el.name && el.value.trim()) lines.push(el.name + ' : ' + el.value.trim());
      });
      var url = form.getAttribute('data-whatsapp') + '?text=' + encodeURIComponent(lines.filter(Boolean).join('\n'));
      window.open(url, '_blank', 'noopener');
    });
  }
})();
