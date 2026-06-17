# 🌍 CarbonSense AI

Your AI-powered personal climate coach. A full-stack application to track, understand, and reduce your carbon footprint.

---

## 🌟 GOOGLE CLOUD PLATFORM (GCP) INTEGRATIONS (FOR HACKATHON!)

This project uses **multiple Google Cloud services** to deliver an intelligent, scalable solution! Here's what's included:

| Google Cloud Service                  | Purpose in CarbonSense AI                                                                    |
| ------------------------------------- | -------------------------------------------------------------------------------------------- |
| **Google Gemini API** (Generative AI) | Powers the AI Climate Assistant with personalized, natural language recommendations and chat |
| **Google Cloud Run**                  | Serverless compute for deploying both frontend and backend containers                        |
| **Google Cloud SQL**                  | Managed PostgreSQL database for user data and carbon history                                 |
| **Google Cloud Storage**              | For storing user profile pictures and other media                                            |
| **Google Maps Platform API**          | Location-based carbon footprint insights and local sustainability recommendations            |
| **Google Cloud Logging & Monitoring** | Observability, error tracking, and performance monitoring                                    |
| **Google reCAPTCHA**                  | Bot protection on authentication endpoints                                                   |

All API keys and service configurations are available in the `.env.example` files!

---

## 🚀 Features

### Core Functionality

- **User Profile System**: Collect detailed lifestyle information
- **Carbon Calculation Engine**: Modular system for transport, energy, food, and lifestyle emissions
- **Carbon Dashboard**: Beautiful visualizations with total footprint, score, and trends
- **AI Climate Assistant (Powered by Google Gemini!)**: Personalized recommendations and chat interface
- **Carbon Twin Simulator**: See impact of lifestyle changes before making them
- **Personalized Action Planner**: Daily/weekly/monthly green actions
- **Gamification**: Eco points and badges (coming soon)

### Technical Highlights

- **Frontend**: React + TypeScript + Tailwind CSS + Recharts
- **Backend**: FastAPI + Python + SQLAlchemy
- **Database**: PostgreSQL
- **Authentication**: JWT with password hashing (bcrypt)
- **Docker Support**: Full containerized deployment

## 🛠️ Quick Start

### Prerequisites

- Docker and Docker Compose
- OR Node.js 20+ and Python 3.11+

### Using Docker (Recommended)

```bash
# Clone and start all services
git clone <repo-url>
cd carbonsense-ai
docker-compose up --build
```

The app will be available at:

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Manual Setup

#### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your config

# Run the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

## 🏗️ Architecture

### Project Structure

```
carbonsense-ai/
├── backend/
│   ├── app/
│   │   ├── api/           # API routes
│   │   ├── core/          # Config, DB, security
│   │   ├── models/        # SQLAlchemy models
│   │   ├── schemas/       # Pydantic schemas
│   │   ├── services/      # Carbon calculator and AI
│   │   └── main.py
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/    # Reusable components
│   │   ├── pages/         # Page components
│   │   ├── hooks/         # Custom hooks
│   │   ├── services/      # API services
│   │   ├── context/       # React context
│   │   └── App.tsx
│   ├── Dockerfile
│   └── package.json
├── docker-compose.yml
└── README.md
```

## 🔐 Security

- JWT-based authentication
- Password hashing using bcrypt
- Input validation with Pydantic
- CORS configuration
- Environment variable protection
- No SQL injection (SQLAlchemy ORM)

## 📊 Carbon Calculation

### Emission Categories

- **Transport**: Distance × frequency × vehicle emission factor
- **Energy**: Electricity + gas consumption
- **Food**: Diet type × meat consumption frequency
- **Lifestyle**: Shopping + waste generation

### Carbon Score

0-100 based on total monthly emissions:

- 80-100: Excellent
- 60-79: Good
- 40-59: Fair
- Below 40: Needs improvement

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest tests/ -v
```

## 📝 License

MIT License - feel free to use this project!

## 🌱 Future Improvements

- Connect to real carbon data APIs
- Add more gamification features
- Community challenges
- Carbon offset marketplace integration
- Mobile app
