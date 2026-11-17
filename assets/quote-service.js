/* Keep service details in the existing message field understood by the forms gateway. */
(function () {
  'use strict';
  var form = document.getElementById('quoteForm');
  if (!form) return;
  var service = document.getElementById('service');
  var message = document.getElementById('message');
  if (!service || !message) return;
  var requested = new URLSearchParams(window.location.search).get('service') || '';
  if (/painting|decorating/i.test(requested)) service.selectedIndex = 1;
  else if (/landlord|letting/i.test(requested)) service.selectedIndex = 2;
  else if (/garden|grounds|lawn|hedge/i.test(requested)) service.selectedIndex = 3;
  else if (requested) service.selectedIndex = 4;
  Array.prototype.some.call(service.options, function (option, index) {
    if (option.value.toLowerCase() !== requested.toLowerCase()) return false;
    service.selectedIndex = index;
    return true;
  });
  var hint = document.getElementById('winter-quote-hint');
  var winterHints = {
    'Salt Spreading & Gritting': 'Include your postcode, the driveway, paths or steps you need gritted, and whether you need one visit or planned cover.',
    'Winter Property Maintenance': 'Include your postcode, the winter jobs you need at home and any access details.',
    'Blocked Drains & Drainage': 'Tell us where water is pooling, where the suspected blockage is and whether the problem keeps returning.',
    'Window & Door Resealing': 'Tell us how many windows or doors are affected and where you notice draughts or rain getting in.'
  };
  if (hint) {
    var updateHint = function () {
      var instructions = winterHints[service.value] || '';
      hint.textContent = instructions;
      hint.hidden = !instructions;
      if (instructions) message.setAttribute('aria-describedby', hint.id);
      else message.removeAttribute('aria-describedby');
    };
    service.addEventListener('change', updateHint);
    updateHint();
  }
  form.addEventListener('submit', function () {
    if (!service.value) return;
    var prefix = 'Service: ' + service.value + '\n';
    if (message.value.indexOf(prefix) !== 0) {
      message.value = prefix + message.value.replace(/^Service: [^\n]*\n/, '');
    }
  });
})();
