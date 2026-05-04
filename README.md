# Conflict Tracker - Global Live Conflict Monitoring

A minimalist, slick web application for tracking conflicts and wars around the world in real-time with a 3D interactive globe, detailed statistics, and curated news from trusted sources.

## Features

✨ **3D Interactive Globe**
- Smooth, rotatable 3D map of the world using Three.js
- Color-coded conflict markers based on intensity
- Zoom and drag interactions for full exploration

📍 **Real-time Conflict Tracking**
- 10+ ongoing global conflicts monitored
- Live intensity indicators (scale 1-10)
- Historical data and casualty estimates

📰 **Integrated News Aggregation**
- Pulls articles from BBC, Reuters, Al Jazeera, and The Guardian
- Filters news relevant to each conflict
- Direct links to source articles

📊 **Comprehensive Statistics**
- Conflict intensity levels
- Estimated casualties
- Parties involved
- International response
- Root causes analysis

🎨 **Minimalist Design**
- Apple-inspired interface
- Smooth animations (Framer Motion)
- Responsive layout
- Radio.garden-level smoothness

## Tech Stack

### Frontend
- **React 18** - UI framework
- **Three.js** - 3D globe rendering
- **three-globe** - Geospatial visualization
- **Framer Motion** - Animations
- **Lucide React** - Icons
- **CSS** - Minimalist styling

### Backend
- **Python 3.8+** - Runtime
- **Flask** - Web framework
- **Flask-CORS** - Cross-origin requests
- **Feedparser** - RSS feed parsing
- **Requests** - HTTP client

## Installation

### Prerequisites
- Node.js 16+ (for frontend)
- Python 3.8+ (for backend)
- npm or yarn (for package management)

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the Flask server:
```bash
python app.py
```
The backend will run at `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```
The frontend will open at `http://localhost:3000`

## Usage

1. **Exploring the Globe**
   - Click and drag to rotate the globe
   - Scroll to zoom in/out
   - Markers appear at conflict locations

2. **Viewing Conflict Details**
   - Click on any conflict marker to open the side panel
   - View statistics, parties involved, and main causes
   - Read the latest news articles from trusted sources

3. **Header Information**
   - View global statistics at the top
   - See active conflict count and average intensity

## API Endpoints

### GET /api/conflicts
Returns list of all tracked conflicts with coordinates and basic info

### GET /api/conflicts/<conflict_id>
Returns detailed information for a specific conflict

### GET /api/conflicts/<conflict_id>/news
Returns latest news articles for a conflict (fetched from RSS feeds)

### GET /api/stats
Returns global statistics (total conflicts, active count, deaths, intensity)

### GET /api/health
Health check endpoint

## Data Sources

**Conflict Data**: Manually curated based on UN reports and major news outlets

**News Feeds**:
- BBC World (http://feeds.bbc.co.uk/news/world/rss.xml)
- Reuters (https://www.reutersagency.com/feed/)
- Al Jazeera (https://www.aljazeera.com/xml/rss/all.xml)
- The Guardian World (https://www.theguardian.com/world/rss)

## Customization

### Adding New Conflicts
Edit `backend/app.py` and add to the `CONFLICTS` list:
```python
{
    "id": "unique-id",
    "name": "Conflict Name",
    "latitude": 0.0,
    "longitude": 0.0,
    "country": "Country",
    "startDate": "YYYY-MM-DD",
    "description": "...",
    "parties": [...],
    "status": "Ongoing",
    "intensity": 7,
    "estimatedDeaths": 100000,
    "internationalResponse": "...",
    "mainCauses": "..."
}
```

### Styling
- Modify CSS files in `frontend/src/styles/` for design changes
- Update color scheme in component files (e.g., `Globe.js` for intensity colors)

### Adding News Sources
Edit the `NEWS_SOURCES` dictionary in `backend/app.py` to add more RSS feeds

## Performance Optimization

The application is optimized for smoothness:
- WebGL rendering for 3D globe
- Requestanimationframe for 60fps interactions
- CSS transforms for smooth animations
- Efficient re-rendering with React
- Lazy loading of news articles

## Deployment

### Backend (Heroku/Render)
```bash
git push heroku main
```

### Frontend (Vercel/Netlify)
```bash
npm run build
# Deploy the build folder
```

## Future Enhancements

- Real-time data integration with conflict monitoring APIs
- User accounts and saved bookmarks
- Advanced filtering and search
- Timeline view of conflict progression
- Social media sentiment analysis
- Predictive models for conflict escalation
- Multi-language support
- Mobile app version

## License

MIT License - feel free to use for educational and non-commercial purposes

## Support

For issues, feature requests, or suggestions, please create an issue in the project repository.

---

**Stay informed. Stay aware. Stay safe.**
