# EUCHIO Mixed Gas Device Website

Website for [gasmixtech.com](https://gasmixtech.com) — EUCHIO Mixed Gas Device product page.

## Product

EUCHIO Mixed Gas Device (氮气氧气配比柜 / 激光切割混气装置)
- Brand: EUCHIO
- Company: Jinan Euchio Machinery Co., Ltd.
- Website: gasmixtech.com

## Quick Start

Open `public/index.html` directly in browser, or serve with any static server:

```bash
# Python
python -m http.server 8000

# Node.js
npx serve

# PHP
php -S localhost:8000
```

## Deploy to Cloudflare Pages

Deploy using Wrangler CLI (no Git connection required):

```bash
cd "E:\我的坚果云\Euchio\激光 金属成型\混合气体设备\网站"
npx wrangler pages deploy public --project-name lishi-laser-website
```

### First-Time Setup (if project doesn't exist yet)

1. Login to Cloudflare: `npx wrangler login`
2. Create project: `npx wrangler pages project create lishi-laser-website`
3. Deploy: `npx wrangler pages deploy public --project-name lishi-laser-website`

## Custom Domain

After first deploy:
1. In [Cloudflare Dashboard](https://dash.cloudflare.com/) → Workers & Pages → lishi-laser-website
2. Custom domains → Add `gasmixtech.com`
3. Update DNS at your registrar to point to Cloudflare

## Project Structure

```
public/
├── index.html              # English homepage (root)
├── parameters.html         # English cutting parameters
├── contact.html            # English contact page
├── privacy.html            # English privacy policy
├── _template.html          # i18n template with {{key}} placeholders
├── 404.html                # Custom 404 page
├── styles.css / script.js  # Main stylesheet & interactions
├── styles.min.css / script.min.js  # Minified production versions
├── robots.txt / sitemap.xml / _headers / favicon.svg
├── images/                 # Product & sample images
├── i18n/                   # Translation JSON files (en.json, zh.json, ...)
├── pagefind/               # Full-text search index & JS
├── blog/                   # English blog posts (11 articles)
├── case-studies/           # English case studies (5 articles)
└── [lang]/                 # 14 language subdirectories (zh/es/ko/ja/pt/tr/pl/it/de/fr/nl/ru/vi/th)
    └── (index + parameters + contact + privacy).html
```

## Contact Info

- Email: sales@gasmixtech.com
- Phone: +86 186 1558 4520 (WeChat)
- WhatsApp Mexico: +52 557 208 0065
- WhatsApp Thailand: +66 961 135 966
