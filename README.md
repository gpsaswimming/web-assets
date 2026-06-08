# web-assets

Shared image/logo CDN and static file store for GPSA, served at
**`assets.gpsaswimming.org`** (Cloudflare Pages project `gpsa-assets`).

The whole repo root is deployed as-is. On each push to `main`,
`.github/workflows/deploy.yml` runs `scripts/generate_index.py` to build a
browsable `index.html` directory listing in every folder, then deploys to
Cloudflare Pages. Reference files by absolute URL, e.g.
`https://assets.gpsaswimming.org/img/gpsa_logo.png`.

## `clinic/` — clinic registration status flag

`clinic/clinic-status.json` is a tiny flag that drives the **clinic registration
button in the GPSA site sidebar**. The clinic site itself
(`clinic.gpsaswimming.org`) is SwimTopia-hosted and doesn't expose a machine
-readable "is registration open" signal, so we publish our own here.

```json
{ "registration_open": false }
```

### Opening / closing the button

When clinic registration opens, set `registration_open` to `true`; set it back to
`false` when it closes. Commit and push to `main` — Cloudflare Pages redeploys and
the sidebar button appears/disappears on the next page load. (This is a manual
flag, mirroring the coach-postings sidebar pattern in the `web-coaches` repo.)

### SwimTopia sidebar snippet

Paste this once into the SwimTopia sidebar HTML block. It's hidden by default and
only shows the button when `registration_open` is `true`:

```html
<!-- GPSA Clinic Registration — Sidebar Widget -->
<div id="clinic-btn" style="display:none; text-align:center; margin: 12px 0;">
  <h2 style="color:#dc001e; background:white; margin-bottom:8px;">Swim Clinic Registration Open!</h2>
  <a href="https://clinic.gpsaswimming.org/register"
     style="background:#dc001e; color:white; padding:10px 16px; border-radius:4px;
            text-decoration:none; font-weight:bold; display:inline-block;">
    Register Now
  </a>
</div>
<script>
  fetch('https://assets.gpsaswimming.org/clinic/clinic-status.json')
    .then(r => r.json())
    .then(d => { if (d.registration_open)
      document.getElementById('clinic-btn').style.display = 'block'; });
</script>
```
