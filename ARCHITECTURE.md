# Project Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (React)                          │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  App.js (Main Container)                            │   │
│  │  ├── Header (Stats, Title)                          │   │
│  │  ├── GlobeComponent (Three.js 3D Visualization)     │   │
│  │  └── SidePanel (Conflict Details & News)            │   │
│  └──────────────────────────────────────────────────────┘   │
│              ↓ HTTP Requests (CORS enabled)   ↓             │
├─────────────────────────────────────────────────────────────┤
│                Backend (Flask + Python)                      │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  app.py (Main Flask App)                            │   │
│  │  ├── /api/conflicts       (GET all conflicts)       │   │
│  │  ├── /api/conflicts/<id>  (GET specific conflict)   │   │
│  │  ├── /api/conflicts/<id>/news (GET conflict news)   │   │
│  │  ├── /api/stats           (GET global statistics)   │   │
│  │  └── /api/health          (Health check)            │   │
│  │                                                      │   │
│  │  utils.py (Helper functions)                        │   │
│  │  config.py (Configuration)                          │   │
│  └──────────────────────────────────────────────────────┘   │
│              ↓ RSS Feed Requests   ↓  In-Memory Data         │
├─────────────────────────────────────────────────────────────┤
│                External Data Sources                        │
│  ├── BBC World (RSS Feed)                                   │
│  ├── Reuters (RSS Feed)                                     │
│  ├── Al Jazeera (RSS Feed)                                  │
│  └── The Guardian (RSS Feed)                                │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. Initial Page Load
```
Browser
  ↓
Load index.html
  ↓
Import React components
  ↓
Request /api/conflicts (GET)
  ↓
Render Globe with markers
  ↓
Display in browser
```

### 2. Clicking a Conflict Marker
```
User Clicks Marker
  ↓
Globe.js raycaster detects click
  ↓
onSelectConflict(conflict) called
  ↓
SidePanel opens with animation
  ↓
Request /api/conflicts/<id>/news (GET)
  ↓
Fetch and parse RSS feeds
  ↓
Display articles in panel
```

### 3. News Fetching (in detail)
```
Request: /api/conflicts/<id>/news
  ↓
Backend matches conflict keywords
  ↓
Query multiple RSS feeds (parallel)
  ↓
Parse XML with feedparser
  ↓
Filter articles by relevance
  ↓
Sort by date (newest first)
  ↓
JSON response to frontend
  ↓
Update SidePanel with articles
```

## Technology Stack Details

### Frontend

| Technology  | Purpose | Why Chosen |
|-------------|---------|-----------|
| React 18   | UI Framework | Fast, component-based, large ecosystem |
| Three.js   | 3D Graphics | Powerful, flexible WebGL wrapper |
| three-globe| Globe Visualization | Specialized for geospatial data |
| Framer Motion | Animations | Smooth, performant animation library |
| CSS3       | Styling | Native, no build overhead |
| Lucide React | Icons | Clean, lightweight icon library |

### Backend

| Technology  | Purpose | Why Chosen |
|-------------|---------|-----------|
| Flask      | Web Framework | Lightweight, Pythonic, perfect for APIs |
| Flask-CORS | Cross-origin | Simple CORS handling |
| Feedparser | RSS Parsing | Robust RSS/Atom parsing |
| Requests   | HTTP Client | Simple HTTP requests |
| python-dotenv | Config | Environment variable management |

## Component Architecture

### Frontend Components

```
App (Container)
├── Header
│   └── Statistics display
├── GlobeComponent
│   ├── Three.js Scene
│   ├── ThreeGlobe instance
│   ├── Points layer (conflicts)
│   ├── Camera & Renderer
│   ├── Mouse interaction handler
│   └── Raycaster (click detection)
└── SidePanel (Modal)
    ├── Close button
    ├── Conflict header
    ├── Description
    ├── Statistics grid
    ├── Parties list
    ├── Causes & Response
    └── News section
```

### Backend Routes

```
Flask App
├── GET /api/conflicts
│   └── Returns all conflicts
├── GET /api/conflicts/<id>
│   └── Returns specific conflict
├── GET /api/conflicts/<id>/news
│   ├── Match keywords
│   ├── Fetch from RSS feeds
│   ├── Parse XML
│   ├── Filter results
│   └── Return JSON
├── GET /api/stats
│   └── Calculate global statistics
└── GET /api/health
    └── Return server status
```

## State Management

### React State (App.js)
```javascript
selectedConflict    // Currently selected conflict object
conflicts          // Array of all conflicts
loading            // Loading state
stats              // Global statistics
```

### Component Props
```
App
  ↓
GlobeComponent (conflicts, onSelectConflict, selectedConflict)
  ↓
SidePanel (conflict, onClose)
```

## 3D Globe Implementation

### ThreeGlobe Structure
```
Scene
├── Globe (Sphere geometry)
│   ├── Material (custom)
│   ├── Texture (world map)
│   └── Points (conflict markers)
├── Atmosphere (visual effect)
├── Lights
│   ├── Ambient light
│   ├── Directional light
│   └── Back light
└── Camera & Renderer
```

### Interaction System
```
Mouse Events
├── mousedown
│   └── Start rotation
├── mousemove
│   ├── Calculate delta
│   └── Update rotation
├── mouseup
│   └── Stop rotation & enable auto-rotate
├── wheel
│   └── Camera zoom
└── click
    ├── Raycaster detection
    ├── Find closest point
    └── Select conflict (if hit)
```

## Performance Considerations

### Frontend Optimizations
- ✅ WebGL rendering (Three.js)
- ✅ requestAnimationFrame for smooth animations
- ✅ Efficient State management
- ✅ CSS transforms and transitions
- ✅ Lazy loading components
- ✅ Image optimization

### Backend Optimizations
- ✅ Efficient RSS feed parsing
- ✅ In-memory data storage (for now)
- ✅ Parallel feed requests
- ✅ Response caching (future)
- ✅ Rate limiting (in utils)

### Network Optimizations
- ✅ Gzip compression
- ✅ Minimal JSON payload
- ✅ Reduced HTTP requests
- ✅ CDN-ready (future)

## Scalability Path

### Current (MVP)
- Single backend server
- In-memory data storage
- RSS feed parsing
- Static conflict data

### Phase 2 (Growth)
- Database integration (PostgreSQL)
- Caching layer (Redis)
- Multiple backend instances
- Load balancer (Nginx)

### Phase 3 (Scale)
- Microservices architecture
- Event streaming (Kafka)
- Real-time data pipeline
- CDN for static assets
- Advanced analytics

## Security Architecture

```
Internet
   ↓
WAF (Optional)
   ↓
Load Balancer (HTTPS)
   ↓
Backend Server
├── CORS validation
├── Input validation
├── Rate limiting
└── Error handling (safe errors)
   ↓
Frontend
├── XSS prevention (React escaping)
├── CSRF tokens (future)
└── Secure headers
```

## Deployment Architecture

### Development
```
localhost:3000 (Frontend)  ←→  localhost:5000 (Backend)
```

### Docker
```
Docker Host
├── Frontend Container (Node.js)
├── Backend Container (Python)
└── Network (internal)
```

### Production (Proposed)
```
CDN (Static files)
   ↓
Load Balancer
   ↓
[Backend 1][Backend 2][Backend 3]
   ↓
Database
   ↓
Cache (Redis)
```

## Error Handling

### Frontend
- Try-catch in component lifecycle
- Error boundary (future)
- User-friendly error messages
- Fallback UI

### Backend
- Try-catch in route handlers
- Validation before processing
- Graceful feed fetch failures
- Informative error responses

## Future Enhancements

1. **Database**: PostgreSQL for persistent storage
2. **Real-time Data**: WebSocket for live updates
3. **User Accounts**: Authentication & bookmarks
4. **Advanced Analytics**: Data visualization & charts
5. **Mobile App**: React Native version
6. **Admin Panel**: Manage conflicts & data
7. **Notifications**: Alert users to new conflicts
8. **Multi-language**: i18n support

---

This architecture is designed to be:
- **Scalable**: Can grow from MVP to enterprise
- **Maintainable**: Clean separation of concerns
- **Performance-focused**: Optimized for 60fps UX
- **Developer-friendly**: Easy to understand and extend
