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
  form.addEventListener('submit', function () {
    if (!service.value) return;
    var prefix = 'Service: ' + service.value + '\n';
    if (message.value.indexOf(prefix) !== 0) {
      message.value = prefix + message.value.replace(/^Service: [^\n]*\n/, '');
    }
  });
})();
