# el-pro.cz

Statický web Ing. Lukáše Macury – LM eP elektro projekce a katalog aplikací pro iPhone, iPad a Mac.
Hostovaný na GitHub Pages (větev `main`, kořen repozitáře), vlastní doména `el-pro.cz` (soubor `CNAME`).
DNS spravuje Seznam Email Profi: A záznamy `@` → 185.199.108.153, 185.199.109.153, 185.199.110.153,
185.199.111.153, CNAME `www` → `<účet>.github.io`. MX záznamy (pošta Seznam) se nemění.

## Struktura

- `index.html` – úvod: hero, aplikace, projekce, kontakt
- `aplikace/` – katalog aplikací (karty; stažení a nákup jen přes App Store)
- `podpora/`, `soukromi/` – obecná podpora a zásady ochrany soukromí webu
- `stazeneleky/` – podpora a zásady ochrany soukromí aplikace Stažené léky.
  **Adresy `podpora.html` a `soukromi.html` jsou zadané v App Store Connect – nepřejmenovávat.**
  Kanonický zdroj těchto stránek je teď zde (původně `app_Sukl_hlídač_iOS/sukl-hlidac/ios/docs/web/`).
- `404.html`, `sitemap.xml`, `robots.txt`, `site.webmanifest`, `favicon.ico`, `apple-touch-icon.png`
- `assets/` – styly (`css/elpro-tokens.css` a `css/elpro-fonts.css` ze značky LM eP, `css/site.css`),
  `js/site.js` (přepínač vzhledu, menu), písma Questrial a Lato, logo, ikony aplikací, OG obrázek
- `.nojekyll` – GitHub Pages servíruje soubory tak, jak jsou

## Úpravy

Hlavička, patička, společná část `<head>`, karty aplikací a `sitemap.xml` se generují skriptem:

```bash
python3 tools/build.py
```

Skript přepíše jen bloky mezi značkami `<!-- @head -->`, `<!-- @header -->`, `<!-- @footer -->`
a `<!-- @apps -->`; zbytek stránek se upravuje přímo v HTML. Seznam aplikací je v `tools/build.py`
(`APPS`). Až aplikace vyjde v App Storu, doplň u ní `appstore` (např.
`https://apps.apple.com/cz/app/id6829675417`), ulož oficiální odznak „Stáhnout v App Storu“
z Apple Marketing Tools jako `assets/img/appstore-badge-cs.svg` a spusť skript znovu.

Náhled: `python3 -m http.server 8742` v kořeni repozitáře a otevřít `http://localhost:8742/`.
