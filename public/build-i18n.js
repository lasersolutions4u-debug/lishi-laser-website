#!/usr/bin/env node
/**
 * build-i18n.js — Static i18n build for gasmixtech.com
 * Reads index.html (template with {{key}} markers) + i18n/*.json
 * Generates localized HTML for each language.
 *
 * Usage: node build-i18n.js
 * No npm dependencies required.
 */

const fs = require('fs');
const path = require('path');

const PUBLIC_DIR = __dirname;
const I18N_DIR = path.join(PUBLIC_DIR, 'i18n');
const SUPPORTED_LOCALES = ['en', 'zh', 'es', 'pt', 'ja', 'ko', 'pl'];
const CORE_PATHS = [
  '/about',
  '/contact',
  '/products/psa-nitrogen-generation-system',
  '/products/integrated-gas-mixing-cabinet',
  '/products/mspv2-4000-proportional-valve',
  '/products/mixed-gas-control-comparison',
];

// ═══════════════════════════════════════════════════════════════════════
// Helpers
// ═══════════════════════════════════════════════════════════════════════

/**
 * Replace every {{key}} marker with its translated value.
 * Keys use dot-notation: {{hero.title}} → strings.hero.title
 */
function replacePlaceholders(html, strings) {
  return html.replace(/\{\{([^}]+)\}\}/g, (match, key) => {
    const normalizedKey = key.trim();
    const value = getNestedValue(strings, normalizedKey);
    if (value === undefined) {
      throw new Error(`Missing translation key: ${normalizedKey}`);
    }
    return String(value);
  });
}

/**
 * Walk a nested object with dot-notation path.
 * getNestedValue({a:{b:"hi"}}, "a.b") → "hi"
 */
function getNestedValue(obj, path) {
  return path.split('.').reduce((o, k) => (o && o[k] !== undefined ? o[k] : undefined), obj);
}

/**
 * Adjust relative paths for subdirectory pages.
 *
 * Template (root) uses:
 *   ./styles.min.css   ./images/…   ./favicon.svg   ./script.min.js
 *   /contact.html  /parameters.html  /
 *
 * Subdirectory pages need:
 *   ../styles.min.css  ../images/…  ../favicon.svg  ../script.min.js
 *   ./contact.html ./parameters.html  ../
 */
function adjustPaths(html, lang) {
  // 1. Asset paths  ./xxx  →  ../xxx
  html = html.replace(/\.(\/(styles(?:\.min)?\.css|script(?:\.min)?\.js|favicon\.svg|images\/))/g, '../$2');

  // 2. Localized core sales-path links
  for (const route of CORE_PATHS) {
    const escapedRoute = route.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const routePattern = new RegExp(`href="${escapedRoute}(?=["?#])`, 'g');
    html = html.replace(routePattern, `href="/${lang}${route}`);
  }

  // 2b. Root-relative script  /script.min.js → ../script.min.js
  html = html.replace(/src="\/script(?:\.min)?\.js"/g, 'src="../script.min.js"');

  // 3. Root-relative dir links  href="/zh/" → href="../zh/"
  //    but skip href="//" (protocol-relative) and already-adjusted paths
  html = html.replace(/href="\/(?!\/)([a-z]{2}\/)"/g, 'href="../$1"');

  // 4. Home link  href="/" → href="../"
  //    Use negative lookahead to avoid matching "/zh/" etc. (already handled)
  html = html.replace(/href="\/"(?!\/)/g, 'href="../"');

  return html;
}

/**
 * Update <html lang>, <link rel="canonical">, and og:url for the language.
 */
function updateMeta(html, lang) {
  // <html lang="xx">
  html = html.replace(/<html lang="en">/, `<html lang="${lang}">`);

  // canonical
  html = html.replace(
    /<link rel="canonical" href="https:\/\/gasmixtech\.com\/">/,
    `<link rel="canonical" href="https://gasmixtech.com/${lang}/">`
  );

  // og:url
  html = html.replace(
    /<meta property="og:url" content="https:\/\/gasmixtech\.com\/">/,
    `<meta property="og:url" content="https://gasmixtech.com/${lang}/">`
  );

  return html;
}

/**
 * Move the "active" class to the correct language option in the switcher.
 */
function updateActiveLang(html, lang) {
  // Remove "active" from all lang-option links
  html = html.replace(/ class="lang-option active"/g, ' class="lang-option"');
  // Add "active" to the current language's option
  const langRe = new RegExp(`(class="lang-option")( data-lang="${lang}")`);
  html = html.replace(langRe, ' class="lang-option active"$2');
  return html;
}

function requestedLocales(args) {
  if (args.length === 0) return [...SUPPORTED_LOCALES];

  const locales = [];
  for (let index = 0; index < args.length; index++) {
    if (args[index] !== '--locale') {
      throw new Error(`Unknown argument: ${args[index]}`);
    }

    if (index + 1 >= args.length || args[index + 1] === '--locale') {
      throw new Error('Missing value for --locale');
    }

    const locale = args[++index];
    if (!SUPPORTED_LOCALES.includes(locale)) {
      throw new Error(`Unsupported locale: ${locale}`);
    }
    if (!locales.includes(locale)) locales.push(locale);
  }
  return locales;
}

function main(args = process.argv.slice(2)) {
  const locales = requestedLocales(args);
  const templatePath = path.join(PUBLIC_DIR, '_template.html');
  const template = fs.readFileSync(templatePath, 'utf-8');

  const localeSources = locales.map((locale) => {
    const jsonPath = path.join(I18N_DIR, `${locale}.json`);
    if (!fs.existsSync(jsonPath)) {
      throw new Error(`Missing translation file: ${locale}.json`);
    }

    try {
      return {
        locale,
        strings: JSON.parse(fs.readFileSync(jsonPath, 'utf-8')),
      };
    } catch (error) {
      throw new Error(`Invalid translation JSON: ${locale}.json`);
    }
  });

  const renderedPages = localeSources.map(({ locale, strings }) => {
    let html = replacePlaceholders(template, strings);
    if (locale !== 'en') {
      html = adjustPaths(html, locale);
      html = updateMeta(html, locale);
    }
    html = updateActiveLang(html, locale);

    if (html.includes('{{') || html.includes('}}')) {
      throw new Error(`Unresolved translation marker: ${locale}/index.html`);
    }

    const outDir = locale === 'en' ? PUBLIC_DIR : path.join(PUBLIC_DIR, locale);
    return { locale, html, outDir };
  });

  for (const { locale, html, outDir } of renderedPages) {
    if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });
    fs.writeFileSync(path.join(outDir, 'index.html'), html, 'utf-8');
    console.log(locale === 'en' ? '  en/index.html (root)' : `  ${locale}/index.html`);
  }

  console.log(`\nDone — ${locales.length} language(s) built.`);
}

if (require.main === module) {
  try {
    main();
  } catch (error) {
    console.error(error.message);
    process.exitCode = 1;
  }
}

module.exports = { replacePlaceholders, adjustPaths, SUPPORTED_LOCALES };
