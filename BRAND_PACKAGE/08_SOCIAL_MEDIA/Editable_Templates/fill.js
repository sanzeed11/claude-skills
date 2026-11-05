/* fill.js — puts the values of the DATA block (top of each template) into the page.
   data-text="key"      → text
   data-headline="key"  → headline; the last word is set gold when DATA.lit_last_word is true
   data-src="key"       → image src (also reads DATA.key_focal = "50% 40%" for the crop point)
   data-show="key"      → element is hidden when DATA.key is empty/false
   Re-apply with other values from render.js:  --js "apply({headline:'…', image:'…'})"  */
function apply(d) {
  window.DATA = Object.assign(window.DATA || {}, d || {}); d = window.DATA;
  document.querySelectorAll('[data-text]').forEach(function (el) { var k = el.dataset.text; if (d[k] != null) el.textContent = d[k]; });
  document.querySelectorAll('[data-headline]').forEach(function (el) {
    var s = d[el.dataset.headline]; if (s == null) return; el.textContent = '';
    var m = /^([\s\S]*?)(\S+)$/.exec(s.trim());
    if (!d.lit_last_word || !m) { el.textContent = s; return; }
    el.append(m[1]); var sp = document.createElement('span'); sp.className = 'lit'; sp.textContent = m[2]; el.append(sp);
  });
  document.querySelectorAll('[data-src]').forEach(function (el) {
    var k = el.dataset.src; if (d[k]) el.src = d[k];
    if (d[k + '_focal']) el.style.objectPosition = d[k + '_focal'];
  });
  document.querySelectorAll('[data-show]').forEach(function (el) { el.hidden = !d[el.dataset.show]; });
  return Promise.all(Array.from(document.images).map(function (im) { return im.decode().catch(function () {}); })).then(function () { return true; });
}
apply({});
