---
name: scraper-etiquette
description: Rules for implementing any real price-collection adapter (API client or web scraper) in prices.py. Use whenever writing, reviewing, or modifying code that fetches airfare data from external sites or APIs, or when the user asks to "plug a real data source" into CariocaScout.
---

# Scraper / API Etiquette

CariocaScout runs unattended on cron — a sloppy collector becomes an
abusive bot without anyone watching. Non-negotiables:

## Prefer official APIs
Always propose an official/affiliate API (e.g., flight-search partner
APIs) before scraping HTML. Scraping is the last resort.

## If scraping is unavoidable
- Honor robots.txt and the site's Terms of Service; if the ToS forbids
  scraping, tell the user and stop — do not implement workarounds.
- Never bypass logins, paywalls, CAPTCHAs, or rate limits.
- Identify honestly (no fake browser User-Agent games beyond a plain,
  truthful UA string).
- One request per route/date per day; add jitter and exponential
  backoff; hard timeout on every request.
- Cache responses; a rerun on the same day must NOT re-fetch.

## Engineering rules
- Any adapter implements the PriceProvider Protocol and returns
  Quote | None. No exceptions for "no availability".
- Tests use FakePriceProvider only — recorded fixtures at most.
  Never call the real source in the test suite.
