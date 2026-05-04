from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from datetime import datetime, timedelta
import feedparser
import os
from dotenv import load_dotenv
from threading import Thread
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import schedule
from scraper import scrape_wikipedia_conflicts


load_dotenv()

app = Flask(__name__)
CORS(app)

# Global cache for news articles
NEWS_CACHE = {}
CACHE_DURATION = 3600  # 1 hour in seconds

# Conflict data with coordinates and basic information
CONFLICTS = [
    {
        "id": "ukraine-russia",
        "name": "Russia-Ukraine War",
        "latitude": 49.5,
        "longitude": 31.5,
        "country": "Ukraine",
        "startDate": "2022-02-24",
        "description": "Armed conflict between Russia and Ukraine following the Russian invasion.",
        "parties": ["Russia", "Ukraine"],
        "status": "Ongoing",
        "intensity": 8,
        "estimatedDeaths": 500000,
        "internationalResponse": "Widespread international condemnation; sanctions against Russia",
        "mainCauses": "Territorial disputes, NATO expansion concerns, political differences"
    },
    {
        "id": "israel-palestine",
        "name": "Israel-Palestine Conflict",
        "latitude": 31.9,
        "longitude": 35.2,
        "country": "Palestine",
        "startDate": "1948-05-15",
        "description": "Long-standing territorial and political conflict. Recent escalation in 2024.",
        "parties": ["Israel", "Palestine", "Hamas"],
        "status": "Ongoing",
        "intensity": 8,
        "estimatedDeaths": 50000,
        "internationalResponse": "Divided international opinion; UN involvement",
        "mainCauses": "Territorial disputes, refugee rights, religious tensions"
    },
    {
        "id": "yemen-civil-war",
        "name": "Yemeni Civil War",
        "latitude": 15.55,
        "longitude": 48.5,
        "country": "Yemen",
        "startDate": "2014-09-21",
        "description": "Civil war between the Saudi-backed government and Houthi forces.",
        "parties": ["Yemen Government", "Houthis"],
        "status": "Ongoing",
        "intensity": 7,
        "estimatedDeaths": 300000,
        "internationalResponse": "Saudi-led coalition intervention; humanitarian concerns",
        "mainCauses": "Political power struggles, sectarian tensions, territorial control"
    },
    {
        "id": "syria-civil-war",
        "name": "Syrian Civil War",
        "latitude": 34.5,
        "longitude": 36.2,
        "country": "Syria",
        "startDate": "2011-03-15",
        "description": "Multi-sided civil war involving government, rebels, and extremist groups.",
        "parties": ["Syrian Government", "Rebels", "ISIS"],
        "status": "Partially Active",
        "intensity": 6,
        "estimatedDeaths": 500000,
        "internationalResponse": "International humanitarian concerns; multiple power interventions",
        "mainCauses": "Civil unrest, sectarian conflict, government repression"
    },
    {
        "id": "myanmar-rohingya",
        "name": "Myanmar Rohingya Crisis",
        "latitude": 17.5,
        "longitude": 92.5,
        "country": "Myanmar",
        "startDate": "2017-08-25",
        "description": "Ethnic cleansing and displacement of Rohingya Muslim population.",
        "parties": ["Myanmar Military", "Rohingya population"],
        "status": "Humanitarian Crisis",
        "intensity": 7,
        "estimatedDeaths": 25000,
        "internationalResponse": "UN investigations; genocide accusations",
        "mainCauses": "Ethnic tensions, government persecution, land disputes"
    },
    {
        "id": "sudan-civil-war",
        "name": "Sudanese Civil War",
        "latitude": 12.5,
        "longitude": 30.0,
        "country": "Sudan",
        "startDate": "2023-04-15",
        "description": "Armed conflict between Sudanese Armed Forces and Rapid Support Forces.",
        "parties": ["Sudanese Armed Forces", "Rapid Support Forces"],
        "status": "Ongoing",
        "intensity": 8,
        "estimatedDeaths": 150000,
        "internationalResponse": "Humanitarian crisis; displacement of millions",
        "mainCauses": "Power struggle, military coup aftermath, political instability"
    },
    {
        "id": "ethiopia-tigray",
        "name": "Ethiopia-Tigray Conflict",
        "latitude": 12.0,
        "longitude": 39.5,
        "country": "Ethiopia",
        "startDate": "2020-11-04",
        "description": "Armed conflict between Ethiopian federal government and Tigray regional forces.",
        "parties": ["Ethiopian Federal Forces", "Tigray People's Liberation Front"],
        "status": "Ceasefire",
        "intensity": 5,
        "estimatedDeaths": 600000,
        "internationalResponse": "UN peacekeeping involvement; humanitarian aid efforts",
        "mainCauses": "Political power struggles, ethnic tensions, constitutional disputes"
    },
    {
        "id": "colombia-drugs",
        "name": "Colombian Armed Groups Conflict",
        "latitude": 4.5,
        "longitude": -74.0,
        "country": "Colombia",
        "startDate": "1964-05-27",
        "description": "Long-running conflict involving government, guerrillas, and drug cartels.",
        "parties": ["Colombian Government", "ELN", "Drug Cartels"],
        "status": "Ongoing",
        "intensity": 5,
        "estimatedDeaths": 220000,
        "internationalResponse": "US military assistance; peace process attempts",
        "mainCauses": "Drug trafficking, land disputes, political ideology"
    },
    {
        "id": "afghanistan-taliban",
        "name": "Afghanistan-Taliban Conflict",
        "latitude": 33.9,
        "longitude": 67.7,
        "country": "Afghanistan",
        "startDate": "2001-10-07",
        "description": "Conflict between Taliban government and various resistance groups.",
        "parties": ["Taliban Government", "Resistance Groups", "ISIS-K"],
        "status": "Ongoing",
        "intensity": 6,
        "estimatedDeaths": 70000,
        "internationalResponse": "Taliban recognition disputed; humanitarian concerns",
        "mainCauses": "Political control, religious governance, international intervention legacy"
    },
    {
        "id": "mexico-cartels",
        "name": "Mexican Drug War",
        "latitude": 23.6,
        "longitude": -102.5,
        "country": "Mexico",
        "startDate": "2006-12-11",
        "description": "Ongoing conflict between Mexican government and drug trafficking organizations.",
        "parties": ["Mexican Federal Forces", "Drug Cartels"],
        "status": "Ongoing",
        "intensity": 6,
        "estimatedDeaths": 250000,
        "internationalResponse": "US DEA cooperation; border security efforts",
        "mainCauses": "Drug trafficking, territorial control, government corruption"
    }
]

# News sources RSS feeds
NEWS_SOURCES = {
    "bbc": "http://feeds.bbc.co.uk/news/world/rss.xml",
    "reuters": "https://www.reutersagency.com/feed/?taxonomy=best-topics&output=rss",
    "aljazeera": "https://www.aljazeera.com/xml/rss/all.xml",
    "guardian": "https://www.theguardian.com/world/rss"
}

def fetch_feed(source_name, feed_url, timeout=5):
    """Fetch a single RSS feed with timeout"""
    try:
        # Set timeout for the feed parser
        import socket
        socket.setdefaulttimeout(timeout)
        feed = feedparser.parse(feed_url)
        return source_name, feed, None
    except Exception as e:
        return source_name, None, str(e)

from news_scraper import fetch_conflict_news_bs4

def fetch_conflict_news_parallel_old(conflict):
    """Fetch news from all sources in parallel (much faster)"""
    conflict_id = conflict['id']
    
    # Check cache
    if conflict_id in NEWS_CACHE:
        cache_time = NEWS_CACHE[conflict_id].get('timestamp', 0)
        if time.time() - cache_time < CACHE_DURATION:
            return NEWS_CACHE[conflict_id]['articles']
    
    articles = []
    conflict_name = conflict['name']
    keywords = [conflict['name'], conflict['country']] + conflict['parties'][:2]
    
    # Fetch from multiple news sources in PARALLEL
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {
            executor.submit(fetch_feed, name, url): name 
            for name, url in NEWS_SOURCES.items()
        }
        
        for future in as_completed(futures, timeout=8):
            try:
                source_name, feed, error = future.result()
                if error:
                    print(f"Error fetching from {source_name}: {error}")
                    continue
                
                if feed and feed.entries:
                    for entry in feed.entries[:5]:
                        title = entry.get('title', '')
                        # Filter by relevance
                        if any(keyword.lower() in title.lower() for keyword in keywords):
                            articles.append({
                                'source': source_name.upper(),
                                'title': title,
                                'link': entry.get('link', ''),
                                'published': entry.get('published', ''),
                                'summary': entry.get('summary', '')[:300]
                            })
            except Exception as e:
                print(f"Error processing feed result: {e}")
    
    # Sort by date (most recent first) and limit
    articles = sorted(articles, key=lambda x: x['published'] if x['published'] else '', reverse=True)[:10]
    
    # Cache the result
    NEWS_CACHE[conflict_id] = {
        'articles': articles,
        'timestamp': time.time()
    }
    
    return articles

@app.route('/api/conflicts', methods=['GET'])
def get_conflicts():
    """Get all active conflicts"""
    return jsonify(CONFLICTS)

@app.route('/api/conflicts/<conflict_id>', methods=['GET'])
def get_conflict(conflict_id):
    """Get specific conflict details"""
    conflict = next((c for c in CONFLICTS if c['id'] == conflict_id), None)
    if not conflict:
        return jsonify({'error': 'Conflict not found'}), 404
    return jsonify(conflict)

@app.route('/api/conflicts/<conflict_id>/news', methods=['GET'])
def get_conflict_news(conflict_id):
    """Get news articles for a specific conflict"""
    conflict = next((c for c in CONFLICTS if c['id'] == conflict_id), None)
    if not conflict:
        return jsonify({'error': 'Conflict not found'}), 404
    
    # Use parallel news fetching (much faster)
    articles = fetch_conflict_news_bs4(conflict)
    
    return jsonify({
        'conflictId': conflict_id,
        'conflictName': conflict['name'],
        'articles': articles
    })

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get global conflict statistics"""
    total_deaths = sum(c.get('estimatedDeaths', 0) for c in CONFLICTS)
    active_conflicts = sum(1 for c in CONFLICTS if c['status'] in ['Ongoing', 'Partially Active'])
    avg_intensity = sum(c.get('intensity', 0) for c in CONFLICTS) / len(CONFLICTS) if CONFLICTS else 0
    
    return jsonify({
        'totalConflicts': len(CONFLICTS),
        'activeConflicts': active_conflicts,
        'estimatedTotalDeaths': total_deaths,
        'averageIntensity': round(avg_intensity, 1)
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'running', 'timestamp': datetime.now().isoformat()})


def update_conflicts_job():
    global CONFLICTS
    scrape_wikipedia_conflicts(CONFLICTS)

def run_schedule():
    update_conflicts_job() # Run once on startup
    schedule.every().week.do(update_conflicts_job)
    while True:
        schedule.run_pending()
        time.sleep(60)

# Start background scraper thread
Thread(target=run_schedule, daemon=True).start()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001, use_reloader=False)
