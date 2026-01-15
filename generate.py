import os
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

GA4_MEASUREMENT_ID = os.getenv("GA4_MEASUREMENT_ID", "").strip()
FOOTER_OWNER = os.getenv("FOOTER_OWNER", "Madita").strip()
DOMAINS_RAW = os.getenv("DOMAINS", "").strip()

if not GA4_MEASUREMENT_ID:
    raise RuntimeError("Missing GA4_MEASUREMENT_ID env var")

if not DOMAINS_RAW:
    raise RuntimeError("Missing DOMAINS env var (use \\n between domains)")

def load_domains(raw: str):
    # Netlify env vars are single-line; we encode newlines as "\n"
    domains = [d.strip().lower() for d in raw.split("\\n") if d.strip()]
    # dedupe preserving order
    seen = set()
    out = []
    for d in domains:
        if d not in seen:
            seen.add(d)
            out.append(d)
    return out

def pretty_name(domain: str):
    base = domain.split(".")[0].replace("-", " ")
    return " ".join(w.capitalize() for w in base.split())

def classify(domain: str):
    d = domain.lower()
    if any(k in d for k in ["toolsuite", "toolshed", "webmastertools", "toolshub", "cybertool", "digitaltool"]):
        return "tools"
    if any(k in d for k in ["ai", "abridged", "condense", "summary", "summaries", "archivewithai", "collector", "zusammenfass"]):
        return "summaries"
    if any(k in d for k in ["webdev", "codewith", "aidev", "nextgenwebdev", "futuristwebdev"]):
        return "dev"
    if any(k in d for k in ["hustle", "sidequest", "neben", "horizonte"]):
        return "hustle"
    if any(k in d for k in ["experiment", "lab", "erkundung", "ideenexperimente", "neugier"]):
        return "experiments"
    if any(k in d for k in ["discworld", "scheibenwelt", "ankh-morpork", "vetinari", "pseudopolisplatz"]):
        return "discworld"
    if any(k in d for k in ["gecko", "otter"]):
        return "whimsy"
    if any(k in d for k in ["naechste", "ausfahrt", "entdeckungsreise"]):
        return "travel"
    return "generic"

def seo_pack(domain: str, theme: str):
    name = pretty_name(domain)
    packs = {
        "tools": {
            "title": f"{name} — Curated AI & Dev Tools (Coming Soon)",
            "desc": "Discover the best AI, developer, productivity, and automation tools — curated and summarized. Join the newsletter for early access.",
            "keywords": "AI tools, developer tools, productivity tools, automation tools, SaaS directory"
        },
        "summaries": {
            "title": f"{name} — AI Summaries & TL;DR (Coming Soon)",
            "desc": "Fast, high-signal AI summaries of tools, articles, videos, and trends. Subscribe for early access.",
            "keywords": "AI summaries, TLDR, article summaries, video summaries, condensed knowledge"
        },
        "dev": {
            "title": f"{name} — AI-Powered Web Development (Coming Soon)",
            "desc": "Modern Laravel + Vue development and automation. Subscribe for launch updates and early client slots.",
            "keywords": "Laravel developer, Vue.js developer, web development, freelance developer, AI automation"
        },
        "hustle": {
            "title": f"{name} — Side Hustle Ideas You Can Ship (Coming Soon)",
            "desc": "Curated, realistic side-hustle ideas with tools and mini playbooks. Get the weekly digest.",
            "keywords": "side hustle ideas, business ideas, make money online, automation"
        },
        "experiments": {
            "title": f"{name} — Experiments in Tech & AI (Coming Soon)",
            "desc": "A living lab of small experiments in tech, AI, and growth. Subscribe to follow along.",
            "keywords": "tech experiments, AI experiments, indie projects, maker"
        },
        "discworld": {
            "title": f"{name} — Discworld Fan Hub (Coming Soon)",
            "desc": "A fan hub for Discworld: curated lore, roleplay resources, and community projects. Subscribe for updates.",
            "keywords": "Discworld, Scheibenwelt, Ankh-Morpork, Terry Pratchett, roleplay"
        },
        "whimsy": {
            "title": f"{name} — Whimsical Internet Project (Coming Soon)",
            "desc": "A playful, experimental corner of the internet. Subscribe to see what emerges.",
            "keywords": "whimsical project, creative experiments, cute animals"
        },
        "travel": {
            "title": f"{name} — Smart Travel Mini Guides (Coming Soon)",
            "desc": "Travel inspiration with short, useful mini guides and curated links. Subscribe for early access.",
            "keywords": "travel inspiration, mini guides, weekend trips, itineraries"
        },
        "generic": {
            "title": f"{name} — New Project Launching Soon",
            "desc": "A new project is launching soon. Subscribe for early access and updates.",
            "keywords": "coming soon, newsletter, launch"
        }
    }
    return packs.get(theme, packs["generic"])

def render_index(domain: str, seo: dict):
    year = datetime.utcnow().year
    form_name = f"newsletter-{domain}"
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{seo['title']}</title>
  <meta name="description" content="{seo['desc']}">
  <meta name="keywords" content="{seo['keywords']}">
  <meta name="robots" content="index,follow">
  <link rel="canonical" href="https://{domain}/">

  <script async src="https://www.googletagmanager.com/gtag/js?id={GA4_MEASUREMENT_ID}"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', '{GA4_MEASUREMENT_ID}');
  </script>

  <style>
    body {{ margin:0; font-family: system-ui, -apple-system, Segoe UI, Roboto, Inter, Arial, sans-serif; background:#070b12; color:#fff; }}
    main {{ max-width: 960px; margin: 0 auto; padding: 56px 20px; }}
    .card {{ margin-top: 22px; padding: 18px; border-radius: 16px; background: rgba(255,255,255,0.06); }}
    input,button {{ width: 100%; padding: 12px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.12); background: rgba(0,0,0,0.25); color: #fff; }}
    button {{ background: rgba(125,211,252,0.18); border-color: rgba(125,211,252,0.35); cursor: pointer; font-weight: 600; }}
    button:hover {{ background: rgba(125,211,252,0.28); }}
    .muted {{ color: rgba(255,255,255,0.72); line-height: 1.6; }}
    footer {{ margin-top: 34px; font-size: 12px; color: rgba(255,255,255,0.55); }}
  </style>
</head>
<body>
  <main>
    <h1>{seo['title']}</h1>
    <p class="muted">{seo['desc']}</p>

    <div class="card">
      <h2 style="margin:0 0 10px;">Get early access</h2>
      <p class="muted" style="margin-top:0;">Join the newsletter for launch updates. No spam.</p>

      <form name="{form_name}"
            method="POST"
            data-netlify="true"
            data-netlify-honeypot="bot-field"
            action="/thanks.html"
            id="signup-form">
        <input type="hidden" name="form-name" value="{form_name}">
        <input type="hidden" name="domain" value="{domain}">
        <p style="display:none;">
          <label>Don’t fill this out: <input name="bot-field" /></label>
        </p>

        <input type="email" name="email" placeholder="you@email.com" required>
        <button type="submit">Notify me</button>
      </form>

      <p class="muted" style="font-size:12px; margin-bottom:0;">Keywords: {seo['keywords']}</p>
    </div>

    <footer>© {year} {FOOTER_OWNER}</footer>

    <script>
      // Track submit attempt
      document.getElementById('signup-form').addEventListener('submit', function() {{
        try {{
          gtag('event','newsletter_signup_attempt',{{event_category:'conversion', event_label:'{domain}'}})
        }} catch(e) {{}}
      }});
    </script>
  </main>
</body>
</html>
"""

def render_thanks(domain: str):
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Thanks — {domain}</title>
  <meta name="robots" content="noindex,nofollow">
  <script async src="https://www.googletagmanager.com/gtag/js?id={GA4_MEASUREMENT_ID}"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', '{GA4_MEASUREMENT_ID}');
    gtag('event','newsletter_signup',{{event_category:'conversion', event_label:'{domain}'}})
  </script>
  <style>
    body {{ margin:0; font-family: system-ui, sans-serif; background:#070b12; color:#fff; padding: 56px 20px; }}
    a {{ color: rgba(125,211,252,0.95); }}
  </style>
</head>
<body>
  <h1>You’re on the list ✅</h1>
  <p>Thanks for subscribing to <strong>{domain}</strong>.</p>
  <p><a href="/">← Back</a></p>
</body>
</html>
"""

def main():
    domains = load_domains(DOMAINS_RAW)
    out = Path("output")
    out.mkdir(exist_ok=True)

    for domain in domains:
        theme = classify(domain)
        seo = seo_pack(domain, theme)

        folder = out / domain
        folder.mkdir(parents=True, exist_ok=True)

        (folder / "index.html").write_text(render_index(domain, seo), encoding="utf-8")
        (folder / "thanks.html").write_text(render_thanks(domain), encoding="utf-8")

    print(f"Generated {len(domains)} sites into {out.resolve()}")

if __name__ == "__main__":
    main()
