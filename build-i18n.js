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

// Supported languages — add new ones here + create i18n/xx.json
const LANGUAGES = ['zh', 'es', 'ko', 'ja', 'pt'];

// ─── Read template ──────────────────────────────────────────────────
const templatePath = path.join(PUBLIC_DIR, '_template.html');
const template = fs.readFileSync(templatePath, 'utf-8');

// ─── Build English (root) ───────────────────────────────────────────
const enStrings = JSON.parse(fs.readFileSync(path.join(I18N_DIR, 'en.json'), 'utf-8'));
const enHtml = replacePlaceholders(template, enStrings);
fs.writeFileSync(path.join(PUBLIC_DIR, 'index.html'), enHtml, 'utf-8');
console.log('  en/index.html (root)');

// ─── Build each language ─────────────────────────────────────────────
let built = 1;

for (const lang of LANGUAGES) {
  const jsonPath = path.join(I18N_DIR, `${lang}.json`);

  if (!fs.existsSync(jsonPath)) {
    console.warn(`  skip: ${lang}.json not found`);
    continue;
  }

  const strings = JSON.parse(fs.readFileSync(jsonPath, 'utf-8'));
  let html = replacePlaceholders(template, strings);
  html = adjustPaths(html, lang);
  html = updateMeta(html, lang);
  html = updateActiveLang(html, lang);

  const outDir = path.join(PUBLIC_DIR, lang);
  if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

  fs.writeFileSync(path.join(outDir, 'index.html'), html, 'utf-8');
  built++;
  console.log(`  ${lang}/index.html`);
}

console.log(`\nDone — ${built} language(s) built.`);

// ═══════════════════════════════════════════════════════════════════════
// Helpers
// ═══════════════════════════════════════════════════════════════════════

/**
 * Replace every {{key}} marker with its translated value.
 * Keys use dot-notation: {{hero.title}} → strings.hero.title
 */
function replacePlaceholders(html, strings) {
  return html.replace(/\{\{([^}]+)\}\}/g, (match, key) => {
    const value = getNestedValue(strings, key.trim());
    if (value === undefined) {
      console.warn(`    missing key: ${key.trim()}`);
      return match; // leave marker in place so it's easy to spot
    }
    return value;
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
 *   ./styles.css   ./images/…   ./favicon.svg   ./script.js
 *   /contact.html  /parameters.html  /
 *
 * Subdirectory pages need:
 *   ../styles.css  ../images/…  ../favicon.svg  ../script.js
 *   ./contact.html ./parameters.html  ../
 */
function adjustPaths(html, lang) {
  // 1. Asset paths  ./xxx  →  ../xxx
  html = html.replace(/\.(\/(styles\.css|script\.js|favicon\.svg|images\/))/g, '../$2');

  // 2. Root-relative page links  /contact.html → ./contact.html
  html = html.replace(/href="\/(contact\.html|parameters\.html)"/g, 'href="./$1"');

  // 2b. Root-relative script  /script.js → ../script.js
  html = html.replace(/src="\/script\.js"/g, 'src="../script.js"');

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
