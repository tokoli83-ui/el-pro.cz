#!/usr/bin/env python3
"""Doplní do stránek el-pro.cz společné části a vygeneruje sitemap.xml.

Stránky jsou běžné HTML soubory v repozitáři (GitHub Pages je servíruje tak, jak jsou).
Skript jen přepíše bloky mezi značkami
    <!-- @head --> … <!-- /@head -->
    <!-- @header --> … <!-- /@header -->
    <!-- @footer --> … <!-- /@footer -->
podle šablon níže. Titulek a popis stránky se berou z jejího <title> a <meta name="description">.

Spuštění z kořene repozitáře:  python3 tools/build.py
"""
import hashlib
import html
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://el-pro.cz"
OG_IMAGE = SITE + "/assets/img/og.png"

NAV = [
    ("/aplikace/", "Aplikace"),
    ("/#projekce", "Projekce"),
    ("/podpora/", "Podpora"),
    ("/#kontakt", "Kontakt"),
]

# Katalog aplikací (blok <!-- @apps -->). Prodej i stažení jen přes App Store:
# po vydání doplň "appstore" (https://apps.apple.com/cz/app/id<AppleID>) a "price",
# karta pak místo štítku ukáže odznak „Stáhnout v App Storu“ (soubor BADGE níže).
APPS = [
    {
        "name": "Stažené léky",
        "icon": "stazene-leky",
        "text": "Hlídač sdělení SÚKL: stažení léčivých přípravků z trhu, pozastavení distribuce "
                "a upozornění na padělky. Na každé nové opatření upozorní. Bez účtu, bez sběru dat.",
        "platforms": "iPhone · iPad · Mac",
        "price": "Zdarma",
        "status": "Brzy v App Storu",
        "appstore": None,  # https://apps.apple.com/cz/app/id6829675417 – až Apple aplikaci schválí
        "links": [("Podpora", "/stazeneleky/podpora.html"), ("Ochrana soukromí", "/stazeneleky/soukromi.html")],
    },
    {
        "name": "PDFPodpis",
        "icon": "pdfpodpis",
        "text": "Prohlížeč PDF s kvalifikovaným elektronickým podpisem a časovým razítkem – "
                "certifikát PostSignum nebo ČKAIT na tokenu či čipové kartě.",
        "platforms": "Mac",
        "status": "Připravujeme",
    },
    {
        "name": "MXW01 Printer",
        "icon": "mxw01-printer",
        "text": "Tisk textu, obrázků, PDF, QR a čárových kódů na mini termotiskárnu "
                "WG Thermo Mini přes Bluetooth – bez účtu a bez telefonu.",
        "platforms": "Mac",
        "status": "Připravujeme",
    },
    {
        "name": "LMproCAD",
        "icon": "lmprocad.svg",
        "text": "Kreslení jednopólových schémat rozváděčů s knihovnou značek, "
                "kusovníkem a exportem do PDF.",
        "platforms": "Mac",
        "status": "Připravujeme",
    },
]
# Oficiální odznak Apple (Marketing Tools, česká verze) – uložit sem před prvním vydáním.
BADGE = "/assets/img/appstore-badge-cs.svg"


def asset_version() -> str:
    h = hashlib.md5()
    for rel in ("assets/css/site.css", "assets/css/elpro-tokens.css", "assets/css/elpro-fonts.css", "assets/js/site.js"):
        h.update((ROOT / rel).read_bytes())
    return h.hexdigest()[:8]


def url_for(rel: str) -> str:
    if rel == "index.html":
        return SITE + "/"
    if rel.endswith("/index.html"):
        return f"{SITE}/{rel[:-len('index.html')]}"
    return f"{SITE}/{rel}"


def active_nav(rel: str) -> str:
    if rel.startswith(("aplikace/", "stazeneleky/")):
        return "/aplikace/"
    if rel.startswith("podpora/"):
        return "/podpora/"
    return ""


def head_block(rel: str, title: str, desc: str, ver: str, noindex: bool) -> str:
    url = url_for(rel)
    t, d = html.escape(title, quote=True), html.escape(desc, quote=True)
    lines = [
        '<meta name="theme-color" content="#0D1B26">',
        '<link rel="icon" href="/favicon.ico" sizes="any">',
        '<link rel="icon" type="image/png" sizes="32x32" href="/assets/img/favicon-32.png">',
        '<link rel="apple-touch-icon" href="/apple-touch-icon.png">',
        '<link rel="manifest" href="/site.webmanifest">',
        '<link rel="preload" href="/assets/fonts/questrial-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>',
        '<link rel="preload" href="/assets/fonts/lato-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>',
        f'<link rel="stylesheet" href="/assets/css/elpro-fonts.css?v={ver}">',
        f'<link rel="stylesheet" href="/assets/css/elpro-tokens.css?v={ver}">',
        f'<link rel="stylesheet" href="/assets/css/site.css?v={ver}">',
        '<script>try{var t=localStorage.getItem("elpro-theme");if(t==="light"||t==="dark")document.documentElement.setAttribute("data-theme",t)}catch(e){}</script>',
        f'<script src="/assets/js/site.js?v={ver}" defer></script>',
    ]
    if noindex:
        lines.append('<meta name="robots" content="noindex">')
    else:
        lines += [
            f'<link rel="canonical" href="{url}">',
            '<meta property="og:type" content="website">',
            '<meta property="og:locale" content="cs_CZ">',
            '<meta property="og:site_name" content="LM eP – elektro projekce">',
            f'<meta property="og:title" content="{t}">',
            f'<meta property="og:description" content="{d}">',
            f'<meta property="og:url" content="{url}">',
            f'<meta property="og:image" content="{OG_IMAGE}">',
            '<meta property="og:image:width" content="1200">',
            '<meta property="og:image:height" content="630">',
            '<meta name="twitter:card" content="summary_large_image">',
        ]
    return "\n".join(lines)


def header_block(rel: str) -> str:
    active = active_nav(rel)
    current = ' aria-current="page"'
    links = "\n".join(
        f'      <a href="{href}"{current if href == active else ""}>{label}</a>' for href, label in NAV
    )
    return f"""<a class="skip" href="#obsah">Přeskočit na obsah</a>
<header class="site-header">
  <div class="wrap site-header__in">
    <a class="brand" href="/" aria-label="LM eP – elektro projekce, úvodní stránka">
      <img class="brand__logo brand__logo--dark" src="/assets/img/logo/lmep_logo_primary_white.png" width="540" height="168" alt="Lukáš Macura – elektro projekce">
      <img class="brand__logo brand__logo--light" src="/assets/img/logo/lmep_logo_primary.png" width="540" height="168" alt="Lukáš Macura – elektro projekce">
    </a>
    <nav class="site-nav" id="hlavni-menu" aria-label="Hlavní navigace">
{links}
    </nav>
    <div class="site-tools">
      <button class="icon-btn" type="button" data-theme-toggle aria-label="Přepnout vzhled">
        <svg class="i-sun" viewBox="0 0 16 16" aria-hidden="true"><circle cx="8" cy="8" r="3" fill="none" stroke="currentColor" stroke-width="1.3"/><path d="M8 1v2M8 13v2M1 8h2M13 8h2M3.05 3.05l1.4 1.4M11.55 11.55l1.4 1.4M3.05 12.95l1.4-1.4M11.55 4.45l1.4-1.4" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/></svg>
        <svg class="i-moon" viewBox="0 0 16 16" aria-hidden="true"><path d="M13.5 9.6A5.8 5.8 0 0 1 6.4 2.5a5.8 5.8 0 1 0 7.1 7.1Z" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linejoin="round"/></svg>
      </button>
      <button class="menu-toggle" type="button" data-menu-toggle aria-expanded="false" aria-controls="hlavni-menu">Menu</button>
    </div>
    <p class="site-claim">Elektro projekce · Aplikace pro <span class="ap">iPHONE</span>, <span class="ap">iPAD</span> a Mac</p>
  </div>
</header>"""


FOOTER = """<footer class="site-footer">
  <div class="wrap site-footer__grid">
    <div>
      <img class="site-footer__symbol site-footer__symbol--dark" src="/assets/img/logo/lmep_symbol_white.png" width="161" height="192" alt="" loading="lazy">
      <img class="site-footer__symbol site-footer__symbol--light" src="/assets/img/logo/lmep_symbol.png" width="161" height="192" alt="" loading="lazy">
    </div>
    <address>
      <strong>Ing. Lukáš Macura · LM eP – elektro projekce</strong><br>
      Záchranářů 785, 735 14 Orlová – Poruba, Česká republika<br>
      IČO 04246420 · neplátce DPH · fyzická osoba zapsaná v živnostenském rejstříku vedeném Městským úřadem Orlová, nezapsaná v obchodním rejstříku<br>
      Autorizovaný technik pro technologická zařízení staveb ČKAIT – 1103802 (obor TT00)<br>
      Tel. <a href="tel:+420724055980">+420 724 055 980</a> · E‑mail <a href="mailto:info@el-pro.cz">info@el-pro.cz</a>
    </address>
    <div class="site-footer__right">
      <nav aria-label="Odkazy v patičce">
        <a href="/aplikace/">Aplikace</a>
        <a href="/podpora/">Podpora</a>
        <a href="/soukromi/">Ochrana soukromí</a>
      </nav>
      <div class="badges">
        <img src="/assets/img/logo/badge_ckait.png" width="101" height="96" alt="ČKAIT" loading="lazy">
        <img src="/assets/img/logo/badge_ex.png" width="111" height="96" alt="Ex" loading="lazy">
      </div>
      <p class="small" style="margin:0">© 2026 Lukáš Macura</p>
    </div>
  </div>
</footer>"""


def app_icon(app: dict) -> str:
    alt = f'Ikona aplikace {app["name"]}'
    if app["icon"].endswith(".svg"):
        return f'<img class="app-card__icon" src="/assets/img/apps/{app["icon"]}" width="256" height="256" alt="{alt}" loading="lazy">'
    base = f'/assets/img/apps/{app["icon"]}'
    return (f'<picture><source srcset="{base}.webp" type="image/webp">'
            f'<img class="app-card__icon" src="{base}.png" width="256" height="256" alt="{alt}" loading="lazy"></picture>')


def apps_block() -> str:
    has_badge = (ROOT / BADGE.lstrip("/")).exists()
    cards = []
    for app in APPS:
        if app.get("appstore"):
            label = f'Stáhnout {app["name"]} v App Storu'
            cta = (f'<a class="appstore-badge" href="{app["appstore"]}" aria-label="{label}"><img src="{BADGE}" width="120" height="40" alt="Stáhnout v App Storu"></a>'
                   if has_badge else f'<a class="btn btn--primary" href="{app["appstore"]}" aria-label="{label}">Stáhnout v App Storu</a>')
            top_right = ""
        else:
            cta = ""
            muted = " chip--muted" if app["status"] == "Připravujeme" else ""
            top_right = f'<span class="chip{muted}">{app["status"]}</span>'
        links = ""
        if app.get("links"):
            links = ('\n      <p class="app-card__links">'
                     + "".join(f'<a href="{h}">{t}</a>' for t, h in app["links"]) + "</p>")
        price = f'<span class="price">{app["price"]}</span>' if app.get("price") else ""
        cards.append(f"""  <li>
    <article class="app-card">
      <div class="app-card__top">{app_icon(app)}{top_right}</div>
      <h3>{app["name"]}</h3>
      <p>{app["text"]}</p>{links}
      <div class="app-card__foot"><span class="platforms">{app["platforms"]}</span>{price}{cta}</div>
    </article>
  </li>""")
    return '<ul class="apps">\n' + "\n".join(cards) + "\n</ul>"


def replace_block(text: str, name: str, content: str, rel: str) -> str:
    pat = re.compile(rf"(<!-- @{name} -->\n).*?(\n?<!-- /@{name} -->)", re.S)
    if not pat.search(text):
        raise SystemExit(f"{rel}: chybí blok <!-- @{name} -->")
    return pat.sub(lambda m: m.group(1) + content + "\n" + m.group(2).lstrip("\n"), text, count=1)


def main() -> None:
    ver = asset_version()
    pages = []
    for path in sorted(ROOT.rglob("*.html")):
        rel = path.relative_to(ROOT).as_posix()
        if rel.startswith((".", "tools/")) or "/." in rel:
            continue
        text = path.read_text(encoding="utf-8")
        if "<!-- @head -->" not in text:
            continue  # např. stazeneleky/index.html (jen přesměrování)
        title = html.unescape(re.search(r"<title>(.*?)</title>", text, re.S).group(1).strip())
        desc_m = re.search(r'<meta name="description" content="(.*?)">', text, re.S)
        desc = html.unescape(desc_m.group(1)) if desc_m else ""
        noindex = rel == "404.html"
        text = replace_block(text, "head", head_block(rel, title, desc, ver, noindex), rel)
        text = replace_block(text, "header", header_block(rel), rel)
        text = replace_block(text, "footer", FOOTER, rel)
        if "<!-- @apps -->" in text:
            text = replace_block(text, "apps", apps_block(), rel)
        path.write_text(text, encoding="utf-8")
        if not noindex:
            pages.append(url_for(rel))
        print("ok", rel)

    today = date.today().isoformat()
    urls = "\n".join(f"  <url><loc>{u}</loc><lastmod>{today}</lastmod></url>" for u in pages)
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "\n</urlset>\n",
        encoding="utf-8",
    )
    print(f"sitemap.xml: {len(pages)} adres, verze assets {ver}")


if __name__ == "__main__":
    main()
