import asyncio
import random
from urllib.parse import urlparse

import pandas as pd
import nest_asyncio
from playwright.async_api import async_playwright

from .config import settings
from .models import ScrapedCompany

nest_asyncio.apply()

async def scrape_page(url: str) -> list[ScrapedCompany]:
    ua = random.choice(settings.user_agents) if settings.use_agent else None
    proxy = random.choice(settings.proxies)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=settings.headless)
        context = await browser.new_context()
        if proxy:
            await context.set_proxy({"server": proxy})
        if ua:
            await context.set_extra_http_headers({"User-Agent": ua})
        page = await context.new_page()
        await page.goto(url, timeout=120_000)
        await page.wait_for_selector("a.provider__title-link.directory_profile")

        names = await page.eval_on_selector_all(
            "a.provider__title-link.directory_profile",
            "els => els.map(el => el.textContent.trim())"
        )
        raw_links = await page.evaluate('''
            () => {
              const selector = "a.provider__cta-link.sg-button-v2.sg-button-v2--primary.website-link__item.website-link__item--non-ppc";
              return Array.from(document.querySelectorAll(selector)).map(el => {
                const href = el.getAttribute("href");
                let dest = null;
                try {
                  const params = new URL(href, location.origin).searchParams;
                  dest = params.get("u") ? decodeURIComponent(params.get("u")) : null;
                } catch {}
                return { destination_url: dest };
              });
            }
        ''')
        locations = await page.eval_on_selector_all(
            ".provider__highlights-item.sg-tooltip-v2.location",
            "els => els.map(el => el.textContent.trim())"
        )
        await browser.close()

    results = []
    for i, name in enumerate(names, start=1):
        raw = raw_links[i-1].get("destination_url") if i-1 < len(raw_links) else None
        website = f"{urlparse(raw).scheme}://{urlparse(raw).netloc}" if raw else None
        loc = locations[i-1] if i-1 < len(locations) else None
        results.append(ScrapedCompany(sno=i, name=name, website=website, location=loc))
    return results

async def run_scraper(base_url: str, total_pages: int):
    tasks = [scrape_page(f"{base_url}?page={p}") for p in range(1, total_pages+1)]
    pages = await asyncio.gather(*tasks)
    flat = [c for page in pages for c in page]
    for idx, comp in enumerate(flat, start=1):
        comp.sno = idx
    df = pd.DataFrame([c.dict() for c in flat])
    return df, f"Scraped {len(df)} companies"
