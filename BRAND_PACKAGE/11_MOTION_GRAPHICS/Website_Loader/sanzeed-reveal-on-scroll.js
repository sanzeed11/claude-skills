/* SANZEED — reveal on scroll. Pairs with sanzeed-reveal-on-scroll.css. 1 KB, no dependencies.
   Adds .is-in to every [data-reveal] element once it enters the viewport (top edge crosses 88 % of the viewport height),
   reading an optional data-reveal-delay="ms". Honours prefers-reduced-motion by revealing everything at once. */
(function () {
  var html = document.documentElement; html.classList.remove('no-js');
  var els = [].slice.call(document.querySelectorAll('[data-reveal]'));
  if (!els.length) return;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduce || !('IntersectionObserver' in window)) { els.forEach(function (el) { el.classList.add('is-in'); }); return; }
  els.forEach(function (el) { var d = el.getAttribute('data-reveal-delay'); if (d) el.style.setProperty('--reveal-delay', d); });
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); } });
  }, { rootMargin: '0px 0px -12% 0px', threshold: 0 });
  els.forEach(function (el) { io.observe(el); });
})();
