// Server-side helper to send admin notifications.
// Usage: from any server-side code call sendAdminNotification(eventType, data)
// This helper will call the Netlify function endpoint if available, or attempt
// to send directly via Resend (server environment) when RESEND_API_KEY is present.

const fetch = global.fetch || require('node-fetch');

async function sendAdminNotification(eventType, data) {
  const payload = { eventType, data };

  // Prefer direct provider if API key is available (server environment)
  if (process.env.RESEND_API_KEY) {
    try {
      const res = await fetch('https://api.resend.com/emails', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${process.env.RESEND_API_KEY}`,
        },
        body: JSON.stringify({
          from: process.env.EMAIL_FROM || `no-reply@${new URL(process.env.APP_BASE_URL || 'https://example.com').hostname}`,
          to: process.env.ADMIN_NOTIFICATION_EMAIL,
          subject: payload.eventType || 'Client action required in portal',
          html: `<pre>${JSON.stringify(payload, null, 2)}</pre>`,
        }),
      });
      if (!res.ok) {
        const text = await res.text();
        console.error('adminNotifications: resend send failed', res.status, text);
      }
      return;
    } catch (err) {
      console.error('adminNotifications: resend exception', err);
      return;
    }
  }

  // If no direct key, try Netlify function local path
  try {
    const fnUrl = (process.env.FUNCTIONS_BASE_URL || '') + '/.netlify/functions/admin-notify';
    // If FUNCTIONS_BASE_URL not set, attempt relative call which will work on server
    const res = await fetch(fnUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    if (!res.ok) {
      const text = await res.text();
      console.error('adminNotifications: function call failed', res.status, text);
    }
  } catch (err) {
    console.error('adminNotifications: failed to call function', err);
  }
}

module.exports = { sendAdminNotification };
