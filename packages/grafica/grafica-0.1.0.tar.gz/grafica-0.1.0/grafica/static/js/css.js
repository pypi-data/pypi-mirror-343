"use strict";

_ready(() => {
  const hr = 'h1 + hr, h2 + hr, h3 + hr';

  document.querySelectorAll(hr).forEach(
    el => el.classList.add('red')
  );

  document.querySelectorAll('.admonition').forEach(
    el => el.classList.add('alert')
  );

  document.querySelectorAll('.hint').forEach(
    el => el.classList.add('alert-info')
  );

  document.querySelectorAll('.note').forEach(
    el => el.classList.add('alert-info')
  );

  document.querySelectorAll('.seealso').forEach(
    el => el.classList.add('alert-info')
  );
});
