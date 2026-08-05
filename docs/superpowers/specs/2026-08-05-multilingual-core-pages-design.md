# Multilingual Core Pages Stabilization Design

## Objective

Make the English site the structural source of truth, retain only languages that serve the project's stated developed-market targets, and stabilize nine core pages per retained language. English-only blog posts and case studies remain outside the localization scope.

No production deployment is included. Deployment requires a separate confirmation after local verification.

## Language Scope

Retain these 11 languages:

- English (`en`)
- Chinese (`zh`)
- Spanish (`es`)
- Korean (`ko`)
- Japanese (`ja`)
- Portuguese (`pt`)
- Polish (`pl`)
- Italian (`it`)
- German (`de`)
- French (`fr`)
- Dutch (`nl`)

Remove these four languages:

- Turkish (`tr`)
- Russian (`ru`)
- Vietnamese (`vi`)
- Thai (`th`)

Arabic is not present in the current project, so there is no Arabic directory or generated content to delete.

Removal includes the language directories, language-specific `llms` files, Pagefind indexes and metadata, sitemap entries, hreflang entries, language-switcher options, and active generator configuration that could recreate the removed pages.

## Fixed Core Page Set

Each retained language has exactly these nine pages:

1. `index.html`
2. `about.html`
3. `parameters.html`
4. `contact.html`
5. `compatibility.html`
6. `roi.html`
7. `payment.html`
8. `privacy.html`
9. `404.html`

The English versions define page structure, section order, navigation, footer, forms, scripts, and shared assets. Localized versions may differ only in translated copy, locale-specific metadata, active language state, and locale-aware URLs.

## Content Boundaries

- Blog posts and case studies remain English-only.
- Localized Blog links point to `/blog/`; no localized `/xx/blog/` routes are created.
- Product specifications and claims are copied from the English source without invention or expansion.
- Existing valid localized text is preserved wherever its corresponding English element still exists.
- Missing localized copy is translated only for structural elements added from the English source.

## Repair Strategy

Use a conservative static-page repair instead of replacing the site with a new templating framework.

1. Repair and verify the nine English pages first.
2. Add regression tests that define the retained language set and required page structure.
3. Remove the four confirmed language families and all active references to them.
4. Synchronize the DOM structure of every retained localized page with its English counterpart while preserving localized text.
5. Normalize asset paths, internal links, canonical URLs, hreflang sets, language selectors, forms, JSON-LD, and footer/navigation structure.
6. Rebuild the sitemap and Pagefind index from the cleaned `public/` tree.

Existing one-off migration scripts are not treated as authoritative generators. Active build scripts are updated so they cannot recreate removed languages. Unrelated scripts and marketing documents are not refactored.

## SEO and URL Rules

- English remains at root URLs.
- Localized core pages remain under `/{lang}/`.
- Every indexable core page contains alternates for the 11 retained languages plus `x-default`, for 12 unique hreflang entries.
- Canonical URLs use the existing pretty-URL convention.
- `x-default` points to the English equivalent.
- English-only blog and case-study pages use English canonicals and do not advertise nonexistent translations.
- The sitemap contains retained core pages plus English blog and case-study pages; deleted-language URLs and 404 pages are excluded.

## Automated Verification

Tests must fail before implementation when they detect the current drift, then pass after repair. The final suite checks:

- exactly nine core pages exist for every retained language;
- removed language directories and active references are absent;
- localized DOM structure matches the English counterpart after ignoring permitted locale differences;
- contact forms contain the same named fields as English;
- internal links and referenced local assets resolve;
- localized Blog links resolve to `/blog/`;
- canonical and hreflang sets are correct;
- JSON-LD parses successfully;
- no unresolved template placeholders or duplicate IDs remain;
- existing site-integrity tests continue to pass;
- the Pagefind rebuild and a local static-site smoke test succeed.

## Safety and Change Control

- Preserve all unrelated uncommitted work already present in the repository.
- Modify only files required by the multilingual core-page stabilization.
- Do not deploy to Cloudflare Pages.
- Do not change product claims, contact details, analytics identifiers, or company positioning except where structure synchronization requires copying the already-approved English source.
- Any production deployment remains subject to the project's separate confirmation requirement.

## Acceptance Criteria

The work is ready for deployment review only when:

1. the English nine-page core passes every integrity check;
2. all ten retained localized versions pass the same structural and link checks;
3. no removed-language content or active routing reference remains;
4. English blog and case-study pages remain available and no localized blog/case pages are introduced;
5. the complete test suite, Pagefind rebuild, and local browser smoke test finish successfully;
6. the final diff contains no unrelated cleanup or formatting changes.
