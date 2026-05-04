import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}

def scrape_bbc(query):
    articles = []
    try:
        url = f"https://www.bbc.co.uk/search?q={quote_plus(query)}"
        res = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        for a in soup.find_all('a', class_='ssrcss-its5xf-PromoLink'):
            title = a.text.strip()
            link = a.get('href')
            if link and not link.startswith('http'):
                link = "https://www.bbc.co.uk" + link
            if title:
                articles.append({'source': 'BBC', 'title': title, 'link': link, 'published': '', 'summary': ''})
    except Exception as e:
        pass
    return articles[:3]

def scrape_pbs(query):
    articles = []
    try:
        url = f"https://www.pbs.org/newshour/search-results?q={quote_plus(query)}"
        res = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        for article in soup.find_all('article'):
            a = article.find('a')
            if a:
                title = a.text.strip()
                link = a.get('href')
                if title:
                    articles.append({'source': 'PBS', 'title': title, 'link': link, 'published': '', 'summary': ''})
    except Exception as e:
        pass
    return articles[:3]

def scrape_dw(query):
    articles = []
    try:
        url = f"https://www.dw.com/search/?languageCode=en&item={quote_plus(query)}"
        res = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        for div in soup.find_all('div', class_='searchResult'):
            a = div.find('a')
            if a:
                title = a.find('h2').text.strip() if a.find('h2') else a.text.strip()
                link = a.get('href')
                if link and not link.startswith('http'):
                    link = "https://www.dw.com" + link
                if title:
                    articles.append({'source': 'DW News', 'title': title, 'link': link, 'published': '', 'summary': ''})
    except Exception as e:
        pass
    return articles[:3]

def scrape_reuters(query):
    # Reuters uses client side rendering or API, we will just use a generic search approach and scrape a tags
    articles = []
    try:
        url = f"https://www.reuters.com/site-search/?query={quote_plus(query)}"
        res = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        for a in soup.find_all('a', href=True):
            if '/article/' in a['href'] or '/world/' in a['href']:
                title = a.text.strip()
                link = "https://www.reuters.com" + a['href'] if not a['href'].startswith('http') else a['href']
                if title and len(title) > 15:
                    articles.append({'source': 'Reuters', 'title': title, 'link': link, 'published': '', 'summary': ''})
    except Exception as e:
        pass
    return articles[:3]

def scrape_nhk(query):
    articles = []
    try:
        url = f"https://www3.nhk.or.jp/nhkworld/en/search/?q={quote_plus(query)}"
        res = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        for a in soup.find_all('a'):
            title = a.text.strip()
            link = a.get('href')
            if link and '/news/' in link and len(title) > 15:
                if not link.startswith('http'):
                     link = "https://www3.nhk.or.jp" + link
                articles.append({'source': 'NHK', 'title': title, 'link': link, 'published': '', 'summary': ''})
    except Exception as e:
        pass
    return articles[:3]

def scrape_ap(query):
    articles = []
    try:
        url = f"https://apnews.com/search?q={quote_plus(query)}"
        res = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        for a in soup.find_all('a', class_='Link'):
            title = a.text.strip()
            link = a.get('href')
            if link and not link.startswith('http'):
                link = "https://apnews.com" + link
            if title and len(title) > 15:
                articles.append({'source': 'AP', 'title': title, 'link': link, 'published': '', 'summary': ''})
    except Exception:
        pass
    return list({v['title']:v for v in articles}.values())[:3] # Deduplicate

def fetch_conflict_news_bs4(conflict):
    """Fetch news from BBC, PBS, DW, Reuters, NHK, AP in parallel via BeautifulSoup"""
    query = conflict['name']
    articles = []
    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = [
            executor.submit(scrape_bbc, query),
            executor.submit(scrape_pbs, query),
            executor.submit(scrape_dw, query),
            executor.submit(scrape_reuters, query),
            executor.submit(scrape_nhk, query),
            executor.submit(scrape_ap, query)
        ]
        for future in as_completed(futures):
            res = future.result()
            if res:
                articles.extend(res)
    # Give them a fake published date since scraping it is brittle without complex selectors
    for i, a in enumerate(articles):
        if not a['published']:
            a['published'] = time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime(time.time() - i*3600))
    return articles

