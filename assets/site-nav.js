(function () {
  'use strict';

  const nav = document.getElementById('primary-nav');
  if (!nav) return;

  const header = nav.closest('header');
  const toggle = header.querySelector('.nav-toggle');
  const desktop = window.matchMedia('(min-width: 1080px)');
  const canHover = window.matchMedia('(hover: hover) and (pointer: fine)');
  let active = null;
  let openedByHover = false;

  function closeGroup() {
    if (!active) return;
    active.button.setAttribute('aria-expanded', 'false');
    active.panel.hidden = true;
    active = null;
    openedByHover = false;
  }

  function openGroup(group, byHover) {
    closeGroup();
    group.panel.hidden = false;
    group.button.setAttribute('aria-expanded', 'true');
    active = group;
    openedByHover = byHover;
  }

  function setMobileMenu(open) {
    nav.classList.toggle('is-open', open);
    toggle.setAttribute('aria-expanded', String(open));
    if (!open) closeGroup();
  }

  toggle.addEventListener('click', function () {
    setMobileMenu(toggle.getAttribute('aria-expanded') !== 'true');
  });

  for (const item of nav.querySelectorAll('.nav-item')) {
    const button = item.querySelector('.nav-label');
    const panel = document.getElementById(button.getAttribute('aria-controls'));
    const group = { item, button, panel };

    button.addEventListener('click', function () {
      if (active !== group) {
        openGroup(group, false);
      } else if (openedByHover) {
        openedByHover = false;
      } else {
        closeGroup();
      }
    });

    item.addEventListener('pointerenter', function (event) {
      if (event.pointerType !== 'mouse' || !desktop.matches || !canHover.matches) return;
      if (active === group || active?.panel.contains(document.activeElement)) return;
      openGroup(group, true);
    });

    item.addEventListener('pointerleave', function () {
      if (active === group && openedByHover && !item.contains(document.activeElement)) {
        closeGroup();
      }
    });
  }

  nav.addEventListener('focusout', function (event) {
    if (active && active.item.contains(event.target) && !active.item.contains(event.relatedTarget)) {
      closeGroup();
    }
  });

  document.addEventListener('keydown', function (event) {
    if (event.key !== 'Escape') return;
    if (active) {
      const button = active.button;
      const focusWasInside = active.item.contains(document.activeElement);
      closeGroup();
      if (focusWasInside) button.focus();
    } else if (toggle.getAttribute('aria-expanded') === 'true') {
      setMobileMenu(false);
      toggle.focus();
    } else {
      return;
    }
    event.preventDefault();
  });

  nav.addEventListener('click', function (event) {
    if (event.target.closest('a')) setMobileMenu(false);
  });

  document.addEventListener('click', function (event) {
    if (!header.contains(event.target)) setMobileMenu(false);
  });

  desktop.addEventListener('change', function () {
    const focusWasInNav = nav.contains(document.activeElement);
    setMobileMenu(false);
    if (!desktop.matches && focusWasInNav) toggle.focus();
  });
})();
