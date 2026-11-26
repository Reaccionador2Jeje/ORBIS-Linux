# ORBIS official website

The official ORBIS website is served by the Cloudflare Worker `orbis-linux`.

- Production URL: https://orbis-linux.cristopheriguaran-7.workers.dev
- Worker source: [`cloudflare/worker.js`](../cloudflare/worker.js)
- Wrangler configuration: [`wrangler.toml`](../wrangler.toml)

## Routes

| Path | Purpose |
| --- | --- |
| `/` | Responsive ORBIS product and project website |
| `/api/status` | JSON service health and project metadata |
| `/api/releases` | Latest official GitHub release, ISO asset links and checksums |
| `/healthz` | Health-check JSON |
| `/robots.txt` | Search crawler policy and sitemap location |
| `/sitemap.xml` | Minimal sitemap |
| Other paths | Plain-text 404 |

## Website sections

- ORBIS overview and product positioning.
- ORBIS Earth, Maps, Data, Weather, Sim and Core.
- Desktop edition details and build-artifact disclaimer.
- Live ISO download panel backed by the latest public GitHub Release; it stays in a “not published yet” state until a successful ISO build creates a release.
- Platform facts, development roadmap and community links.
- Responsive mobile navigation, reduced-motion support, metadata and security headers.

The website deliberately labels planned components as planned. It does not claim that a stable ISO release or live Earth-data feeds are available.

## Deploy

The Worker is already deployed to the account's `workers.dev` subdomain. For future source changes:

```bash
npm install --global wrangler
wrangler deploy
```

Authenticate Wrangler with the Cloudflare account that owns the `orbis-linux` Worker. The repository's `wrangler.toml` selects `cloudflare/worker.js`.

## Smoke checks

```bash
curl -fsS https://orbis-linux.cristopheriguaran-7.workers.dev/api/status
curl -I https://orbis-linux.cristopheriguaran-7.workers.dev/
curl -fsS https://orbis-linux.cristopheriguaran-7.workers.dev/robots.txt
```

The health endpoint reports Worker availability, not the build status of the Linux ISO. `/api/releases` reads the latest public GitHub Release and never invents a download URL. The website refreshes this endpoint to populate the official download panel.
