# leotanfinancial-shop-mockup

Static HTML mockup for the `/shop` page on [leotanfinancial.sg](https://leotanfinancial.sg). Two pages, no build step.

**Live preview:** [leotanfinancial-shop-mockup.vercel.app](https://leotanfinancial-shop-mockup.vercel.app)

## What's in here

- `index.html` — full shop page mockup with 12 products (eBooks, apps, 1:1 session, bundle) and brand-matched styling (navy `#0B3D61` + orange `#F68A1E`, Plus Jakarta Sans + Roboto Serif)
- `cover.html` — eBook cover mockup for *The Ultimate Guide to Investing in Singapore* with three angle variants (flat, 3D, series stack)
- `shop-mockup-assets/` — real eBook covers extracted from the production PDFs + clean Leo headshot used for the Investing cover

## Stack

Single-file HTML + Tailwind via CDN. No bundler, no framework. Open the file or deploy as a static site.

## Products

| # | Product | Type | Price (SGD) | Cover |
|---|---|---|---|---|
| 1 | The Ultimate Guide to Financial Planning | eBook | 24 | Real PDF cover |
| 2 | The Ultimate Guide to Adulting | eBook | 19 | Real PDF cover |
| 3 | 9 Money Management Rules | eBook | 15 | Real PDF cover |
| 4 | The Wedding Playbook | eBook | 24 | Real PDF cover |
| 5 | Are You Truly Ready for Retirement? | eBook | 24 | Real PDF cover |
| 6 | The Ultimate Guide to Investing in Singapore | eBook | 19 | HTML/CSS mockup (see `cover.html`) |
| 7 | Budget Tracker | App (Excel + Notion) | 15 | UI mock |
| 8 | HDB Mortgage Calculator | Pay-to-unlock app | 12 | UI mock |
| 9 | CPF Life Estimator | Pay-to-unlock app | 12 | UI mock |
| 10 | PolicyLens | AI tool · pay-to-unlock | 19 | UI mock |
| 11 | 1:1 Bee Hive Finance Hub Walkthrough | Session | 80 | UI mock |
| 12 | Complete eBook Bundle (all 6) | Bundle | 89 (was 125, save 29%) | — |

## Status

This is a layout/visual mockup. No real checkout, no real auth. Once approved, content gets ported to the actual `/shop` route in [`leotansingapore/leotanfinancial.sg`](https://github.com/leotansingapore/leotanfinancial.sg) and wired up with Stripe + Supabase (see plan in main repo).

## Deploy

Auto-deployed to Vercel on push to `main`.
