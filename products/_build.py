#!/usr/bin/env python3
"""Generate static product detail pages from _data.json.

Output: products/<slug>.html — one file per product.
The template mirrors the Ko-fi reference shape but uses the Leo Tan Financial visual system
(Plus Jakarta Sans heading, Roboto Serif display, navy + orange + cream palette).
"""
import json
import html
import re
from pathlib import Path

HERE = Path(__file__).parent
DATA = json.loads((HERE / "_data.json").read_text())


def esc(s):
    return html.escape(str(s), quote=True)


def render_image(p):
    img = p.get("image")
    aspect = p.get("image_aspect", "4/5")
    if img:
        # rewrite ../shop-mockup-assets/foo to absolute /shop-mockup-assets/foo
        if img.startswith("../"):
            img = "/" + img[3:]
        return (
            f'<div class="bg-cream/40 rounded-2xl overflow-hidden border border-line/60">'
            f'<img src="{esc(img)}" alt="{esc(p["title"])}" '
            f'class="w-full block" style="aspect-ratio: {aspect}; object-fit: cover;" />'
            f'</div>'
        )
    # fallback: stylised placeholder
    return (
        f'<div class="rounded-2xl border border-line/60 aspect-[4/5] flex items-center justify-center bg-gradient-to-br from-navy to-navy-dark text-white p-10 text-center">'
        f'<div><div class="text-[11px] heading uppercase tracking-widest text-white/60">{esc(p["category"])}</div>'
        f'<div class="display text-3xl font-bold mt-3 leading-tight">{esc(p["title"])}</div></div></div>'
    )


def render_what_inside(items):
    lis = "".join(
        f'<li class="flex gap-3"><span class="text-orange shrink-0 mt-1">→</span><span>{esc(x)}</span></li>'
        for x in items
    )
    return (
        '<section class="mt-10">'
        '<h2 class="display text-2xl font-bold text-navy flex items-center gap-2"><span class="text-orange">✦</span> What\'s inside</h2>'
        f'<ul class="mt-5 space-y-2.5 text-mute leading-relaxed">{lis}</ul>'
        '</section>'
    )


def render_how_to_use(steps):
    lis = "".join(
        f'<li class="flex gap-3"><span class="display text-navy font-bold shrink-0">{i+1}.</span><span>{esc(x)}</span></li>'
        for i, x in enumerate(steps)
    )
    return (
        '<section class="mt-10">'
        '<h2 class="display text-2xl font-bold text-navy flex items-center gap-2"><span class="text-orange">✦</span> How to use it</h2>'
        f'<ul class="mt-5 space-y-2.5 text-mute leading-relaxed">{lis}</ul>'
        '</section>'
    )


def render_who_for(text):
    return (
        '<section class="mt-10">'
        '<h2 class="display text-2xl font-bold text-navy flex items-center gap-2"><span class="text-orange">✦</span> Who this is for</h2>'
        f'<p class="mt-5 text-mute leading-relaxed">{esc(text)}</p>'
        '</section>'
    )


def render_deeper(text):
    return (
        '<section class="mt-10">'
        '<h2 class="display text-2xl font-bold text-navy flex items-center gap-2"><span class="text-orange">✦</span> Want to go deeper?</h2>'
        f'<p class="mt-5 text-mute leading-relaxed">{esc(text)}</p>'
        '</section>'
    )


def render_other_items(current_slug):
    others = [(s, p) for s, p in DATA.items() if s != current_slug]
    # show 3 — biased toward complementary categories
    pick = others[:3] if len(others) >= 3 else others
    cards = ""
    for slug, p in pick:
        img = p.get("image")
        if img and img.startswith("../"):
            img = "/" + img[3:]
        bg = (
            f'<img src="{esc(img)}" alt="" class="w-full h-full object-cover" />'
            if img
            else '<div class="w-full h-full bg-gradient-to-br from-navy to-navy-dark"></div>'
        )
        cards += (
            f'<a href="{esc(slug)}.html" class="group bg-white border border-line rounded-xl overflow-hidden hover:shadow-md hover:-translate-y-0.5 transition-all">'
            f'<div class="aspect-[4/5] bg-cream/40 overflow-hidden">{bg}</div>'
            f'<div class="p-4">'
            f'<div class="text-[10px] heading uppercase tracking-widest text-mute">{esc(p["category"])}</div>'
            f'<h3 class="display text-base font-semibold text-navy mt-1 leading-tight">{esc(p["title"])}</h3>'
            f'<div class="text-sm display font-bold text-navy mt-2">{esc(p["price"])}</div>'
            f'</div></a>'
        )
    return (
        '<section class="max-w-6xl mx-auto px-5 py-14 border-t border-line/60">'
        '<div class="flex items-center justify-between mb-6">'
        '<h2 class="display text-2xl font-bold text-navy">Other items in the shop</h2>'
        '<a href="/index.html" class="heading text-sm font-medium text-mute hover:text-navy">View all →</a>'
        '</div>'
        f'<div class="grid grid-cols-1 sm:grid-cols-3 gap-5">{cards}</div>'
        '</section>'
    )


def page(slug, p):
    img_block = render_image(p)
    what = render_what_inside(p.get("what_inside", []))
    how = render_how_to_use(p.get("how_to_use", []))
    who = render_who_for(p.get("who_for", "")) if p.get("who_for") else ""
    deeper = render_deeper(p.get("deeper", "")) if p.get("deeper") else ""
    other = render_other_items(slug)

    compare = (
        f'<span class="text-mute line-through ml-2 text-base">{esc(p["compare_at_price"])}</span>'
        if p.get("compare_at_price")
        else ""
    )

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{esc(p['title'])} — Leo Tan Financial</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Roboto+Serif:opsz,wght@8..144,400;8..144,500;8..144,600;8..144,700&family=Roboto:wght@400;500&display=swap" rel="stylesheet" />
  <script>
    tailwind.config = {{
      theme: {{
        extend: {{
          fontFamily: {{
            display: ["'Roboto Serif'", "system-ui", "sans-serif"],
            heading: ["'Plus Jakarta Sans'", "system-ui", "sans-serif"],
            body: ["Roboto", "system-ui", "sans-serif"],
          }},
          colors: {{
            navy: {{ DEFAULT: "#0B3D61", dark: "#082B45" }},
            orange: {{ DEFAULT: "#F68A1E", dark: "#D97408" }},
            cream: "#FEF3E2",
            ink: "#37393F",
            mute: "#54595F",
            line: "#CFD8DC",
          }},
        }},
      }},
    }};
  </script>
  <style>
    body {{ font-family: Roboto, system-ui, sans-serif; color: #37393F; }}
    h1, h2, h3, .display {{ font-family: 'Roboto Serif', serif; }}
    .heading {{ font-family: 'Plus Jakarta Sans', system-ui, sans-serif; }}
  </style>
</head>
<body class="bg-white">
  <!-- TOP BAR -->
  <header class="border-b border-line/60 sticky top-0 bg-white/95 backdrop-blur z-40">
    <div class="max-w-6xl mx-auto px-5 py-3 flex items-center justify-between">
      <a href="/index.html" class="flex items-center gap-2.5 group">
        <span class="w-9 h-9 rounded-full bg-navy text-white display font-bold flex items-center justify-center group-hover:bg-orange transition">L</span>
        <span class="heading font-semibold text-navy">Leo Tan Financial</span>
      </a>
      <a href="/index.html" class="heading text-sm text-mute hover:text-navy flex items-center gap-1.5">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
        Back to shop
      </a>
    </div>
  </header>

  <!-- HERO -->
  <main class="max-w-6xl mx-auto px-5 py-10">
    <div class="grid lg:grid-cols-[1.2fr_0.8fr] gap-10 lg:gap-14">
      <!-- LEFT: image + long-form content -->
      <div>
        {img_block}

        <!-- Description -->
        <section class="mt-10">
          <h2 class="display text-2xl font-bold text-navy">Description</h2>
          <p class="mt-4 text-lg text-ink leading-relaxed">{esc(p['tagline'])}</p>
        </section>

        {what}
        {how}
        {who}
        {deeper}

        <!-- Disclaimer -->
        <div class="mt-10 bg-cream/60 border-l-4 border-orange rounded-r-xl px-5 py-4 text-sm text-mute leading-relaxed">
          <span class="text-orange">⚠</span> This is a digital product. For personal use only. No financial advice — for that, book the 1:1 Financial Simulation. Do not resell or redistribute.
        </div>
      </div>

      <!-- RIGHT: sticky buy panel -->
      <aside class="lg:sticky lg:top-24 self-start">
        <div class="bg-white border border-line rounded-2xl p-6 shadow-sm">
          <div class="text-[11px] heading uppercase tracking-widest text-orange font-bold">{esc(p['category'])}</div>
          <h1 class="display text-3xl font-bold text-navy mt-2 leading-tight">{esc(p['title'])}</h1>

          <div class="flex items-center gap-2 mt-4 text-sm text-mute heading">
            <span class="text-amber-500">★★★★★</span>
            <span>{esc(p.get('rating', '4.9'))} · {esc(p.get('buyers', ''))}</span>
          </div>

          <div class="mt-6 pt-6 border-t border-line/60">
            <div class="flex items-baseline">
              <span class="display text-3xl font-bold text-navy">{esc(p['price'])}</span>
              {compare}
            </div>
            <p class="text-xs text-mute heading mt-1.5">One-time payment. Free updates for life.</p>
          </div>

          <button class="mt-6 w-full bg-navy hover:bg-navy-dark text-white py-3.5 rounded-lg heading font-semibold text-base transition">Buy now</button>
          <button class="mt-2.5 w-full bg-white hover:bg-cream/40 border border-line text-navy py-3.5 rounded-lg heading font-semibold text-sm transition">Add to wishlist</button>

          <p class="text-xs text-mute leading-relaxed mt-5">{esc(p['tagline'])}</p>

          <!-- Share -->
          <div class="mt-6 pt-5 border-t border-line/60 flex items-center justify-between">
            <span class="text-[11px] heading uppercase tracking-widest text-mute">Share</span>
            <div class="flex items-center gap-2">
              <button aria-label="Copy link" class="w-8 h-8 rounded-full border border-line hover:bg-cream/40 flex items-center justify-center text-mute hover:text-navy">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>
              </button>
              <button aria-label="Share on X" class="w-8 h-8 rounded-full border border-line hover:bg-cream/40 flex items-center justify-center text-mute hover:text-navy">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
              </button>
              <button aria-label="Share on Facebook" class="w-8 h-8 rounded-full border border-line hover:bg-cream/40 flex items-center justify-center text-mute hover:text-navy">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M22 12.06C22 6.5 17.52 2 12 2S2 6.5 2 12.06c0 5 3.66 9.15 8.44 9.94v-7.03H7.9v-2.91h2.54V9.85c0-2.51 1.49-3.89 3.77-3.89 1.1 0 2.24.2 2.24.2v2.46h-1.26c-1.24 0-1.63.77-1.63 1.56v1.88h2.78l-.45 2.91h-2.34V22c4.78-.79 8.45-4.95 8.45-9.94z"/></svg>
              </button>
            </div>
          </div>
        </div>

        <!-- Trust strip -->
        <div class="mt-5 grid grid-cols-3 gap-3 text-center">
          <div class="bg-cream/40 rounded-lg px-2 py-3">
            <div class="text-orange display text-xl font-bold">30s</div>
            <div class="text-[10px] heading uppercase tracking-wider text-mute mt-0.5">checkout</div>
          </div>
          <div class="bg-cream/40 rounded-lg px-2 py-3">
            <div class="text-orange display text-xl font-bold">∞</div>
            <div class="text-[10px] heading uppercase tracking-wider text-mute mt-0.5">free updates</div>
          </div>
          <div class="bg-cream/40 rounded-lg px-2 py-3">
            <div class="text-orange display text-xl font-bold">7d</div>
            <div class="text-[10px] heading uppercase tracking-wider text-mute mt-0.5">refund</div>
          </div>
        </div>
      </aside>
    </div>
  </main>

  {other}

  <!-- FOOTER -->
  <footer class="border-t border-line/60 mt-10 py-8 text-center text-xs text-mute">
    <div class="max-w-6xl mx-auto px-5">
      © Leo Tan Financial · <a href="/index.html" class="hover:text-navy">Shop home</a>
    </div>
  </footer>
</body>
</html>
"""


def main():
    for slug, p in DATA.items():
        out = HERE / f"{slug}.html"
        out.write_text(page(slug, p))
        print(f"wrote {out.name} ({out.stat().st_size // 1024}KB)")
    print(f"\n{len(DATA)} pages")


if __name__ == "__main__":
    main()
