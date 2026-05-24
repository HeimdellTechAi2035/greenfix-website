/* Netlify Function: admin-notify
   Receives POST requests with JSON { eventType, data }
   Sends an admin notification email using Resend (if configured).
   Environment variables used (set in Netlify):
     RESEND_API_KEY - API key for Resend (optional)
     EMAIL_FROM - the 'from' email address (e.g. no-reply@yourdomain.com)
     ADMIN_NOTIFICATION_EMAIL - address to receive alerts
     APP_BASE_URL - public URL of the app
*/

const RESEND_API = 'https://api.resend.com/emails';

exports.handler = async function (event, context) {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method Not Allowed' };
  }

  let body;
  try {
    body = JSON.parse(event.body || '{}');
  } catch (err) {
    return { statusCode: 400, body: 'Invalid JSON' };
  }

  const { eventType, data } = body;
  const adminEmail = process.env.ADMIN_NOTIFICATION_EMAIL;
  const appBase = process.env.APP_BASE_URL || '';

  if (!adminEmail) {
    console.error('ADMIN_NOTIFICATION_EMAIL not configured');
    return { statusCode: 500, body: 'Server misconfigured' };
  }

  // Build subject and HTML body
  const subject = buildSubject(eventType, data);
  const html = buildHtml(eventType, data, appBase);

  // Try to send using Resend if key provided
  const resendKey = process.env.RESEND_API_KEY;
  const from = process.env.EMAIL_FROM || `no-reply@${new URL(appBase || 'https://example.com').hostname}`;

  if (resendKey) {
    try {
      const res = await fetch(RESEND_API, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${resendKey}`,
        },
        body: JSON.stringify({
          from,
          to: adminEmail,
          subject,
          html,
        }),
      });

      if (!res.ok) {
        const text = await res.text();
        console.error('Resend error', res.status, text);
        // don't block primary action — return 202 so callers know we queued (but logged failure)
        return { statusCode: 202, body: 'email-failed' };
      }

      return { statusCode: 200, body: 'email-sent' };
    } catch (err) {
      console.error('Resend send failed', err);
      return { statusCode: 202, body: 'email-failed' };
    }
  }

  // If no provider configured, log and return 202
  console.warn('No email provider configured (RESEND_API_KEY not set). Email not sent.');
  console.log('Would send to', adminEmail, 'subject', subject);
  return { statusCode: 202, body: 'no-provider' };
};

function buildSubject(eventType, data) {
  switch (eventType) {
    case 'job_request':
      return 'New Greenfix job request submitted';
    case 'client_message':
      return 'New client message received';
    case 'date_accepted':
      return 'Client accepted proposed job date';
    case 'completion_dispute':
      return 'Client disputed job completion';
    default:
      return 'Client action required in portal';
  }
}

function escapeHtml(s) {
  if (!s) return '';
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/\"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function buildHtml(eventType, data, appBase) {
  const client = data.client || {};
  const job = data.job || {};
  const message = data.message || '';

  const parts = [];
  parts.push(`<p><strong>Event:</strong> ${escapeHtml(eventType)}</p>`);
  if (client.company) parts.push(`<p><strong>Company:</strong> ${escapeHtml(client.company)}</p>`);
  if (client.name) parts.push(`<p><strong>Contact:</strong> ${escapeHtml(client.name)}</p>`);
  if (client.email) parts.push(`<p><strong>Contact email:</strong> ${escapeHtml(client.email)}</p>`);
  if (job.title) parts.push(`<p><strong>Job:</strong> ${escapeHtml(job.title)}</p>`);
  if (job.service_type) parts.push(`<p><strong>Service type:</strong> ${escapeHtml(job.service_type)}</p>`);
  if (job.property_address) parts.push(`<p><strong>Property:</strong> ${escapeHtml(job.property_address)}</p>`);
  if (job.id) parts.push(`<p><strong>Job ref:</strong> ${escapeHtml(job.id)}</p>`);
  if (data.submitted_at) parts.push(`<p><strong>Submitted:</strong> ${escapeHtml(data.submitted_at)}</p>`);
  if (message) parts.push(`<hr/><p><strong>Message:</strong><br/>${escapeHtml(message)}</p>`);
  if (appBase && job.id) {
    const href = `${appBase.replace(/\/$/, '')}/admin/jobs/${encodeURIComponent(job.id)}`;
    parts.push(`<p><a href="${escapeHtml(href)}">Open job in admin dashboard</a></p>`);
  }

  return `<!doctype html><html><body>${parts.join('\n')}</body></html>`;
}
