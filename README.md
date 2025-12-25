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
# DT Assignment — Web Scraper

A small, dependency-light web scraper that extracts structured company information from publicly accessible websites and saves the results as JSON.

## Features

- Extracts page identity (title, meta description)
- Discovers internal links and identifies common pages (About, Products, Contact, Careers)
- Collects social media links, emails, and phone numbers from visible text
- Captures product/offerings listed in `<li>` items
- Detects and logs likely JS-rendered pages (no JS execution)
- Produces a single structured JSON output per run

## Requirements

- Python 3.8+
- pip

Recommended packages (install below): `requests`, `beautifulsoup4`

## Installation

Create a virtual environment (optional) and install dependencies:

```bash
python -m venv .venv
source .venv/Scripts/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt  # or: pip install requests beautifulsoup4
```

If you prefer not to use a requirements file, run:

```bash
pip install requests beautifulsoup4
```

## Usage

Run the scraper and follow the prompt to enter a target URL:

```bash
python scraper.py
```

The script will crawl a limited number of internal pages (keeps runs small and safe) and write a JSON file with the structured result. Example outputs are available in the `samples/` folder.

## Sample outputs

See the included examples:

- `samples/output_company1.json`
- `samples/output_company2.json`

## Limitations

- The scraper does not execute JavaScript. Pages that require client-side rendering may return limited content.
- No authentication or login flows are followed.
- Intended for small, ethical crawls only.

## Files

- `scraper.py` — main scraper script
- `samples/` — example JSON outputs
- `.gitignore` — ignored files

## Next steps I can do for you

- Run the scraper on a target URL and include the generated `output.json` in `samples/`
- Add a `requirements.txt` and small test harness to validate output structure
- Create a GitHub repo and push this project (if you give me the repo name or allow me to use `gh`)

## License & Contact

This project is provided as-is for educational purposes. Tell me if you want a license added (MIT, Apache-2.0, etc.).

---

If you'd like any wording changed or extra sections (contributing, CI), tell me which and I'll update the README.
