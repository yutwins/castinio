const menuButton = document.querySelector('.menu-button');
const navigation = document.querySelector('#navigation');
function closeMenu() { navigation?.classList.remove('is-open'); menuButton?.setAttribute('aria-expanded', 'false'); if (menuButton) menuButton.textContent = 'メニュー'; }
menuButton?.addEventListener('click', () => { const open = menuButton.getAttribute('aria-expanded') !== 'true'; menuButton.setAttribute('aria-expanded', String(open)); navigation.classList.toggle('is-open', open); menuButton.textContent = open ? '閉じる' : 'メニュー'; });
document.addEventListener('keydown', event => { if(event.key === 'Escape' && menuButton?.getAttribute('aria-expanded') === 'true'){closeMenu();menuButton.focus();} });
navigation?.addEventListener('click', event => { if (event.target.closest('a')) closeMenu(); });
window.matchMedia('(min-width: 801px)').addEventListener('change', event => { if(event.matches) closeMenu(); });
const heroPhotos = document.querySelectorAll('.hero-photo');
if (heroPhotos.length > 1 && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
  let heroIndex = 0;
  setInterval(() => {
    heroPhotos[heroIndex].classList.remove('is-active');
    heroIndex = (heroIndex + 1) % heroPhotos.length;
    heroPhotos[heroIndex].classList.add('is-active');
  }, 6000);
}
const contactForm = document.querySelector('#contact-form');
if (contactForm) {
  const type = new URLSearchParams(location.search).get('type');
  if (['join','match','other'].includes(type)) contactForm.elements.type.value = type;
  contactForm.addEventListener('submit', async event => {
    event.preventDefault();
    const result = document.querySelector('#form-result');
    const submitButton = contactForm.querySelector('button[type="submit"]');
    const turnstileToken = contactForm.elements['cf-turnstile-response']?.value || '';

    result.hidden = false;
    result.textContent = '送信中…';
    submitButton.disabled = true;

    try {
      const response = await fetch('/api/contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          type: contactForm.elements.type.value,
          name: contactForm.elements.name.value,
          email: contactForm.elements.email.value,
          message: contactForm.elements.message.value,
          turnstileToken,
        }),
      });
      const data = await response.json().catch(() => ({}));
      if (response.ok && data.ok) {
        result.textContent = 'お問い合わせを受け付けました。ありがとうございます。';
        contactForm.reset();
        window.turnstile?.reset();
      } else {
        result.textContent = '送信に失敗しました。お手数ですがInstagramのDMからご連絡ください。';
      }
    } catch (error) {
      result.textContent = '通信エラーが発生しました。お手数ですがInstagramのDMからご連絡ください。';
    } finally {
      submitButton.disabled = false;
      result.focus();
    }
  });
}
