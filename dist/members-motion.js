(() => {
  const buttons = [...document.querySelectorAll('[data-motion]')];
  const status = document.querySelector('#motion-status');
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const play = document.querySelector('#motion-play');
  let timer;
  function clearDemo() {
    clearTimeout(timer);
    document.querySelectorAll('.motion-demo').forEach(card => card.classList.remove('motion-demo'));
  }
  function select(mode) {
    clearDemo();
    document.body.dataset.memberMotion = mode;
    buttons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.motion === mode)));
    status.textContent = ({original:'A：元の動き', bold:'B：大胆な動き', adopted:'採用版：元の動き＋光'}[mode]) + (reduced.matches ? '（端末設定により動きを抑制）' : '');
    const url = new URL(location.href);
    url.searchParams.set('motion', mode);
    history.replaceState(null, '', url);
  }
  buttons.forEach(button => button.addEventListener('click', () => select(button.dataset.motion)));
  play.addEventListener('click', () => {
    clearDemo();
    const section = location.hash === '#staff' ? '#staff' : '#players';
    const card = document.querySelector(`${section} .member-card`);
    card.scrollIntoView({block: 'center', behavior: reduced.matches ? 'instant' : 'smooth'});
    // Delay the preview briefly to let the selected card enter the viewport.
    timer = setTimeout(() => {
      card.classList.add('motion-demo');
      timer = setTimeout(clearDemo, 2000);
    }, reduced.matches ? 0 : 400);
  });
  reduced.addEventListener('change', () => select(document.body.dataset.memberMotion));
  const requested = new URLSearchParams(location.search).get('motion');
  select(['bold', 'original', 'adopted'].includes(requested) ? requested : 'adopted');
})();
