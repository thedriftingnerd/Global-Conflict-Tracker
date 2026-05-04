# Quick Start Guide

## Prerequisites
- Node.js 16+ (for frontend)
- Python 3.8+ (for backend)
- npm or yarn
- Git (optional)

## ⚡ Quick Start (5 minutes)

### Option 1: Using Setup Script (Recommended for Unix/Mac/Linux)

```bash
# Make the setup script executable
chmod +x setup.sh

# Run the setup script
./setup.sh
```

The script will:
- Create Python virtual environment
- Install Python dependencies
- Install Node packages
- Provide instructions for running the app

### Option 2: Manual Setup

#### Backend Setup
```bash
# Navigate to backend
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the server
python app.py
```

The backend will run at `http://localhost:5000`

#### Frontend Setup (in a new terminal)
```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

The frontend will open at `http://localhost:3000`

### Option 3: Using Docker

```bash
# Build and run with docker-compose
docker-compose up

# Access:
# Frontend: http://localhost:3000
# Backend: http://localhost:5000
```

## 🌍 Using the Application

1. **Explore the Globe**
   - Click and drag to rotate
   - Scroll to zoom in/out
   - Markers show conflict locations (color = intensity)

2. **View Conflict Details**
   - Click any marker to open details panel
   - See statistics, involved parties, and news

3. **Read News**
   - Latest articles from trusted sources automatically loaded
   - Click links to read full articles

## 🎨 Customization

### Add More Conflicts
Edit `backend/app.py` and add to the `CONFLICTS` list:
```python
{
    "id": "unique-id",
    "name": "Conflict Name",
    "latitude": 0.0,
    "longitude": 0.0,
    ...
}
```

### Change Colors/Styling
Edit CSS files in `frontend/src/styles/`

### Add News Sources
Edit `NEWS_SOURCES` in `backend/app.py`

## 📦 Project Structure

```
conflict_tracker/
├── backend/
│   ├── app.py              # Flask API server
│   ├── config.py           # Configuration
│   ├── requirements.txt     # Python dependencies
│   ├── Dockerfile          # Docker setup
│   └── venv/               # Virtual environment
├── frontend/
│   ├── public/
│   │   └── index.html      # HTML template
│   ├── src/
│   │   ├── App.js          # Main React component
│   │   ├── index.js        # Entry point
│   │   ├── components/     # React components
│   │   │   ├── Globe.js    # 3D globe
│   │   │   ├── SidePanel.js
│   │   │   └── Header.js
│   │   └── styles/         # CSS files
│   ├── package.json
│   ├── Dockerfile
│   └── node_modules/
├── docker-compose.yml      # Docker configuration
├── setup.sh               # Setup script
├── README.md              # Full documentation
└── QUICKSTART.md          # This file
```

## 🔧 Troubleshooting

### Port Already in Use
```bash
# Change port in backend/app.py line ~300:
app.run(debug=True, host='0.0.0.0', port=5001)

# Change API URL in frontend/.env:
VITE_REACT_APP_API_URL=http://localhost:5001
```

### CORS Errors
- Ensure backend is running on port 5000
- Check frontend `.env` has correct API URL

### News Not Loading
- Check backend logs for RSS feed errors
- Some RSS feeds may be temporarily unavailable
- The app continues to work without news

### 3D Globe Not Rendering
- Update graphics drivers
- Try different browser (Chrome recommended)
- Check WebGL support: https://get.webgl.org/

## 🚀 Deployment

### Deploy Backend (Heroku)
```bash
cd backend
heroku create conflict-tracker-api
git push heroku main
```

### Deploy Frontend (Vercel)
```bash
cd frontend
npm run build
# Upload 'build' folder to Vercel
```

## 📚 API Endpoints

- `GET /api/conflicts` - All conflicts
- `GET /api/conflicts/<id>` - Specific conflict
- `GET /api/conflicts/<id>/news` - News for conflict
- `GET /api/stats` - Global statistics
- `GET /api/health` - Server status

## 🎯 Next Steps

1. Customize data with real conflicts in your region
2. Add more news sources
3. Deploy to production
4. Add user authentication
5. Implement real-time data updates

## 📝 Notes

- First load may take a moment to fetch news articles
- Some RSS feeds may have rate limits
- News is cached for performance
- Data is for educational purposes

## 💬 Questions?

Refer to the full [README.md](README.md) for detailed documentation.

---

**Enjoy tracking global conflicts responsibly!** 🌍
