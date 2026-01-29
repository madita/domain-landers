import os
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# =====================
# ENV CONFIG (per Netlify site)
# =====================
DOMAIN = os.getenv("DOMAIN", "").strip().lower()
GA4_MEASUREMENT_ID = os.getenv("GA4_MEASUREMENT_ID", "").strip()
FOOTER_OWNER = os.getenv("FOOTER_OWNER", "Madita").strip()

if not DOMAIN:
    raise RuntimeError("Missing DOMAIN env var (e.g. cybertoolsuite.com)")
if not GA4_MEASUREMENT_ID:
    raise RuntimeError("Missing GA4_MEASUREMENT_ID env var (e.g. G-XXXXXXXXXX)")

# =====================
# HELPERS
# =====================
def pretty_name(domain: str) -> str:
    base = domain.split(".")[0].replace("-", " ")
    return " ".join(w.capitalize() for w in base.split())

def classify(domain: str) -> str:
    d = domain
    if any(k in d for k in ["toolsuite", "toolshed", "toolshub", "webmastertools", "cybertool", "digitaltool"]):
        return "tools"
    if any(k in d for k in ["ai", "abridged", "summary", "summaries", "condense", "archivewithai", "collector", "zusammenfass"]):
        return "summaries"
    if any(k in d for k in ["webdev", "codewith", "aidev", "nextgenwebdev", "futuristwebdev"]):
        return "dev"
    if any(k in d for k in ["hustle", "sidequest", "neben", "horizonte"]):
        return "hustle"
    if any(k in d for k in ["experiment", "lab", "erkundung", "ideenexperimente", "neugier"]):
        return "experiments"
    if any(k in d for k in ["discworld", "scheibenwelt", "ankh-morpork", "vetinari", "pseudopolisplatz"]):
        return "discworld"
    if any(k in d for k in ["gecko", "otter", "vollwieeinotter"]):
        return "whimsy"
    if any(k in d for k in ["naechste", "ausfahrt", "entdeckungsreise"]):
        return "travel"
    return "generic"

def seo_pack(domain: str, theme: str) -> dict:
    name = pretty_name(domain)
    packs = {
        "tools": {
            "title": f"{name} — Curated AI & Dev Tools (Coming Soon)",
            "desc": "Discover curated AI, developer, productivity, and automation tools — summarized and updated. Join the newsletter for early access.",
            "keywords": "AI tools, developer tools, productivity tools, automation tools, SaaS directory"
        },
        "summaries": {
            "title": f"{name} — AI Summaries & TL;DR (Coming Soon)",
            "desc": "High-signal AI summaries of tools, articles, videos, and trends. Subscribe for early access and weekly digests.",
            "keywords": "AI summaries, TLDR, article summaries, video summaries, condensed knowledge"
        },
        "dev": {
            "title": f"{name} — AI-Powered Web Development (Coming Soon)",
            "desc": "Modern Laravel + Vue development and AI automation services. Subscribe for launch updates and early client slots.",
            "keywords": "Laravel developer, Vue.js developer, web development, freelance developer, AI automation"
        },
        "hustle": {
            "title": f"{name} — Side Hustle Ideas You Can Ship (Coming Soon)",
            "desc": "Curated and automated side-hustle ideas with tools and mini playbooks. Subscribe for the weekly digest.",
            "keywords": "side hustle ideas, business ideas, make money online, automation"
        },
        "experiments": {
            "title": f"{name} — Experiments in Tech & AI (Coming Soon)",
            "desc": "A living lab of small experiments in tech, AI, and growth. Subscribe to follow along and get updates.",
            "keywords": "tech experiments, AI experiments, indie projects, maker"
        },
        "discworld": {
            "title": f"{name} — Discworld Fan Hub (Coming Soon)",
            "desc": "A curated Discworld fan hub for lore, roleplay, and community projects. Subscribe for launch updates.",
            "keywords": "Discworld, Scheibenwelt, Ankh-Morpork, Terry Pratchett, roleplay"
        },
        "whimsy": {
            "title": f"{name} — Whimsical Internet Project (Coming Soon)",
            "desc": "A playful, experimental corner of the internet. Subscribe to see what emerges next.",
            "keywords": "whimsical project, creative experiments, cute animals"
        },
        "travel": {
            "title": f"{name} — Smart Travel Mini Guides (Coming Soon)",
            "desc": "Travel inspiration with short, useful mini guides and curated links. Subscribe for early access.",
            "keywords": "travel inspiration, mini guides, weekend trips, itineraries"
        },
        "generic": {
            "title": f"{name} — New Project Launching Soon",
            "desc": "A new project is launching soon. Subscribe for early access and launch updates.",
            "keywords": "coming soon, newsletter, launch"
        }
    }
    return packs.get(theme, packs["generic"])

# =====================
# HTML (Netlify Forms + GA4 events)
# =====================
def render_index(domain: str, seo: dict) -> str:
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
  <meta property="og:title" content="{seo['title']}">
  <meta property="og:description" content="{seo['desc']}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://{domain}/">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="theme-color" content="#0b1220">

  <!-- Google Analytics (GA4) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id={GA4_MEASUREMENT_ID}"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', '{GA4_MEASUREMENT_ID}');
  </script>

  <style>
    :root {{
      --bg: #070b12;
      --card: rgba(255,255,255,0.06);
      --text: rgba(255,255,255,0.92);
      --muted: rgba(255,255,255,0.70);
      --line: rgba(255,255,255,0.12);
      --accent: #7dd3fc;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Inter, Arial, sans-serif;
      color: var(--text);
      background: radial-gradient(1200px 800px at 20% 0%, rgba(125,211,252,0.18), transparent 55%),
                  radial-gradient(900px 700px at 80% 20%, rgba(167,139,250,0.12), transparent 60%),
                  var(--bg);
      min-height: 100vh;
    }}
    .wrap {{
      max-width: 980px;
      margin: 0 auto;
      padding: 56px 20px 40px;
    }}
    .top {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      margin-bottom: 24px;
    }}
    .badge {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      font-size: 12px;
      padding: 8px 12px;
      border: 1px solid var(--line);
      border-radius: 999px;
      background: rgba(255,255,255,0.04);
      color: var(--muted);
    }}
    .dot {{
      width: 8px; height: 8px; border-radius: 50%;
      background: var(--accent);
      box-shadow: 0 0 18px rgba(125,211,252,0.8);
    }}
    h1 {{
      font-size: 40px;
      line-height: 1.1;
      margin: 10px 0 12px;
      letter-spacing: -0.02em;
    }}
    p {{
      margin: 0 0 14px;
      color: var(--muted);
      font-size: 16px;
      line-height: 1.6;
    }}
    .grid {{
      display: grid;
      grid-template-columns: 1.2fr 0.8fr;
      gap: 18px;
      margin-top: 22px;
    }}
    .card {{
      border: 1px solid var(--line);
      background: var(--card);
      border-radius: 18px;
      padding: 18px;
    }}
    .card h2 {{
      margin: 0 0 10px;
      font-size: 16px;
    }}
    .list {{
      margin: 10px 0 0;
      padding: 0 0 0 18px;
      color: var(--muted);
      line-height: 1.7;
      font-size: 14px;
    }}
    .cta {{
      display: grid;
      gap: 10px;
      margin-top: 12px;
    }}
    input[type="email"] {{
      width: 100%;
      padding: 12px 12px;
      border-radius: 12px;
      border: 1px solid var(--line);
      background: rgba(0,0,0,0.18);
      color: var(--text);
      outline: none;
      font-size: 14px;
    }}
    button {{
      width: 100%;
      padding: 12px 12px;
      border-radius: 12px;
      border: 1px solid rgba(125,211,252,0.35);
      background: rgba(125,211,252,0.14);
      color: var(--text);
      font-weight: 600;
      cursor: pointer;
    }}
    button:hover {{
      background: rgba(125,211,252,0.22);
    }}
    .fine {{
      font-size: 12px;
      color: rgba(255,255,255,0.55);
      margin-top: 8px;
    }}
    .footer {{
      margin-top: 26px;
      border-top: 1px solid var(--line);
      padding-top: 14px;
      display: flex;
      justify-content: space-between;
      gap: 10px;
      flex-wrap: wrap;
      color: rgba(255,255,255,0.55);
      font-size: 12px;
    }}
    a {{ color: rgba(125,211,252,0.92); text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    @media (max-width: 880px) {{
      .grid {{ grid-template-columns: 1fr; }}
      h1 {{ font-size: 34px; }}
    }}
  </style>
</head>
<body>
  <main class="wrap">
    <div class="top">
      <div class="badge"><span class="dot"></span> Coming soon · validating interest</div>
      <div class="badge">{domain}</div>
    </div>

    <h1>{seo['title']}</h1>
    <p>{seo['desc']}</p>

    <div class="grid">
      <section class="card">
        <h2>What this will become</h2>
        <ul class="list">
          <li><strong>High-signal content</strong> (curated + summarized)</li>
          <li><strong>Searchable pages</strong> designed for SEO</li>
          <li><strong>Regular updates</strong> driven by automation</li>
          <li><strong>Built by a web developer</strong> (Laravel/Vue, APIs, automations)</li>
        </ul>

        <div class="fine">
          SEO keywords: <em>{seo['keywords']}</em>
        </div>
      </section>

      <aside class="card">
        <h2>Get early access</h2>
        <p>Join the list to get the first invite + launch perks. No spam.</p>

        <!-- Netlify Form -->
        <form class="cta"
              name="newsletter-{domain}"
              method="POST"
              data-netlify="true"
              data-netlify-honeypot="bot-field"
              action="/thanks.html"
              id="signup-form">
          <input type="hidden" name="form-name" value="newsletter-{domain}">
          <input type="hidden" name="domain" value="{domain}">

          <!-- honeypot -->
          <p style="display:none;">
            <label>Don’t fill this out: <input name="bot-field" /></label>
          </p>

          <input type="email" name="email" placeholder="you@domain.com" required>
          <button type="submit" id="signup-btn">Notify me</button>
        </form>

        <div class="fine" id="signup-note">
          By subscribing you agree to receive launch updates. Unsubscribe anytime.
        </div>
      </aside>
    </div>

    <div class="footer">
      <div>© {year} {FOOTER_OWNER}. All rights reserved.</div>
      <div>
        <a href="#" onclick="gtag('event','cta_click',{{'event_category':'engagement','event_label':'{domain}'}}); return false;">Tracked CTA</a>
      </div>
    </div>
  </main>

  <script>
    document.getElementById('signup-form').addEventListener('submit', function() {{
      try {{
        gtag('event', 'newsletter_signup_attempt', {{
          event_category: 'conversion',
          event_label: '{domain}'
        }});
      }} catch(e) {{}}
      document.getElementById('signup-note').textContent = "Thanks — submitting…";
    }});
  </script>
</body>
</html>
"""

def render_thanks(domain: str) -> str:
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
    gtag('event', 'newsletter_signup', {{ event_category: 'conversion', event_label: '{domain}' }});
  </script>

  <style>
    body {{
      margin:0;
      font-family: system-ui, -apple-system, Segoe UI, Roboto, Inter, Arial, sans-serif;
      background:#070b12;
      color: rgba(255,255,255,0.92);
      min-height:100vh;
      display:flex;
      align-items:center;
      justify-content:center;
      padding: 24px;
    }}
    .card {{
      max-width: 720px; width:100%;
      border: 1px solid rgba(255,255,255,0.12);
      background: rgba(255,255,255,0.06);
      border-radius: 18px; padding: 22px;
    }}
    h1 {{ margin:0 0 10px; font-size: 26px; }}
    p {{ margin:0 0 16px; color: rgba(255,255,255,0.75); line-height:1.6; }}
    a {{ color: rgba(125,211,252,0.92); text-decoration:none; }}
    a:hover {{ text-decoration:underline; }}
  </style>
</head>
<body>
  <div class="card">
    <h1>You're on the list ✅</h1>
    <p>Thanks for subscribing to <strong>{domain}</strong>.</p>
    <p><a href="/">← Back</a></p>
  </div>
</body>
</html>
"""

def main():
    theme = classify(DOMAIN)
    seo = seo_pack(DOMAIN, theme)

    out_dir = Path("output")
    out_dir.mkdir(exist_ok=True)

    (out_dir / "index.html").write_text(render_index(DOMAIN, seo), encoding="utf-8")
    (out_dir / "thanks.html").write_text(render_thanks(DOMAIN), encoding="utf-8")

    print(f"Generated landing page for {DOMAIN} into {out_dir.resolve()}")

if __name__ == "__main__":
    main()
