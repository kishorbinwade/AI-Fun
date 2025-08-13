# AI-Fun

# AI Surprise & Serendipity - Complete Setup Guide

A full-stack application that brings daily joy and insights through AI-powered affirmations, random fun content, and personality insights using GPT-4o.

## 🌟 Features

- **Daily AI Affirmations**: Unique, personalized affirmations that stay consistent throughout the day
- **AI Random Fun**: Jokes, compliments, riddles, and mini art pieces on-demand
- **Personality Insights**: Quirky personality analysis based on user input with shareable results
- **Beautiful UI**: Modern, responsive design with smooth animations and glass morphism
- **Fast API Backend**: High-performance backend with GPT-4o integration
- **Fallback System**: Graceful degradation when API is unavailable

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- OpenAI API key with GPT-4o access
- Redis (optional, for caching)
- Modern web browser

### Backend Setup

1. **Clone and navigate to backend directory**
```bash
mkdir ai-serendipity && cd ai-serendipity
```

2. **Create and activate virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install fastapi uvicorn openai pydantic python-dotenv aiofiles
```

4. **Create environment file**
```bash
# Create .env file
echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
echo "ENVIRONMENT=development" >> .env
echo "DEBUG=True" >> .env
```

5. **Save the FastAPI code as `main.py`** (from the FastAPI backend artifact above)

6. **Run the server**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Save the HTML file** (from the frontend artifact above) as `index.html`

2. **Serve the frontend** using any web server:
```bash
# Option 1: Python built-in server
python -m http.server 3000

# Option 2: Node.js live-server (if you have it)
npx live-server --port=3000

# Option 3: Simply open index.html in your browser
```

The frontend will be available at `http://localhost:3000`

## 🔧 Configuration

### API Endpoints

- `GET /` - Health check
- `GET /api/daily-affirmation` - Get daily affirmation
- `GET /api/random-fun` - Get random fun content
- `POST /api/personality-insight` - Get personality insights
- `GET /api/stats` - Get app statistics
- `GET /api/personality-types` - List personality types

### Environment Variables

```env
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Optional
OPENAI_MODEL=gpt-4o
REDIS_URL=redis://localhost:6379/0
ENVIRONMENT=development
DEBUG=True
MAX_TOKENS=300
TEMPERATURE=0.8
CACHE_TTL=3600
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=3600
```

### Frontend Configuration

Update the `API_BASE_URL` in the frontend JavaScript:

```javascript
const API_BASE_URL = 'http://localhost:8000/api';  // Development
// const API_BASE_URL = 'https://your-api-domain.com/api';  // Production
```

## 🐳 Docker Deployment

### Using Docker Compose

1. **Create docker-compose.yml**:
```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - redis

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  frontend:
    image: nginx:alpine
    ports:
      - "3000:80"
    volumes:
      - ./index.html:/usr/share/nginx/html/index.html:ro
```

2. **Run with Docker Compose**:
```bash
docker-compose up -d
```

### Manual Docker Build

```bash
# Build backend
docker build -t ai-serendipity-api .
docker run -d -p 8000:8000 --env-file .env ai-serendipity-api

# Serve frontend with nginx
docker run -d -p 3000:80 -v $(pwd)/index.html:/usr/share/nginx/html/index.html:ro nginx:alpine
```

## 🌐 Production Deployment

### Backend (FastAPI)

1. **Use production WSGI server**:
```bash
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

2. **Nginx reverse proxy**:
```nginx
server {
    listen 80;
    server_name your-api-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Frontend

1. **Deploy to static hosting** (Netlify, Vercel, AWS S3, etc.)
2. **Update API endpoint** to production URL
3. **Configure CORS** in backend for your frontend domain

### Environment Variables for Production

```env
OPENAI_API_KEY=your_production_openai_key
ENVIRONMENT=production
DEBUG=False
ALLOWED_ORIGINS=["https://your-frontend-domain.com"]
REDIS_URL=redis://your-redis-host:6379/0
```

## 🔒 Security Considerations

1. **API Key Protection**: Never expose OpenAI API key in frontend
2. **CORS Configuration**: Set specific allowed origins in production
3. **Rate Limiting**: Implement proper rate limiting for API endpoints
4. **Input Validation**: All user inputs are validated server-side
5. **HTTPS**: Use HTTPS in production for both frontend and API

## 📈 Performance Optimization

### Backend

- **Caching**: Implement Redis caching for repeated requests
- **Connection Pooling**: Use connection pooling for database/Redis
- **Async Processing**: All API calls are asynchronous
- **Response Compression**: Enable gzip compression

### Frontend

- **Lazy Loading**: Load content on demand
- **Client-side Caching**: Cache responses in memory
- **Optimized Animations**: Use GSAP for smooth animations
- **CDN**: Serve static assets from CDN

## 🧪 Testing

### Backend Tests

```python
# test_main.py
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert "AI Serendipity" in response.json()["message"]

def test_daily_affirmation():
    response = client.get("/api/daily-affirmation")
    assert response.status_code == 200
    data = response.json()
    assert "affirmation" in data
    assert "visual_element" in data

def test_personality_insight():
    response = client.post(
        "/api/personality-insight",
        json={"input": "I love reading books"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "insight" in data
    assert "traits" in data
```

Run tests:
```bash
pip install pytest pytest-asyncio
pytest test_main.py -v
```

## 🐛 Troubleshooting

### Common Issues

1. **OpenAI API Key Error**
   - Verify API key is set in `.env` file
   - Check API key has GPT-4o access
   - Ensure sufficient API credits

2. **CORS Error**
   - Add your frontend domain to `allowed_origins`
   - Check if both HTTP and HTTPS are needed

3. **Port Already in Use**
   - Change port in uvicorn command: `--port 8001`
   - Kill existing process: `kill -9 $(lsof -ti:8000)`

4. **Frontend API Connection Failed**
   - Verify backend is running on correct port
   - Check `API_BASE_URL` in frontend JavaScript
   - Look at browser console for network errors

### Debug Mode

Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📝 API Documentation

Once the server is running
