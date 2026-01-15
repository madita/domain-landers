import os
import re
from pathlib import Path
from datetime import datetime

def load_domains():
    path = Path("domains.txt")
    if not path.exists():
        raise RuntimeError("domains.txt not found")

    return [d.strip().lower() for d in path.read_text().splitlines() if d.strip()]



# ==== CONFIG YOU SHOULD EDIT ====
GA4_MEASUREMENT_ID = "G-XXXXXXXXXX"  # <-- replace with your GA4 Measurement ID
FOOTER_OWNER = "Madita"             # <-- change if you like
# =================================

def clean_domains(raw: str):
    domains = load_domains()
    for line in raw.strip().splitlines():
        d = line.strip()
        if not d:
            continue
        d = re.sub(r"\s*\(.*?\)\s*", "", d)  # remove parenthetical notes
        domains.append(d.lower())
    seen = set()
    out = []
    for d in domains:
        if d not in seen:
            seen.add(d)
            out.append(d)
    return out

def classify(domain: str):
    d = domain.lower()
    if any(k in d for k in ["toolsuite", "toolshed", "webmastertools", "toolshub", "cybertool", "digitaltool"]):
        return "tools_directory"
    if any(k in d for k in ["ai", "aicondense", "aiabridged", "synthetic", "archivewithai", "aicollector", "summaries", "zusammenfass", "venturesummaries", "madsummaries"]):
        return "summaries_ai"
    if any(k in d for k in ["futuristwebdev", "nextgenwebdev", "codewithai", "aidevsolutions"]):
        return "dev_ai_services"
    if any(k in d for k in ["hustle", "sidequest", "neben", "horizonte"]):
        return "hustle"
    if any(k in d for k in ["experiment", "erkundung", "entdeck", "ideenexperimente", "neugier", "lab"]):
        return "experiments"
    if any(k in d for k in ["discworld", "scheibenwelt", "ankh-morpork", "pseudopolisplatz", "vetinari", "swrpg", "discworlders"]):
        return "discworld_fandom"
    if any(k in d for k in ["naechste", "ausfahrt", "entdeckungsreiseblog"]):
        return "travel"
    if any(k in d for k in ["gecko", "otter", "vollwieeinotter", "vweo", "fairytalegeckos", "happyasa"]):
        return "whimsy_animals"
    if any(k in d for k in ["fellowship", "geeksunite", "thronsaal", "diegilde"]):
        return "community"
    if "disorganizer" in d:
        return "productivity"
    if any(k in d for k in ["madita", "madwort", "madrone"]):
        return "personal_brand"
    if "fabricatidiem" in d:
        return "motto_brand"
    return "generic"

def pretty_name(domain: str):
    base = domain.split(".")[0].replace("-", " ")
    return " ".join(w.capitalize() for w in base.split())

def seo_pack(domain: str, theme: str):
    name = pretty_name(domain)
    packs = {
        "tools_directory": {
            "title": f"{name} — Curated AI & Dev Tools Directory (Coming Soon)",
            "desc": "Discover the best AI, developer, productivity, and automation tools — curated, summarized, and updated frequently. Join the newsletter for early access.",
            "keywords": "AI tools directory, developer tools, productivity tools, automation tools, SaaS directory, best tools, tool reviews"
        },
        "summaries_ai": {
            "title": f"{name} — AI Summaries & TL;DR Hub (Coming Soon)",
            "desc": "Fast, high-signal AI summaries of tools, articles, videos, and trends. Subscribe to get weekly TL;DR updates and early access.",
            "keywords": "AI summaries, TLDR, article summaries, video summaries, research summaries, curated newsletter, condensed knowledge"
        },
        "dev_ai_services": {
            "title": f"{name} — AI-Powered Web Development & Automation (Coming Soon)",
            "desc": "Modern Laravel/Vue web development and AI automation for businesses. Subscribe for launch updates and early client slots.",
            "keywords": "Laravel developer, Vue.js developer, web development freelance, AI automation, custom web apps, API integrations, Germany"
        },
        "hustle": {
            "title": f"{name} — AI-Assisted Side Hustle Ideas & Playbooks (Coming Soon)",
            "desc": "Automated research and bite-sized playbooks for realistic side hustles. Get weekly ideas, tools, and experiments you can ship.",
            "keywords": "side hustle ideas, make money online, business ideas, automation, AI tools for business, indie hacking, newsletter"
        },
        "experiments": {
            "title": f"{name} — Experiments in Tech, AI & Growth (Coming Soon)",
            "desc": "A living lab of experiments: tools, workflows, and mini-projects—summarized so you can learn fast. Newsletter launching soon.",
            "keywords": "tech experiments, AI experiments, growth experiments, automation workflows, project ideas, indie maker"
        },
        "discworld_fandom": {
            "title": f"{name} — Discworld Hub & Community Projects (Coming Soon)",
            "desc": "A fan hub for Discworld: curated lore, roleplay resources, timelines, and community projects. Subscribe for launch updates.",
            "keywords": "Discworld, Scheibenwelt, Ankh-Morpork, Terry Pratchett, roleplay, fan community, lore"
        },
        "travel": {
            "title": f"{name} — Smart Travel Inspiration & Mini Guides (Coming Soon)",
            "desc": "Automated travel inspiration with short mini guides and curated links. Subscribe to get new routes and destination ideas.",
            "keywords": "travel blog, travel inspiration, mini guides, weekend trips, Germany travel, itineraries, travel newsletter"
        },
        "whimsy_animals": {
            "title": f"{name} — Whimsical Stories & Animal Joy (Coming Soon)",
            "desc": "A playful corner of the internet: geckos, otters, stories, and bite-sized joy. Join the newsletter for early drops.",
            "keywords": "gecko, otter, cute stories, animal facts, whimsical blog, merch, newsletter"
        },
        "community": {
            "title": f"{name} — Community HQ for Makers & Geeks (Coming Soon)",
            "desc": "A friendly HQ for makers: curated links, projects, and resources. Subscribe to get the first invites.",
            "keywords": "geek community, maker community, resources, newsletter, events, projects, knowledge hub"
        },
        "productivity": {
            "title": f"{name} — Productivity, Organization & Automation (Coming Soon)",
            "desc": "Tools and workflows to organize chaos: checklists, templates, and automation ideas. Get early access via the newsletter.",
            "keywords": "productivity, organization, automation workflows, templates, task management, knowledge management"
        },
        "personal_brand": {
            "title": f"{name} — Studio & Digital Projects (Coming Soon)",
            "desc": "A studio of web development, automation, and experiments. Subscribe for updates and early previews.",
            "keywords": "web developer, Laravel, Vue.js, automation, freelance developer, portfolio, side projects"
        },
        "motto_brand": {
            "title": f"{name} — Make The Day Count (Coming Soon)",
            "desc": "A small brand around focused effort and playful experimentation—projects, tools, and writing. Subscribe for the first release.",
            "keywords": "motivation, productivity, experiments, projects, newsletter, make the day count"
        },
        "generic": {
            "title": f"{name} — New Project Launching Soon",
            "desc": "A new project is launching soon. Subscribe for early access, updates, and the first public release.",
            "keywords": "coming soon, newsletter, launch, early access, updates"
        }
    }
    return packs.get(theme, packs["generic"])

def render_thanks(domain: str, title: str):
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
      margin:0; font-family: system-ui, -apple-system, Segoe UI, Roboto, Inter, Arial, sans-serif;
      background:#070b12; color: rgba(255,255,255,0.92); min-height:100vh;
      display:flex; align-items:center; justify-content:center; padding: 24px;
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
    <p>We’ll email you when the project launches. Meanwhile, feel free to share this page with someone who’d love it.</p>
    <p><a href="/">← Back to {title}</a></p>
  </div>
</body>
</html>
"""

def render_index(domain: str, seo: dict):
    year = datetime.utcnow().year
    form_name = f"newsletter-{domain}"  # unique form per domain (helps filtering)
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
    gtag('config', '{GA4_MEASUREMENT_ID}', {{ 'send_page_view': true }});
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
              name="{form_name}"
              method="POST"
              data-netlify="true"
              data-netlify-honeypot="bot-field"
              action="/thanks.html"
              id="signup-form">
          <input type="hidden" name="form-name" value="{form_name}">
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
        · <a href="#" onclick="alert('Add your privacy page later.'); return false;">Privacy</a>
        · <a href="#" onclick="alert('Add your imprint later (esp. for .de).'); return false;">Imprint</a>
      </div>
    </div>
  </main>

  <script>
    // Track submit attempt (Netlify redirects to /thanks.html on success)
    const form = document.getElementById('signup-form');
    const note = document.getElementById('signup-note');
    form.addEventListener('submit', function() {{
      try {{
        gtag('event', 'newsletter_signup_attempt', {{
          event_category: 'conversion',
          event_label: '{domain}'
        }});
      }} catch(e) {{}}
      note.textContent = "Thanks — submitting…";
    }});
  </script>
</body>
</html>
"""

def main():
    out_dir = Path("output")
    out_dir.mkdir(exist_ok=True)

    domains = clean_domains(DOMAINS_RAW)
    for domain in domains:
        theme = classify(domain)
        seo = seo_pack(domain, theme)

        domain_dir = out_dir / domain
        domain_dir.mkdir(parents=True, exist_ok=True)

        (domain_dir / "index.html").write_text(render_index(domain, seo), encoding="utf-8")
        (domain_dir / "thanks.html").write_text(render_thanks(domain, seo["title"]), encoding="utf-8")

    print(f"Generated {len(domains)} Netlify landing pages in: {out_dir.resolve()}")

if __name__ == "__main__":
    main()
