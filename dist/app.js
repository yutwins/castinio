const menuButton = document.querySelector('.menu-button');
const navigation = document.querySelector('#navigation');
function closeMenu() { navigation?.classList.remove('is-open'); menuButton?.setAttribute('aria-expanded', 'false'); if (menuButton) menuButton.textContent = 'メニュー'; }
menuButton?.addEventListener('click', () => { const open = menuButton.getAttribute('aria-expanded') !== 'true'; menuButton.setAttribute('aria-expanded', String(open)); navigation.classList.toggle('is-open', open); menuButton.textContent = open ? '閉じる' : 'メニュー'; });
document.addEventListener('keydown', event => { if(event.key === 'Escape' && menuButton?.getAttribute('aria-expanded') === 'true'){closeMenu();menuButton.focus();} });
navigation?.addEventListener('click', event => { if (event.target.closest('a')) closeMenu(); });
window.matchMedia('(min-width: 801px)').addEventListener('change', event => { if(event.matches) closeMenu(); });
const contactForm = document.querySelector('#contact-form');
if (contactForm) {
  const type = new URLSearchParams(location.search).get('type');
  if (['join','match','other'].includes(type)) contactForm.elements.type.value = type;
  contactForm.addEventListener('submit', event => {
    event.preventDefault();
    const result = document.querySelector('#form-result');
    result.hidden = false;
    result.textContent = '入力内容を確認しました。このフォームは画面確認用です。メッセージは送信・保存されていません。実際のご連絡はInstagramのDMをご利用ください。';
    result.focus();
  });
}
