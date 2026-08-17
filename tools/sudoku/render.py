"""HTML/sitemap rendering for generated pages (pure stdlib string templates,
no template engine dependency — rendered once at generation time, the output
committed is plain static HTML)."""

from html import escape

SITE_URL = "https://sudokuonline.cl"
ADSENSE_CLIENT = "ca-pub-1229284733731710"
GA_MEASUREMENT_ID = "G-5QC1LB2EF8"

NAV_ITEMS = [
    ("index.html", "Inicio"),
    ("play.html", "Archivo"),
    ("sudoku-rules.html", "Reglas"),
    ("tecnicas.html", "Técnicas"),
    ("historia.html", "Historia"),
    ("faq.html", "FAQ"),
    ("about.html", "Nosotros"),
    ("contact.html", "Contacto"),
    ("privacy.html", "Privacidad"),
]

MONTH_NAMES_ES = [
    "", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",
]


def _head_scripts():
    return f"""
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_CLIENT}" crossorigin="anonymous"></script>
    <script async src="https://www.googletagmanager.com/gtag/js?id={GA_MEASUREMENT_ID}"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{ dataLayer.push(arguments); }}
      gtag('js', new Date());
      gtag('config', '{GA_MEASUREMENT_ID}');
    </script>"""


def _nav(base, active_href):
    links = []
    for href, label in NAV_ITEMS:
        full_href = f"{base}{href}"
        current = ' aria-current="page"' if href == active_href else ""
        links.append(f'<a href="{full_href}"{current}>{label}</a>')
    return "\n        ".join(links)


def _footer(base):
    links = "\n        ".join(
        f'<a href="{base}{href}">{label}</a>' for href, label in NAV_ITEMS
    )
    return f"""  <footer class="site-footer">
    <div class="footer-inner">
      <p class="footer-brand">Sudoku Online</p>
      <nav class="footer-nav" aria-label="Enlaces del sitio">
        {links}
      </nav>
      <p class="footer-note">Un sudoku nuevo cada día, en tres niveles de dificultad, generado y verificado automáticamente.</p>
      <p class="footer-copy">&copy; {{year}} Sudoku Online (sudokuonline.cl)</p>
    </div>
  </footer>"""


def render_shell(*, title, description, base, active_nav, canonical_path,
                  body_html, extra_head="", year):
    css_links = "\n    ".join(
        f'<link rel="stylesheet" href="{base}css/{name}.css">'
        for name in ("base", "layout", "board", "components", "content")
    )
    footer = _footer(base).replace("{year}", str(year))
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(description)}">
  <link rel="canonical" href="{SITE_URL}/{canonical_path}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{escape(title)}">
  <meta property="og:description" content="{escape(description)}">
  <meta property="og:url" content="{SITE_URL}/{canonical_path}">
  <meta property="og:locale" content="es_CL">
  {css_links}
  <link rel="icon" type="image/x-icon" href="{base}assets/images/favicon.ico">
  {_head_scripts()}
  {extra_head}
</head>
<body>
  <header class="site-header">
    <div class="site-header-inner">
      <a class="site-brand" href="{base}index.html">Sudoku Online</a>
      <nav class="site-nav" aria-label="Navegación principal">
        {_nav(base, active_nav)}
      </nav>
    </div>
  </header>
  <main class="page-container">
{body_html}
  </main>
{footer}
</body>
</html>
"""


def _difficulty_nav(date_str, difficulty_key, is_html_page=True):
    from .difficulty import TIERS

    ext = ".html" if is_html_page else ".json"
    items = []
    for tier in TIERS:
        cls = "active" if tier["key"] == difficulty_key else ""
        href = f"{date_str}-{tier['key']}{ext}"
        items.append(
            f'<a class="difficulty-pill difficulty-{tier["key"]} {cls}" '
            f'href="{href}">{tier["label"]}</a>'
        )
    return "\n          ".join(items)


def render_puzzle_page(*, date_str, difficulty_key, difficulty_label,
                        clues, data_file_name, prev_date, next_date,
                        display_date, year):
    from .difficulty import TIERS_BY_KEY

    title = f"Sudoku {difficulty_label} — {display_date} | Sudoku Online"
    description = (
        f"Juega el sudoku nivel {difficulty_label.lower()} del {display_date} "
        f"gratis, en el navegador, sin registro. Verificación instantánea "
        f"y solución única garantizada."
    )

    prev_link = (
        f'<a class="puzzle-nav-link" href="{prev_date}-{difficulty_key}.html">&larr; Día anterior</a>'
        if prev_date else '<span class="puzzle-nav-link disabled">&larr; Día anterior</span>'
    )
    next_link = (
        f'<a class="puzzle-nav-link" href="{next_date}-{difficulty_key}.html">Día siguiente &rarr;</a>'
        if next_date else '<span class="puzzle-nav-link disabled">Día siguiente &rarr;</span>'
    )

    body = f"""    <section class="content-page puzzle-page">
      <h1 class="section-title">Sudoku del {display_date}</h1>
      <p class="puzzle-meta">Nivel <strong>{difficulty_label}</strong> &middot; {clues} pistas &middot; solución única verificada automáticamente.</p>
      <div class="difficulty-switch" role="tablist" aria-label="Cambiar nivel de dificultad">
          {_difficulty_nav(date_str, difficulty_key)}
      </div>
      <div id="board" class="sudoku-board" data-puzzle-src="../{data_file_name}"></div>
      <div class="actions">
        <button id="check-button" type="button">Verificar</button>
      </div>
      <p id="message" class="message" role="status"></p>
      <nav class="puzzle-navigation" aria-label="Navegación de tableros">
        {prev_link}
        <a class="puzzle-nav-link" href="../play.html">Ver archivo completo</a>
        {next_link}
      </nav>
    </section>"""

    extra_head = '<script type="module" src="../js/puzzle-page.js"></script>'

    return render_shell(
        title=title,
        description=description,
        base="../",
        active_nav="play.html",
        canonical_path=f"sudokus/{date_str}-{difficulty_key}.html",
        body_html=body,
        extra_head=extra_head,
        year=year,
    )


def render_archive_page(listing, year):
    """listing: list of dicts sorted newest first, each with
    date, difficulty, difficulty_label, page, title."""
    from collections import OrderedDict

    by_month = OrderedDict()
    for entry in listing:
        y, m, _ = entry["date"].split("-")
        key = (y, m)
        by_month.setdefault(key, {})
        by_month[key].setdefault(entry["date"], []).append(entry)

    month_blocks = []
    for (y, m), days in by_month.items():
        month_label = f"{MONTH_NAMES_ES[int(m)]} {y}"
        rows = []
        for date_str in sorted(days.keys(), reverse=True):
            day_entries = sorted(
                days[date_str], key=lambda e: e["difficulty_order"]
            )
            links = "\n              ".join(
                f'<a class="puzzle-item-button difficulty-{e["difficulty"]}" '
                f'href="{e["page"]}">{e["difficulty_label"]}</a>'
                for e in day_entries
            )
            d, mo, yr = date_str.split("-")[::-1]
            rows.append(f"""          <li class="archive-day">
            <span class="archive-date">{d}-{mo}-{yr}</span>
            <div class="archive-links">
              {links}
            </div>
          </li>""")
        month_blocks.append(f"""      <div class="archive-month">
        <h3 class="archive-month-title">{month_label}</h3>
        <ul class="archive-day-list">
{chr(10).join(rows)}
        </ul>
      </div>""")

    if not month_blocks:
        content = '<p class="empty-archive">Todavía no hay tableros publicados. Vuelve mañana para ver el primero.</p>'
    else:
        content = "\n".join(month_blocks)

    body = f"""    <section class="content-page">
      <h1 class="section-title">Archivo de Sudokus</h1>
      <p>Todos los tableros publicados, organizados por mes. Cada día se agregan tres niveles nuevos: Fácil, Medio y Difícil.</p>
      <div class="archive">
{content}
      </div>
    </section>"""

    return render_shell(
        title="Archivo de Sudokus | Sudoku Online",
        description="Revisa y juega cualquier sudoku publicado anteriormente en Sudoku Online, organizado por mes y nivel de dificultad.",
        base="",
        active_nav="play.html",
        canonical_path="play.html",
        body_html=body,
        year=year,
    )


def render_sitemap(listing, static_pages):
    urls = [f"{SITE_URL}/"] + [f"{SITE_URL}/{p}" for p in static_pages]
    urls += [f"{SITE_URL}/{e['page']}" for e in listing]
    entries = "\n".join(
        f"  <url><loc>{escape(u)}</loc></url>" for u in urls
    )
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{entries}
</urlset>
"""
