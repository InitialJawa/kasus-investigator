"""
KASUS INVESTIGATOR - Social Media Scraper (YouTube, Kaskus, TikTok)
Scrape data dari platform sosial media pakai Playwright
"""
import asyncio
import json
import os
import re
from datetime import datetime
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent.parent / "output"
SOCIAL_DATA_FILE = OUTPUT_DIR / "social_media_data.json"

SEARCH_QUERIES = [
    "konflik kejaksaan polri 2026",
    "ferry boboho kejaksaan",
    "febrie ardiansyah brankas emas",
    "korupsi timah 300 triliun",
    "penggeledahan kejaksaan polri",
    "kortastipidkor kejaksaan",
    "brimob konvoi kejaksaan agung",
    "brankas sentul emas 74 kg",
    "ferry yanto hongkiriwang",
    "kejaksaan vs polri",
    "febrie ardiansyah densus 88",
    "perpres kortastipidkor jokowi",
]


async def scrape_youtube(page, query, max_results=5):
    """Scrape YouTube search results + video details"""
    results = []
    url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
    
    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(3000)
        
        # Ambil data dari ytInitialData
        data = await page.evaluate("""() => {
            const scripts = document.querySelectorAll('script');
            for (const s of scripts) {
                if (s.textContent.includes('ytInitialData')) {
                    const match = s.textContent.match(/ytInitialData\\s*=\\s*(\\{.+?\\});/s);
                    if (match) return JSON.parse(match[1]);
                }
            }
            return null;
        }""")
        
        if not data:
            # Fallback: scrape DOM langsung
            items = await page.query_selector_all('ytd-video-renderer')
            for item in items[:max_results]:
                try:
                    title_el = await item.query_selector('#video-title')
                    title = await title_el.inner_text() if title_el else ""
                    href = await title_el.get_attribute('href') if title_el else ""
                    
                    channel_el = await item.query_selector('#channel-name a')
                    channel = await channel_el.inner_text() if channel_el else ""
                    
                    meta_el = await item.query_selector('#metadata-line')
                    meta = await meta_el.inner_text() if meta_el else ""
                    
                    desc_el = await item.query_selector('#description-text')
                    desc = await desc_el.inner_text() if desc_el else ""
                    
                    if title.strip():
                        results.append({
                            "platform": "youtube",
                            "type": "video",
                            "title": title.strip(),
                            "url": f"https://www.youtube.com{href}" if href else "",
                            "channel": channel.strip(),
                            "metadata": meta.strip(),
                            "description": desc.strip(),
                            "query": query,
                            "scraped_at": datetime.now().isoformat(),
                        })
                except Exception:
                    continue
        else:
            # Parse ytInitialData
            try:
                contents = (data.get("contents", {})
                    .get("twoColumnSearchResultsRenderer", {})
                    .get("primaryContents", {})
                    .get("sectionListRenderer", {})
                    .get("contents", []))
                
                for section in contents:
                    items_data = (section.get("itemSectionRenderer", {})
                        .get("contents", []))
                    
                    for item_data in items_data[:max_results]:
                        vid = item_data.get("videoRenderer", {})
                        if not vid:
                            continue
                        
                        title_text = ""
                        title_runs = vid.get("title", {}).get("runs", [])
                        if title_runs:
                            title_text = title_runs[0].get("text", "")
                        
                        vid_id = vid.get("videoId", "")
                        channel_name = ""
                        ch_runs = vid.get("ownerText", {}).get("runs", [])
                        if ch_runs:
                            channel_name = ch_runs[0].get("text", "")
                        
                        desc_snippets = vid.get("detailedMetadataSnippets", [])
                        desc_text = ""
                        if desc_snippets:
                            desc_runs = desc_snippets[0].get("snippetText", {}).get("runs", [])
                            desc_text = "".join(r.get("text", "") for r in desc_runs)
                        
                        view_text = ""
                        view_runs = vid.get("viewCountText", {}).get("simpleText", "")
                        if view_runs:
                            view_text = view_runs
                        
                        published = vid.get("publishedTimeText", {}).get("simpleText", "")
                        
                        if title_text:
                            results.append({
                                "platform": "youtube",
                                "type": "video",
                                "title": title_text,
                                "url": f"https://www.youtube.com/watch?v={vid_id}" if vid_id else "",
                                "channel": channel_name,
                                "views": view_text,
                                "published": published,
                                "description": desc_text,
                                "query": query,
                                "scraped_at": datetime.now().isoformat(),
                            })
            except Exception:
                pass
    
    except Exception as e:
        print(f"  [WARN] YouTube query '{query}': {e}")
    
    return results


async def scrape_youtube_comments(page, video_url, max_comments=10):
    """Scrape komentar dari satu video YouTube"""
    comments = []
    try:
        await page.goto(video_url, wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(3000)
        
        # Scroll untuk load komentar
        for _ in range(3):
            await page.evaluate("window.scrollBy(0, 800)")
            await page.wait_for_timeout(1500)
        
        comment_els = await page.query_selector_all('ytd-comment-thread-renderer')
        for cel in comment_els[:max_comments]:
            try:
                author_el = await cel.query_selector('#author-text')
                author = await author_el.inner_text() if author_el else ""
                
                content_el = await cel.query_selector('#content-text')
                content = await content_el.inner_text() if content_el else ""
                
                like_el = await cel.query_selector('#vote-count-middle')
                likes = await like_el.inner_text() if like_el else ""
                
                if content.strip():
                    comments.append({
                        "platform": "youtube",
                        "type": "comment",
                        "author": author.strip(),
                        "content": content.strip(),
                        "likes": likes.strip(),
                        "video_url": video_url,
                        "scraped_at": datetime.now().isoformat(),
                    })
            except Exception:
                continue
    except Exception as e:
        print(f"  [WARN] Comments {video_url}: {e}")
    
    return comments


async def scrape_kaskus(page, query, max_results=5):
    """Scrape Kaskus search results"""
    results = []
    url = f"https://www.kaskus.co.id/search?q={query.replace(' ', '+')}"
    
    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(3000)
        
        items = await page.query_selector_all('article, .discussion-item, .post-item, [class*="thread"]')
        
        for item in items[:max_results]:
            try:
                title_el = await item.query_selector('a[href*="/thread/"], h3 a, h2 a, .title a')
                title = await title_el.inner_text() if title_el else ""
                href = await title_el.get_attribute('href') if title_el else ""
                
                snippet_el = await item.query_selector('.post-content, .excerpt, p')
                snippet = await snippet_el.inner_text() if snippet_el else ""
                
                if title.strip():
                    full_url = href if href.startswith("http") else f"https://www.kaskus.co.id{href}"
                    results.append({
                        "platform": "kaskus",
                        "type": "thread",
                        "title": title.strip(),
                        "url": full_url,
                        "snippet": snippet.strip()[:500],
                        "query": query,
                        "scraped_at": datetime.now().isoformat(),
                    })
            except Exception:
                continue
        
        # Fallback: coba parse semua link
        if not results:
            links = await page.query_selector_all('a')
            for link in links[:50]:
                try:
                    href = await link.get_attribute('href') or ""
                    text = await link.inner_text()
                    if "/thread/" in href and text.strip() and len(text.strip()) > 10:
                        full_url = href if href.startswith("http") else f"https://www.kaskus.co.id{href}"
                        results.append({
                            "platform": "kaskus",
                            "type": "thread",
                            "title": text.strip()[:200],
                            "url": full_url,
                            "query": query,
                            "scraped_at": datetime.now().isoformat(),
                        })
                        if len(results) >= max_results:
                            break
                except Exception:
                    continue
    except Exception as e:
        print(f"  [WARN] Kaskus query '{query}': {e}")
    
    return results


async def scrape_tiktok(page, query, max_results=5):
    """Scrape TikTok search results"""
    results = []
    url = f"https://www.tiktok.com/search?q={query.replace(' ', '+')}"
    
    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(4000)
        
        # Coba scrape dari DOM
        items = await page.query_selector_all('[class*="DivItemContainer"], [data-e2e="search_top-item"], [class*="video-feed-item"]')
        
        for item in items[:max_results]:
            try:
                desc_el = await item.query_selector('[data-e2e="search-card-desc"], p, span')
                desc = await desc_el.inner_text() if desc_el else ""
                
                link_el = await item.query_selector('a[href*="/video/"]')
                href = await link_el.get_attribute('href') if link_el else ""
                
                author_el = await item.query_selector('[data-e2e="search-card-user-unique-id"], [class*="author"]')
                author = await author_el.inner_text() if author_el else ""
                
                if desc.strip() or href:
                    results.append({
                        "platform": "tiktok",
                        "type": "video",
                        "description": desc.strip(),
                        "url": href if href.startswith("http") else f"https://www.tiktok.com{href}" if href else "",
                        "author": author.strip(),
                        "query": query,
                        "scraped_at": datetime.now().isoformat(),
                    })
            except Exception:
                continue
        
        # Fallback: cari semua video link
        if not results:
            links = await page.query_selector_all('a[href*="/video/"]')
            seen = set()
            for link in links[:20]:
                try:
                    href = await link.get_attribute('href') or ""
                    if "/video/" in href and href not in seen:
                        seen.add(href)
                        text = await link.inner_text()
                        full_url = href if href.startswith("http") else f"https://www.tiktok.com{href}"
                        results.append({
                            "platform": "tiktok",
                            "type": "video",
                            "description": text.strip()[:200] if text.strip() else "",
                            "url": full_url,
                            "query": query,
                            "scraped_at": datetime.now().isoformat(),
                        })
                        if len(results) >= max_results:
                            break
                except Exception:
                    continue
    except Exception as e:
        print(f"  [WARN] TikTok query '{query}': {e}")
    
    return results


async def main():
    from playwright.async_api import async_playwright
    
    print("=" * 60)
    print("KASUS INVESTIGATOR - Social Media Scraper")
    print("=" * 60)
    
    all_data = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            viewport={"width": 1366, "height": 768},
            locale="id-ID",
        )
        page = await context.new_page()
        
        # === YOUTUBE ===
        print("\n--- YouTube ---")
        yt_videos = []
        for query in SEARCH_QUERIES[:6]:
            print(f"  Searching: {query}")
            vids = await scrape_youtube(page, query)
            yt_videos.extend(vids)
            print(f"    -> {len(vids)} video")
            await page.wait_for_timeout(1000)
        
        # Deduplicate
        seen_urls = set()
        unique_vids = []
        for v in yt_videos:
            if v["url"] and v["url"] not in seen_urls:
                seen_urls.add(v["url"])
                unique_vids.append(v)
        
        # Scrape komentar dari top 3 video
        print(f"\n  Total unique YouTube videos: {len(unique_vids)}")
        print("  Scraping comments dari top 3 video...")
        yt_comments = []
        for vid in unique_vids[:3]:
            if vid.get("url"):
                coms = await scrape_youtube_comments(page, vid["url"])
                yt_comments.extend(coms)
                print(f"    {vid['title'][:50]}... -> {len(coms)} komentar")
                await page.wait_for_timeout(1000)
        
        all_data.extend(unique_vids)
        all_data.extend(yt_comments)
        
        # === KASKUS ===
        print("\n--- Kaskus ---")
        kaskus_data = []
        for query in SEARCH_QUERIES[:4]:
            print(f"  Searching: {query}")
            threads = await scrape_kaskus(page, query)
            kaskus_data.extend(threads)
            print(f"    -> {len(threads)} thread")
            await page.wait_for_timeout(1500)
        
        # Deduplicate
        seen_kaskus = set()
        unique_kaskus = []
        for k in kaskus_data:
            if k["url"] and k["url"] not in seen_kaskus:
                seen_kaskus.add(k["url"])
                unique_kaskus.append(k)
        
        all_data.extend(unique_kaskus)
        print(f"  Total unique Kaskus threads: {len(unique_kaskus)}")
        
        # === TIKTOK ===
        print("\n--- TikTok ---")
        tiktok_data = []
        for query in SEARCH_QUERIES[:4]:
            print(f"  Searching: {query}")
            vids = await scrape_tiktok(page, query)
            tiktok_data.extend(vids)
            print(f"    -> {len(vids)} video")
            await page.wait_for_timeout(1500)
        
        # Deduplicate
        seen_tiktok = set()
        unique_tiktok = []
        for t in tiktok_data:
            if t.get("url") and t["url"] not in seen_tiktok:
                seen_tiktok.add(t["url"])
                unique_tiktok.append(t)
        
        all_data.extend(unique_tiktok)
        print(f"  Total unique TikTok: {len(unique_tiktok)}")
        
        await browser.close()
    
    # Simpan
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(SOCIAL_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'=' * 60}")
    print(f"SELESAI! Social media data saved: {SOCIAL_DATA_FILE}")
    print(f"  YouTube videos : {len(unique_vids)}")
    print(f"  YouTube comments: {len(yt_comments)}")
    print(f"  Kaskus threads  : {len(unique_kaskus)}")
    print(f"  TikTok videos   : {len(unique_tiktok)}")
    print(f"  TOTAL           : {len(all_data)} items")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    asyncio.run(main())
