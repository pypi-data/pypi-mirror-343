
function loadES5() {
  var el = document.createElement('script');
  el.src = '/lcn_static/frontend_es5/entrypoint.b24f9f88d795c2da.js';
  document.body.appendChild(el);
}
if (/.*Version\/(?:11|12)(?:\.\d+)*.*Safari\//.test(navigator.userAgent)) {
    loadES5();
} else {
  try {
    new Function("import('/lcn_static/frontend_latest/entrypoint.bc518ae11573493f.js')")();
  } catch (err) {
    loadES5();
  }
}
  