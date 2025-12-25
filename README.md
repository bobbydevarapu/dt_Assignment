DT Assignment — Web Scraper

Overview

This repository contains a lightweight, honest web scraper that extracts structured company information from publicly accessible websites. It is intentionally simple (no browser automation) and designed to produce clean JSON output without inventing data.

Key Rules

- Crawl limit: 10–12 pages per run
- Skip login/privileged pages
- Detect and log JS-rendered pages (no JS execution performed)
- Produce factual, non-hallucinated JSON

Features

- Extracts page identity: title and meta description
- Discovers internal links and identifies common key pages (About, Products, Contact, Careers, etc.)
- Collects social media links found on pages
- Extracts emails and phone numbers from visible text
- Captures product/offerings listed in <li> items
- Logs errors, pages crawled, and JS-rendering notes
- Saves structured results to JSON (`output.json`)

Output

The scraper writes a single `output.json` file at the project root containing:

- company identity (title, description)
- list of pages crawled and HTTP status codes
- discovered key pages and internal links
- contact details (emails, phone numbers)
- social links and offerings
- processing logs and JS-rendering notes

How to Run

1. Install dependencies

```bash
pip install requests beautifulsoup4
```

2. Run the scraper

```bash
python scraper.py
```

3. Enter the website URL when prompted (example: `https://freshworks.com`)

4. After completion, `output.json` appears in the project folder. Example sample outputs are provided in the `samples/` folder.

Sample Outputs

Two example outputs are included to demonstrate scraper results:

- `samples/output_company1.json` — Freshworks example
- `samples/output_company2.json` — HubSpot example

Limitations (Honest System Behavior)

- JS-heavy sites may return minimal HTML. The scraper logs: "JS-rendered site — minimal HTML returned" when this is detected.
- No Selenium or headless browser is used — this keeps the tool lightweight but limits rendering of JS-driven content.
- Only publicly reachable pages are scanned; private or authenticated content is ignored.

Files Included

- `scraper.py` — main scraper script
- `README.md` — this documentation
- `samples/` — sample output JSON files

Notes

This tool is intended for small, honest crawls for educational or assessment purposes. If you need full JS rendering, consider a separate headless-browser solution.

If you'd like, I can also:

- run the scraper on a target URL and produce `output.json`
- add a small test harness to validate output structure

Happy to proceed with any of the above.
