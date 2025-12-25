import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
import json
from datetime import datetime

MAX_PAGES = 12   # Assignment requires 10–15 pages


def fetch(url):
    """Fetch a page safely with proper headers."""
    try:
        response = requests.get(url, timeout=7, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        })
        if response.status_code == 200:
            return response.text, None
        return None, f"HTTP {response.status_code}"
    except Exception as e:
        return None, str(e)


def extract_links(soup, base_url):
    """Extract internal links only."""
    domain = urlparse(base_url).netloc
    links = set()

    for a in soup.find_all("a", href=True):
        full = urljoin(base_url, a["href"])
        if urlparse(full).netloc == domain:
            links.add(full)

    return list(links)


def detect_key_pages(links):
    KEYS = {
        "about": ["about"],
        "products": ["product", "solution"],
        "services": ["service"],
        "industries": ["industry"],
        "pricing": ["pricing"],
        "careers": ["career", "jobs"],
        "contact": ["contact"]
    }

    detected = {k: None for k in KEYS}

    for link in links:
        low = link.lower()
        for key, words in KEYS.items():
            if any(w in low for w in words):
                detected[key] = link

    return detected


def extract_socials(soup):
    socials = {
        "linkedin": None,
        "twitter": None,
        "instagram": None,
        "youtube": None,
        "facebook": None
    }

    for a in soup.find_all("a", href=True):
        href = a["href"].lower()

        if "linkedin.com" in href:
            socials["linkedin"] = href
        elif "twitter.com" in href or "x.com" in href:
            socials["twitter"] = href
        elif "instagram.com" in href:
            socials["instagram"] = href
        elif "youtube.com" in href:
            socials["youtube"] = href
        elif "facebook.com" in href:
            socials["facebook"] = href

    return socials


def extract_emails(text):
    return list(set(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)))


def extract_phones(text):
    return list(set(re.findall(r"\+?\d[\d\s\-]{7,}\d", text)))


def scrape(url):
    visited = set()
    to_visit = [url]
    pages_crawled = 0

    output = {
        "identity": {},
        "business_summary": {
            "offerings": [],
        },
        "evidence": {},
        "contact_location": {},
        "team_hiring": {},
        "metadata": {
            "timestamp": datetime.utcnow().isoformat(),
            "pages_crawled": [],
            "errors": [],
        }
    }

    all_text = ""

    while to_visit and pages_crawled < MAX_PAGES:
        page_url = to_visit.pop(0)
        if page_url in visited:
            continue

        html, error = fetch(page_url)
        if error:
            output["metadata"]["errors"].append({page_url: error})
            continue

        # JS-rendered detection
        if html and len(html) < 500:
            output["metadata"]["errors"].append({
                page_url: "JS-rendered site — minimal HTML returned"
            })
            continue

        visited.add(page_url)
        output["metadata"]["pages_crawled"].append(page_url)
        pages_crawled += 1

        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text(" ", strip=True)
        all_text += " " + text

        # first page only → extract identity
        if pages_crawled == 1:
            title = soup.title.string.strip() if soup.title else None
            desc_tag = soup.find("meta", attrs={"name": "description"})
            desc = desc_tag.get("content", "").strip() if desc_tag else None

            output["identity"] = {
                "company_name": title or "Not found",
                "website_url": url,
                "tagline": desc or "Not found"
            }

        # offerings (list items)
        for li in soup.find_all("li"):
            li_text = li.text.strip()
            if 3 < len(li_text) < 80:
                if li_text not in output["business_summary"]["offerings"]:
                    output["business_summary"]["offerings"].append(li_text)

        # extract all internal links
        new_links = extract_links(soup, url)
        for link in new_links:
            if link not in visited and link not in to_visit:
                to_visit.append(link)

        # detect socials (first page mostly)
        output["evidence"]["social_links"] = extract_socials(soup)

        # detect key pages
        output["evidence"]["key_pages"] = detect_key_pages(new_links)

    # contacts
    output["contact_location"]["emails"] = extract_emails(all_text)
    output["contact_location"]["phones"] = extract_phones(all_text)

    return output


if __name__ == "__main__":
    url = input("Enter website URL: ").strip()
    result = scrape(url)

    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4)

    print("\nScraping complete. Saved as output.json")