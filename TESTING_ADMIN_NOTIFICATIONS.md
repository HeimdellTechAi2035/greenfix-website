How to test Admin Notification emails locally and after deploy

Prerequisites
- Set environment variables from `.env.example`.
- For local function testing install `netlify-cli` (`npm i -g netlify-cli`) and run `netlify dev` from the project root.

Local testing (Netlify dev)
1. Start Netlify dev: `netlify dev` (this will serve `/.netlify/functions/admin-notify`).
2. Send a test POST via curl:

```bash
curl -X POST http://localhost:8888/.netlify/functions/admin-notify \
  -H "Content-Type: application/json" \
  -d '{"eventType":"job_request","data":{"client":{"company":"ACME" , "name":"Joe"},"job":{"id":"JOB123","title":"Lawncare"},"message":"Test job"}}'
```

3. Inspect the function logs. If `RESEND_API_KEY` is set the function will attempt to send via Resend; otherwise it will log the intended email.

Direct function test (deployed)
1. Deploy to Netlify. Ensure Netlify environment variables include at minimum:
   - `ADMIN_NOTIFICATION_EMAIL` = admin@greenfixexterior-care.co.uk
  - `APP_BASE_URL` = https://portal.greenfixexterior-care.co.uk
   - `RESEND_API_KEY` (if using Resend)
   - `EMAIL_FROM`
2. Call the function URL: `https://<your-site>/.netlify/functions/admin-notify` with the same curl payload as above.

Integration notes
- You must invoke the function after a database write completes. Wherever your server-side job creation, message creation, date acceptance, or completion/dispute code runs, call this helper or POST to the function with the relevant payload.
- Example server-side usage (pseudo-code):

```js
// after saving job to DB
await fetch('/.netlify/functions/admin-notify', { method: 'POST', body: JSON.stringify({ eventType: 'job_request', data: { job, client, submitted_at: new Date().toISOString() } }) });
```

Error handling
- The function will not block primary actions. If email sending fails it will return 202 and log the error in function logs.
