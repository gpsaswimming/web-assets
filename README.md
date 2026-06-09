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
<style>
  .gpsa-clinic-cta {
    text-align: center !important;
    padding: 0 !important;
    /* Pulls the content up to eliminate the CMS's hidden top title space */
    margin: -20px 0 0 0 !important;
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
  }
  .gpsa-clinic-cta .clinic-title {
    color: #D10A14 !important;
    font-size: 22px !important;
    font-weight: bold !important;
    line-height: 1.3 !important;
    margin: 0 0 8px 0 !important;
    padding: 0 !important;
    display: block !important;
  }
  .gpsa-clinic-cta .clinic-subtext {
    color: #333333 !important;
    font-size: 16px !important;
    line-height: 1.4 !important;
    margin: 0 0 12px 0 !important;
  }
  .gpsa-clinic-cta .clinic-date {
    font-weight: bold !important;
  }
  .gpsa-clinic-cta .clinic-btn {
    display: inline-block !important;
    background-color: #D10A14 !important;
    color: #ffffff !important;
    text-decoration: none !important;
    font-weight: bold !important;
    font-size: 15px !important;
    padding: 10px 24px !important;
    border-radius: 4px !important;
    transition: background-color 0.15s ease-in-out !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
    width: 85% !important;
    max-width: 260px !important;
    box-sizing: border-box !important;
  }
  .gpsa-clinic-cta .clinic-btn:hover {
    background-color: #A80810 !important;
    color: #ffffff !important;
    text-decoration: none !important;
  }
</style>
<div class="gpsa-clinic-cta" id="clinic-btn" style="display:none;">
    <div class="clinic-title">
        Improve Your Technique This Summer!
    </div>
    <p class="clinic-subtext">
        J. Kyle Hurdle Swim Clinic<br>
        <span class="clinic-date">June 6th – June 7th</span>
    </p>
    <p>
        <a href="https://clinic.gpsaswimming.org" class="clinic-btn" target="_blank" rel="noopener">Register Now</a>
    </p>
</div>
<script>
  fetch('https://assets.gpsaswimming.org/clinic/clinic-status.json')
    .then(r => r.json())
    .then(d => { if (d.registration_open)
      document.getElementById('clinic-btn').style.display = 'block'; });
</script>
```
