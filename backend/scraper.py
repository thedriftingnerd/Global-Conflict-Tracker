import requests
from bs4 import BeautifulSoup
import re
from geopy.geocoders import Nominatim
import time

geolocator = Nominatim(user_agent="conflict_tracker_app")

def extract_number(text):
    if not text:
        return 0
    # Remove citations like [1]
    text = re.sub(r'\[\d+\]', '', text)
    # Extract just numbers, ignoring commas
    nums = re.findall(r'[\d,]+', text)
    if nums:
        return int(nums[0].replace(',', ''))
    return 0

def scrape_wikipedia_conflicts(existing_conflicts):
    print("Scraping Wikipedia for ongoing armed conflicts...")
    url = "https://en.wikipedia.org/wiki/List_of_ongoing_armed_conflicts"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        new_conflicts_count = 0
        
        # Look at the first 3 tables (Major conflicts, 10,000+, 1,000+)
        tables = soup.find_all('table', class_='wikitable')[:3]
        
        for table in tables:
            rows = table.find_all('tr')[1:] # Skip header
            for row in rows:
                cols = row.find_all(['th', 'td'])
                if len(cols) >= 5:
                    start_yr = cols[0].text.strip()
                    conflict_names = cols[1].text.strip().split('\n')
                    main_conflict = conflict_names[0].split('(')[0].strip() # Get main name
                    
                    if not main_conflict: continue
                        
                    continent = cols[2].text.strip()
                    locations = cols[3].text.strip().split('\n')
                    main_country = locations[0].strip().split(' ')[0] if locations else ""
                    
                    cumulative_deaths = extract_number(cols[4].text)
                    
                    # Generate a simple ID
                    conflict_id = main_conflict.lower().replace(' ', '-').replace(',', '')
                    conflict_id = re.sub(r'[^a-z0-9\-]', '', conflict_id)[:30]
                    
                    # Check if exists
                    exists = any(c['id'] == conflict_id for c in existing_conflicts)
                    if not exists:
                        print(f"Discovered new conflict: {main_conflict} in {main_country}")
                        lat, lng = 0.0, 0.0
                        
                        # Try to geolocate
                        try:
                            location_data = geolocator.geocode(main_country, timeout=5)
                            if location_data:
                                lat = location_data.latitude
                                lng = location_data.longitude
                        except Exception as e:
                            print(f"Geocoding failed for {main_country}: {e}")
                            
                        intensity = 8 if cumulative_deaths > 100000 else (6 if cumulative_deaths > 10000 else 4)
                        
                        parties = locations[:2] if len(locations) > 1 else [main_country]
                        
                        new_conflict = {
                            "id": conflict_id,
                            "name": main_conflict,
                            "latitude": lat,
                            "longitude": lng,
                            "country": main_country,
                            "startDate": f"{start_yr}-01-01",
                            "description": f"Ongoing conflict starting in {start_yr}.",
                            "parties": parties,
                            "status": "Ongoing",
                            "intensity": intensity,
                            "estimatedDeaths": cumulative_deaths,
                            "internationalResponse": "Under international monitoring.",
                            "mainCauses": "Political and territorial disputes."
                        }
                        
                        existing_conflicts.append(new_conflict)
                        new_conflicts_count += 1
                        time.sleep(1) # Be nice to geocoder API
                        
        print(f"Scraping completed. Added {new_conflicts_count} new conflicts.")
    except Exception as e:
        print(f"Error during scraping: {e}")

