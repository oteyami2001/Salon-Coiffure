#!/usr/bin/env python3
"""Génère le site statique (en français) à partir d'un fichier de configuration JSON.

Usage : python3 build.py site.json [dossier_sortie]
Bibliothèque standard uniquement.
"""
import json
import shutil
import sys
from datetime import date
from html import escape as e
from pathlib import Path

ASSETS = Path(__file__).resolve().parent / "assets"

MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet",
        "août", "septembre", "octobre", "novembre", "décembre"]

PALETTES = [("#6f6a62", "#2f2c28"), ("#8a7f70", "#3a352f"), ("#5d6669", "#25292b"),
            ("#7b6f66", "#332d29"), ("#68705f", "#2a2e26"), ("#857565", "#3b3129")]


def fr_date(value):
    """'2026-09-01' -> '1 septembre 2026' (laisse le texte tel quel sinon)."""
    try:
        d = date.fromisoformat(value)
    except (TypeError, ValueError):
        return value or ""
    return f"{'1er' if d.day == 1 else d.day} {MOIS[d.month - 1]} {d.year}"


def para(text):
    return f"<p>{e(text)}</p>" if text else ""


class Site:
    def __init__(self, cfg_path, out):
        self.cfg_path = Path(cfg_path).resolve()
        self.cfg = json.loads(self.cfg_path.read_text(encoding="utf-8"))
        self.out = Path(out).resolve()
        self.ph_count = 0

    # ---------- helpers ----------
    def img(self, src, label, rel):
        """Return une source utilisable : URL telle quelle, fichier local copié ou image provisoire générée."""
        if src:
            if src.startswith(("http://", "https://", "//", "data:")):
                return src
            p = (self.cfg_path.parent / src).resolve()
            if p.exists():
                dest = self.out / "assets" / "img" / p.name
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(p, dest)
                return f"{rel}assets/img/{p.name}"
            print(f"attention : image introuvable : {src} (image provisoire utilisée)")
        return rel + self.placeholder(label)

    def placeholder(self, label):
        self.ph_count += 1
        a, b = PALETTES[self.ph_count % len(PALETTES)]
        n = self.ph_count
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 1000" preserveAspectRatio="xMidYMid slice">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient></defs>
<rect width="1600" height="1000" fill="url(#g)"/>
<g fill="none" stroke="#fff" stroke-opacity=".12" stroke-width="2">
<path d="M0 760 L{300 + n * 37 % 400} 520 L{900 + n * 53 % 300} 560 L1600 380"/>
<rect x="{260 + n * 71 % 500}" y="300" width="420" height="460"/>
<rect x="{760 + n * 43 % 300}" y="420" width="300" height="340"/>
<path d="M0 760 H1600"/></g>
<title>{e(label)} (image provisoire)</title>
</svg>'''
        name = f"assets/img/ph-{n}.svg"
        dest = self.out / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(svg, encoding="utf-8")
        return name

    def write(self, path, html):
        dest = self.out / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(html, encoding="utf-8")

    # ---------- shell ----------
    def nav(self, rel, current):
        c = self.cfg
        items = [
            ("LE SALON", "a-propos.html", [("L’ÉQUIPE", "equipe.html"), ("RECRUTEMENT", "recrutement.html")]),
            ("RÉALISATIONS", "realisations.html", [(m["title"].upper(), f"realisations/{m['slug']}.html") for m in c["markets"]]),
            ("PRESTATIONS", "services.html", [(s["title"].upper(), f"services/{s['slug']}.html") for s in c["services"]]),
            ("ACTUALITÉS", "actualites.html", []),
            ("CONTACT", "contact.html", []),
        ]
        out = []
        for label, href, kids in items:
            cur = ' aria-current="page"' if current == href else ""
            sub = ""
            if kids:
                sub = '<ul class="sub">' + "".join(
                    f'<li><a href="{rel}{h}"{" aria-current=page" if current == h else ""}>{e(t)}</a></li>' for t, h in kids
                ) + "</ul>"
            out.append(f'<li><a href="{rel}{href}"{cur}>{label}</a>{sub}</li>')
        return "<ul>" + "".join(out) + "</ul>"

    def brand_html(self, rel, home):
        b = self.cfg["brand"]
        name = e(b.get("short") or b["name"])
        dark = self.resolve_logo(b.get("logo"), rel)
        light = self.resolve_logo(b.get("logo_white") or b.get("logo"), rel)
        if dark or light:
            parts = f'<img class="logo-dark" src="{dark or light}" alt="{name}">'
            if home:
                parts += f'<img class="logo-light" src="{light or dark}" alt="">'
            return parts
        return name

    def resolve_logo(self, src, rel):
        return self.img(src, "logo", rel) if src else ""

    def tagline(self):
        return '<div class="tagline">' + "".join(f"<span>{e(t)}</span>" for t in self.cfg["brand"]["tagline"]) + "</div>"

    def footer(self, rel):
        c = self.cfg
        col = lambda title, links: f"<div><h4>{title}</h4>" + "".join(f'<a href="{rel}{h}">{e(t)}</a>' for t, h in links) + "</div>"
        locs = ""
        for l in c["locations"]:
            lines = "<br>".join(e(x) for x in l.get("lines", []))
            phone = l.get("phone", "")
            tel = "".join(ch for ch in phone if ch.isdigit())
            extra = f'<br>Tél. <a href="tel:{tel}">{e(phone)}</a>' if phone else ""
            if l.get("email"):
                extra += f'<br><a href="mailto:{e(l["email"])}">{e(l["email"])}</a>'
            locs += f'<p class="loc"><strong>{e(l["city"])}</strong><br>{lines}{extra}</p>'
        icons = {
            "facebook": '<path d="M14 9V7c0-.8.5-1 1-1h2V2h-3c-3 0-4 2-4 4.5V9H8v4h2v9h4v-9h3l.5-4H14z"/>',
            "instagram": '<path d="M12 7a5 5 0 100 10 5 5 0 000-10zm0 8a3 3 0 110-6 3 3 0 010 6zm5.5-9a1.2 1.2 0 100 2.4 1.2 1.2 0 000-2.4zM17 2H7a5 5 0 00-5 5v10a5 5 0 005 5h10a5 5 0 005-5V7a5 5 0 00-5-5zm3 15a3 3 0 01-3 3H7a3 3 0 01-3-3V7a3 3 0 013-3h10a3 3 0 013 3v10z"/>',
            "linkedin": '<path d="M4 3a2 2 0 100 4 2 2 0 000-4zM2 9h4v12H2zm7 0h4v1.7c.6-1 2-2 4-2 4 0 5 2.5 5 6V21h-4v-5.5c0-1.5 0-3.3-2-3.3s-2.4 1.6-2.4 3.2V21H9z"/>',
        }
        social = "".join(
            f'<a href="{e(u)}" aria-label="{k}" rel="noopener" target="_blank"><svg viewBox="0 0 24 24" aria-hidden="true">{icons[k]}</svg></a>'
            for k, u in c.get("social", {}).items() if u and k in icons
        )
        credit = c.get("footer", {}).get("credit", "")
        return f'''<footer class="footer"><div class="wrap"><div class="footer-cols">
{col("LE SALON", [("l’équipe", "equipe.html"), ("recrutement", "recrutement.html"), ("contact", "contact.html")])}
{col("RÉALISATIONS", [(m["title"], f"realisations/{m['slug']}.html") for m in c["markets"]])}
{col("PRESTATIONS", [(s["title"], f"services/{s['slug']}.html") for s in c["services"]])}
<div><h4>NOUS TROUVER</h4>{locs}</div></div>
{f'<div class="social">{social}</div>' if social else ""}
<div class="copyright">&copy; {date.today().year} {e(c["brand"]["name"])}. Tous droits réservés.{(" " + e(credit)) if credit else ""}</div>
</div></footer>'''

    def page(self, path, title, body, current, home=False):
        rel = "../" * path.count("/")
        c = self.cfg
        col, f = c["colors"], c["fonts"]
        root = (f":root{{--ink:{col['ink']};--paper:{col['paper']};--muted:{col['muted']};--line:{col['line']};"
                f"--accent:{col['accent']};--footer-bg:{col['footer_bg']};--footer-ink:{col['footer_ink']};"
                f"--font-display:'{f['display']}';--font-body:'{f['body']}'}}")
        fonts = f'<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?{f["google_fonts_query"]}&display=swap">' if f.get("google_fonts_query") else ""
        name = e(c["brand"]["name"])
        html = f'''<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)} | {name}</title>
<meta name="description" content="{e(c['brand'].get('description', ''))}">
<meta property="og:title" content="{e(title)} | {name}"><meta property="og:type" content="website"><meta property="og:locale" content="fr_FR">
{fonts}<link rel="stylesheet" href="{rel}assets/styles.css"><style>{root}</style></head>
<body class="{'home' if home else 'inner'}">
<a class="skip" href="#main-content">Aller au contenu principal</a>
<header class="site-header"><div class="wrap header-inner">
<a class="brand" href="{rel}index.html" aria-label="{name} – accueil">{self.brand_html(rel, home)}</a>
<button class="menu-toggle" aria-label="Menu" aria-expanded="false" aria-controls="site-nav"><span></span><span></span><span></span></button>
<nav class="nav" id="site-nav" aria-label="Navigation principale">{self.nav(rel, current)}</nav>
</div></header>
<main id="main-content">{body(rel)}</main>
{self.footer(rel)}
<script src="{rel}assets/main.js"></script></body></html>'''
        self.write(path, html)

    def inner_head(self, title, intro):
        return f'{self.tagline()}<section class="section"><div class="wrap"><h2 class="page-title">{e(title)}</h2><p class="lede">{e(intro)}</p></div></section>'

    # ---------- pages ----------
    def home(self):
        c = self.cfg

        def body(rel):
            slides = c["hero"]["slides"] or [{"image": "", "caption": ""}]
            s_html = "".join(
                f'<div class="slide{" is-active" if i == 0 else ""}" data-caption="{e(s.get("caption", ""))}">'
                f'<img src="{self.img(s.get("image"), s.get("caption") or "hero", rel)}" alt="{e(s.get("caption", ""))}"{"" if i == 0 else " loading=lazy"}></div>'
                for i, s in enumerate(slides))
            dots = "".join(f'<button aria-label="Diapositive {i+1}"{" class=is-active" if i == 0 else ""}></button>' for i in range(len(slides))) if len(slides) > 1 else ""
            logo = c["brand"].get("logo_white")
            mark = f'<img src="{self.img(logo, "logo", rel)}" alt="{e(c["brand"]["name"])}">' if logo else f'<div class="word">{e(c["brand"].get("short") or c["brand"]["name"])}</div>'
            tiles = "".join(
                f'<a class="tile" href="{rel}realisations/{m["slug"]}.html"><img src="{self.img(m.get("image"), m["title"], rel)}" alt="" loading="lazy"><span class="tile-label">{e(m["title"])}</span></a>'
                for m in c["markets"])
            four = " four" if len(c["markets"]) == 4 else ""
            svcs = "".join(
                f'<a class="card" href="{rel}services/{s["slug"]}.html" style="text-decoration:none"><img src="{self.img(s.get("image"), s["title"], rel)}" alt="" loading="lazy"><h3>{e(s["title"])}</h3><p class="muted">{e(s.get("intro", ""))}</p></a>'
                for s in c["services"])
            news = "".join(
                f'<article class="card"><span class="label">{e(fr_date(n.get("date", "")))}</span><h3>{e(n["title"])}</h3><p>{e(n.get("summary", ""))}</p></article>'
                for n in c.get("news", [])[:3])
            h = c["home"]
            return f'''<section class="hero" aria-label="Réalisations à la une">{s_html}<div class="hero-mark">{mark}</div>
<div class="hero-caption label">{e(slides[0].get("caption", ""))}</div><div class="hero-dots">{dots}</div></section>
{self.tagline()}
<section class="section"><div class="wrap split"><div><h2>{e(h["intro_heading"])}</h2></div><div><p class="lede">{e(h["intro"])}</p><a class="btn ghost" href="{rel}a-propos.html">DÉCOUVRIR LE SALON</a></div></div></section>
<section class="section" style="padding-top:0"><div class="wrap"><h2>nos réalisations</h2><div class="grid tiles{four}">{tiles}</div></div></section>
<section class="section" style="padding-top:0"><div class="wrap"><h2>nos prestations</h2><div class="grid cards4">{svcs}</div></div></section>
{f'<section class="section" style="padding-top:0"><div class="wrap"><h2>actualités</h2><div class="grid cards3">{news}</div></div></section>' if news else ""}
<section class="section cta"><div class="wrap"><h2>{e(h["cta_heading"])}</h2><a class="btn" href="{rel}contact.html">{e(h["cta_button"])}</a></div></section>'''

        self.page("index.html", "Accueil", body, "index.html", home=True)

    def about(self):
        a = self.cfg["about"]

        def body(rel):
            paras = "".join(f"<p>{e(p)}</p>" for p in a.get("body", []))
            vals = "".join(f'<div><h3>{e(v["title"])}</h3><p class="muted">{e(v["body"])}</p></div>' for v in a.get("values", []))
            return f'''{self.inner_head("le salon", a["intro"])}
<section class="section" style="padding-top:0"><div class="wrap split"><img src="{self.img(a.get("image"), "salon", rel)}" alt=""><div class="prose">{paras}<a class="btn ghost" href="{rel}equipe.html">RENCONTRER L’ÉQUIPE</a></div></div></section>
{f'<section class="section" style="padding-top:0"><div class="wrap grid values">{vals}</div></section>' if vals else ""}'''

        self.page("a-propos.html", "Le salon", body, "a-propos.html")

    def team(self):
        def body(rel):
            ppl = "".join(
                f'<article class="card person"><img src="{self.img(p.get("photo"), p["name"], rel)}" alt="{e(p["name"])}" loading="lazy"><h3>{e(p["name"])}</h3><span class="label">{e(p.get("role", ""))}</span>{para(p.get("bio"))}</article>'
                for p in self.cfg["team"])
            return f'{self.inner_head("l’équipe", self.cfg.get("team_intro", "Les talents qui prennent soin de vos cheveux."))}<section class="section" style="padding-top:0"><div class="wrap grid cards4">{ppl}</div></section>'

        self.page("equipe.html", "L’équipe", body, "equipe.html")

    def careers(self):
        ca = self.cfg["careers"]

        def body(rel):
            ben = "".join(f"<li>{e(b)}</li>" for b in ca.get("benefits", []))
            jobs = "".join(
                f'<li><strong>{e(j["title"])}</strong> <span class="muted">— {e(j.get("location", ""))} · {e(j.get("type", ""))}</span>'
                + (f' <a href="{e(j["link"])}">postuler</a>' if j.get("link") else "") + "</li>"
                for j in ca.get("openings", []))
            jobs = jobs or '<li class="muted">Aucun poste ouvert pour le moment — les candidatures spontanées sont toujours les bienvenues.</li>'
            email = self.cfg["contact"].get("email", "")
            return f'''{self.inner_head("recrutement", ca["intro"])}
<section class="section" style="padding-top:0"><div class="wrap split" style="align-items:start">
<div><h3>postes ouverts</h3><ul class="list-clean">{jobs}</ul></div>
<div><h3>pourquoi nous rejoindre</h3><ul class="list-clean">{ben}</ul>{f'<p style="margin-top:28px"><a class="btn" href="mailto:{e(email)}">ENVOYER VOTRE CV</a></p>' if email else ""}</div></div></section>'''

        self.page("recrutement.html", "Recrutement", body, "recrutement.html")

    def projects(self):
        c = self.cfg

        def body(rel):
            tiles = "".join(
                f'<a class="tile" href="{rel}realisations/{m["slug"]}.html"><img src="{self.img(m.get("image"), m["title"], rel)}" alt="" loading="lazy"><span class="tile-label">{e(m["title"])}</span></a>'
                for m in c["markets"])
            four = " four" if len(c["markets"]) == 4 else ""
            return f'{self.inner_head("réalisations", c.get("projects_intro", ""))}<section class="section" style="padding-top:0"><div class="wrap grid tiles{four}">{tiles}</div></section>'

        self.page("realisations.html", "Réalisations", body, "realisations.html")
        for m in c["markets"]:
            def mbody(rel, m=m):
                cards = "".join(
                    f'<article class="card"><img src="{self.img(p.get("image"), p["title"], rel)}" alt="{e(p["title"])}" loading="lazy"><h3>{e(p["title"])}</h3><span class="label">{e(p.get("location", ""))}{(" · " + e(p["year"])) if p.get("year") else ""}</span>{para(p.get("summary"))}</article>'
                    for p in m.get("projects", []))
                return f'{self.inner_head(m["title"], m.get("intro", ""))}<section class="section" style="padding-top:0"><div class="wrap grid cards3">{cards}</div><div class="wrap" style="margin-top:48px"><a class="btn ghost" href="{rel}projects.html">TOUTES LES RÉALISATIONS</a></div></section>'
            self.page(f"realisations/{m['slug']}.html", m["title"].capitalize(), mbody, f"realisations/{m['slug']}.html")

    def services(self):
        c = self.cfg

        def body(rel):
            cards = "".join(
                f'<a class="card" href="{rel}services/{s["slug"]}.html" style="text-decoration:none"><img src="{self.img(s.get("image"), s["title"], rel)}" alt="" loading="lazy"><h3>{e(s["title"])}</h3><p class="muted">{e(s.get("intro", ""))}</p></a>'
                for s in c["services"])
            return f'{self.inner_head("prestations", c.get("services_intro", ""))}<section class="section" style="padding-top:0"><div class="wrap grid cards4">{cards}</div></section>'

        self.page("services.html", "Prestations", body, "services.html")
        for s in c["services"]:
            def sbody(rel, s=s):
                pts = "".join(f"<li>{e(p)}</li>" for p in s.get("points", []))
                return f'''<div class="page-hero"><img src="{self.img(s.get("image"), s["title"], rel)}" alt=""></div>
{self.inner_head(s["title"], s.get("intro", ""))}
<section class="section" style="padding-top:0"><div class="wrap split" style="align-items:start"><ul class="list-clean">{pts}</ul>
<div><p class="muted">Envie de changement ? Réservez votre rendez-vous.</p><a class="btn" href="{rel}contact.html">PRENDRE RENDEZ-VOUS</a></div></div></section>'''
            self.page(f"services/{s['slug']}.html", s["title"].capitalize(), sbody, f"services/{s['slug']}.html")

    def news(self):
        def body(rel):
            items = "".join(
                f'<article class="news-item"><img src="{self.img(n.get("image"), n["title"], rel)}" alt="" loading="lazy"><div><span class="label muted">{e(fr_date(n.get("date", "")))}</span><h3>{e(n["title"])}</h3><p>{e(n.get("summary", ""))}</p>'
                + (f'<a class="label" style="color:var(--accent);font-size:12px" href="{e(n["link"])}">LIRE LA SUITE</a>' if n.get("link") else "") + "</div></article>"
                for n in self.cfg.get("news", []))
            return f'{self.inner_head("actualités", self.cfg.get("news_intro", "Les nouvelles du salon."))}<section class="section" style="padding-top:0"><div class="wrap">{items}</div></section>'

        self.page("actualites.html", "Actualités", body, "actualites.html")

    def contact(self):
        ct = self.cfg["contact"]

        def body(rel):
            action = ct.get("form_action") or f'mailto:{ct.get("email", "")}'
            enc = '' if ct.get("form_action") else ' enctype="text/plain"'
            locs = "".join(
                f'<div style="margin-bottom:28px"><h3>{e(l["city"])}</h3><p>' + "<br>".join(e(x) for x in l.get("lines", []))
                + (f'<br>Tél. {e(l["phone"])}' if l.get("phone") else "") + "</p></div>"
                for l in self.cfg["locations"])
            return f'''{self.inner_head("contact", ct.get("intro", ""))}
<section class="section" style="padding-top:0"><div class="wrap split" style="align-items:start">
<form action="{e(action)}" method="post"{enc}>
<div class="field"><label for="n">Nom</label><input id="n" name="name" required autocomplete="name"></div>
<div class="field"><label for="em">E-mail</label><input id="em" name="email" type="email" required autocomplete="email"></div>
<div class="field"><label for="tel">Téléphone</label><input id="tel" name="telephone" type="tel" autocomplete="tel"></div>
<div class="field"><label for="msg">Votre demande (prestation, date souhaitée…)</label><textarea id="msg" name="message" rows="6" required></textarea></div>
<button class="btn" type="submit">ENVOYER</button></form>
<div>{locs}</div></div></section>'''

        self.page("contact.html", "Contact", body, "contact.html")

    def build(self):
        if self.out.exists():
            shutil.rmtree(self.out)
        (self.out / "assets").mkdir(parents=True)
        shutil.copy2(ASSETS / "styles.css", self.out / "assets" / "styles.css")
        shutil.copy2(ASSETS / "main.js", self.out / "assets" / "main.js")
        for step in (self.home, self.about, self.team, self.careers, self.projects, self.services, self.news, self.contact):
            step()
        pages = sorted(str(p.relative_to(self.out)) for p in self.out.rglob("*.html"))
        print(f"{len(pages)} pages générées dans {self.out} :")
        for p in pages:
            print("  " + p)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    Site(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "dist").build()
