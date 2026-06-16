# 🚀 CarbonSense AI Deployment Guide

Two easy deployment options:
1. **Docker Compose** (Recommended - one command deployment!)
2. **Manual Deployment** (For full control)


## Option 1: Docker Compose (Recommended)

### Step 1: Prepare your environment
1. Copy `backend/.env.example` → `backend/.env`
2. Copy `frontend/.env.example` → `frontend/.env`
3. Update the `SECRET_KEY` in `backend/.env` to a strong random value!

### Step 2: Run everything!
```bash
docker-compose up --build -d
```

The app will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Step 3: Check status
```bash
docker-compose ps
```

### To stop:
```bash
docker-compose down
```

### To view logs:
```bash
docker-compose logs -f  # -f = follow live logs
```


## Option 2: Manual Deployment

### Prerequisites
- Python 3.11+
- Node.js 20+
- PostgreSQL 15+ (or use SQLite for small deployments)

---

### Backend Setup (Manual)

1. Navigate to backend dir:
```bash
cd backend
```

2. Create venv and install dependencies:
```bash
python -m venv venv

# Windows:
.\venv\Scripts\Activate.ps1

# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
```

3. Configure environment variables:
```bash
# Copy example env and edit
cp .env.example .env
# Then edit .env with your settings
```

4. Start backend:
```bash
# Development:
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production (use gunicorn with uvicorn workers):
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000
```

---

### Frontend Setup (Manual)

1. Navigate to frontend dir:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your backend URL
```

4. Build for production:
```bash
npm run build
```

5. Serve the frontend (use nginx, or any static server):
```bash
# Example: use serve package
npm install -g serve
serve -s dist -l 3000
```


## Cloud Deployment (Optional)

### Render / Fly.io / Railway
1. Push your code to GitHub
2. Connect repo to your cloud provider
3. Create PostgreSQL database service
4. Configure environment variables (from .env.example)
5. Deploy both backend and frontend!


## Security Checklist Before Production

- [ ] Change `SECRET_KEY` to a cryptographically strong random string
- [ ] Disable debug mode
- [ ] Use HTTPS only (HSTS)
- [ ] Update CORS origins to your production domain
- [ ] Use PostgreSQL in production instead of SQLite
- [ ] Set up database backups!


## Environment Variables Reference

### Backend (.env)
| Variable | Purpose | Example |
|----------|---------|---------|
| DATABASE_URL | Database connection URL | sqlite:///./test.db or postgresql://... |
| SECRET_KEY | JWT signing secret (REQUIRED!) | A long random string! |
| ALGORITHM | JWT algorithm | HS256 |
| ACCESS_TOKEN_EXPIRE_MINUTES | Token lifetime | 10080 (7 days) |
| BACKEND_CORS_ORIGINS | Allowed frontend domains | http://localhost:3000,https://yoursite.com |
| OPENAI_API_KEY | Optional OpenAI key | sk-... |

### Frontend (.env)
| Variable | Purpose | Example |
|----------|---------|---------|
| VITE_API_URL | Backend API address | http://localhost:8000 |


## Troubleshooting

### Docker:
- Port conflicts? Change ports in `docker-compose.yml`
- Database not starting? Check `docker-compose logs db`
