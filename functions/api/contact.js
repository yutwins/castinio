function jsonResponse(body, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}

const VALID_TYPES = ['join', 'match', 'other'];
const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export async function onRequestPost({ request, env }) {
  let data;
  try {
    data = await request.json();
  } catch {
    return jsonResponse({ ok: false, error: 'invalid_request' }, 400);
  }

  const type = typeof data.type === 'string' ? data.type : '';
  const name = typeof data.name === 'string' ? data.name.trim() : '';
  const email = typeof data.email === 'string' ? data.email.trim() : '';
  const message = typeof data.message === 'string' ? data.message.trim() : '';
  const turnstileToken = typeof data.turnstileToken === 'string' ? data.turnstileToken : '';

  if (!VALID_TYPES.includes(type)) {
    return jsonResponse({ ok: false, error: 'invalid_type' }, 400);
  }
  if (!name || name.length > 100) {
    return jsonResponse({ ok: false, error: 'invalid_name' }, 400);
  }
  if (!email || email.length > 254 || !EMAIL_PATTERN.test(email)) {
    return jsonResponse({ ok: false, error: 'invalid_email' }, 400);
  }
  if (!message || message.length > 5000) {
    return jsonResponse({ ok: false, error: 'invalid_message' }, 400);
  }
  if (!turnstileToken) {
    return jsonResponse({ ok: false, error: 'missing_turnstile' }, 400);
  }

  const verifyResponse = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      secret: env.TURNSTILE_SECRET_KEY,
      response: turnstileToken,
      remoteip: request.headers.get('CF-Connecting-IP') || undefined,
    }),
  });
  const verifyResult = await verifyResponse.json();
  if (!verifyResult.success) {
    return jsonResponse({ ok: false, error: 'turnstile_failed' }, 400);
  }

  if (!env.CONTACT_SUBMISSIONS) {
    return jsonResponse({ ok: false, error: 'storage_not_configured' }, 500);
  }

  const id = `${Date.now()}-${crypto.randomUUID()}`;
  const record = { type, name, email, message, receivedAt: new Date().toISOString() };
  await env.CONTACT_SUBMISSIONS.put(id, JSON.stringify(record));

  return jsonResponse({ ok: true });
}
