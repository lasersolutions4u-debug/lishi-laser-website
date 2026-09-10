from pathlib import Path

DOMAIN = "https://gasmixtech.com"
SUPPORTED_LOCALES = ("en", "zh", "es", "pt", "ja", "ko", "pl")
LOCALIZED_LOCALES = SUPPORTED_LOCALES[1:]
UNSUPPORTED_LOCALES = ("de", "fr", "it", "nl", "tr", "ru", "vi", "th")

CORE_ROUTES = {
    "home": "/",
    "about": "/about",
    "contact": "/contact",
    "psa": "/products/psa-nitrogen-generation-system",
    "cabinet": "/products/integrated-gas-mixing-cabinet",
    "valve": "/products/mspv2-4000-proportional-valve",
    "comparison": "/products/mixed-gas-control-comparison",
}


def route_for(locale, page_key):
    route = CORE_ROUTES[page_key]
    if locale == "en":
        return route
    return f"/{locale}/" if page_key == "home" else f"/{locale}{route}"


def canonical_url(locale, page_key):
    return f"{DOMAIN}{route_for(locale, page_key)}"


def output_path(public_dir: Path, locale, page_key):
    route = CORE_ROUTES[page_key]
    if page_key == "home":
        relative = Path("index.html")
    else:
        relative = Path(route.lstrip("/") + ".html")
    return public_dir / relative if locale == "en" else public_dir / locale / relative


def alternates_for(page_key):
    values = {locale: canonical_url(locale, page_key) for locale in SUPPORTED_LOCALES}
    values["x-default"] = values["en"]
    return values
