# Conflict Tracker - Development & Deployment Guide

## Development Environment

### Local Development Setup

1. **Backend Development**
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   export FLASK_ENV=development
   flask run
   ```

2. **Frontend Development**
   ```bash
   cd frontend
   npm install
   npm start
   ```

### Environment Variables

**Backend (.env)**
```
FLASK_ENV=development
CORS_ALLOWED_ORIGINS=http://localhost:3000
NEWS_API_KEY=your_key_here  # Optional
```

**Frontend (.env)**
```
REACT_APP_API_URL=http://localhost:5000
REACT_APP_ENABLE_NEWS=true
```

## Production Deployment

### Option 1: Heroku (Backend) + Vercel (Frontend)

**Backend on Heroku:**
```bash
# Install Heroku CLI
brew install heroku/brew/heroku

# Login
heroku login

# Create app
heroku create conflict-tracker-api

# Set environment
heroku config:set FLASK_ENV=production

# Deploy
git push heroku main

# View logs
heroku logs --tail
```

**Frontend on Vercel:**
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
cd frontend
vercel

# Set environment variables in Vercel dashboard
REACT_APP_API_URL=https://conflict-tracker-api.herokuapp.com
```

### Option 2: Docker

**Build and run:**
```bash
docker-compose up -d

# Check logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Option 3: AWS / DigitalOcean

**Backend (Flask)**
- Use Gunicorn WSGI server
- Deploy to EC2 or App Platform
- Use RDS for database (future)

**Frontend (React)**
- Build for production: `npm run build`
- Host static files on S3 + CloudFront
- Or use Lightsail / App Platform

**Example Gunicorn command:**
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Database Setup (Optional for Real Data)

```sql
-- PostgreSQL example
CREATE TABLE conflicts (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    start_date DATE,
    status VARCHAR(50),
    intensity INT,
    description TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE conflict_updates (
    id UUID PRIMARY KEY,
    conflict_id UUID REFERENCES conflicts(id),
    deaths INT,
    displaced INT,
    cost_billions FLOAT,
    last_update TIMESTAMP,
    source VARCHAR(255)
);
```

## CI/CD Pipeline

### GitHub Actions Example

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - run: pip install -r backend/requirements.txt
      - run: cd backend && python -m pytest

  frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-node@v2
        with:
          node-version: '16'
      - run: cd frontend && npm ci
      - run: cd frontend && npm run build
      - run: cd frontend && npm test
```

## Performance Optimization

### Frontend
- Code splitting with React.lazy()
- Image optimization
- Gzip compression
- CDN for static assets
- Service worker for offline support

### Backend
- Database indexing
- Caching with Redis
- API rate limiting
- Async task queue (Celery)
- Load balancing with Nginx

## Monitoring & Logging

### Sentry (Error Tracking)
```python
import sentry_sdk
sentry_sdk.init("your_sentry_url")
```

### CloudWatch / ELK Stack
Configure structured logging for production

### Uptime Monitoring
Use Pingdom, Uptime Robot, or similar

## Security Checklist

- [ ] HTTPS/SSL enabled
- [ ] CORS properly configured
- [ ] Input validation on all endpoints
- [ ] Rate limiting implemented
- [ ] Secrets in environment variables
- [ ] SQL injection prevention
- [ ] XSS prevention
- [ ] CSRF protection
- [ ] Regular security updates

## Scaling Strategies

1. **Horizontal Scaling**
   - Use load balancer
   - Multiple backend instances
   - Static file CDN

2. **Caching**
   - Redis for session/data cache
   - Browser caching headers
   - API response caching

3. **Database**
   - Read replicas
   - Connection pooling
   - Index optimization

4. **Async Processing**
   - News fetching in background
   - Queue system for long tasks

---

For more details, see [QUICKSTART.md](QUICKSTART.md) and [README.md](README.md)
