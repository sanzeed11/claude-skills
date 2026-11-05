/* fill.js — puts the DATA block at the top of a social animation into its markup (same idea as 08_SOCIAL_MEDIA/Editable_Templates/fill.js).
   [data-text="key"]      -> textContent
   [data-src="key"]       -> img.src (+ DATA[key + "_focal"] -> object-position)
   [data-headline="key"]  -> one <span class="w"> per word (the type-in animates these); the last word gets .lit or .dim
                            when DATA.lit_last_word / DATA.dim_last_word is true
   Runs at parse time (end of body), before the load event, so capture_frames.js sees the finished page. */
(function () {
  var D = window.DATA || {};
  document.querySelectorAll('[data-text]').forEach(function (el) { var k = el.getAttribute('data-text'); if (k in D) el.textContent = D[k]; });
  document.querySelectorAll('[data-src]').forEach(function (el) { var k = el.getAttribute('data-src'); if (D[k]) el.src = D[k]; if (D[k + '_focal']) el.style.objectPosition = D[k + '_focal']; });
  document.querySelectorAll('[data-headline]').forEach(function (el) {
    var k = el.getAttribute('data-headline'), words = String(D[k] || '').split(/\s+/).filter(Boolean);
    el.innerHTML = words.map(function (w, i) {
      var last = i === words.length - 1, cls = 'w' + (last && D.lit_last_word ? ' lit' : '') + (last && D.dim_last_word ? ' dim' : '');
      return '<span class="' + cls + '">' + w.replace(/&/g, '&amp;').replace(/</g, '&lt;') + '</span>';
    }).join(' ');
  });
})();
