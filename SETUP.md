# 🚀 PROJECT SETUP & RUN GUIDE

## Quick Start (5 minutes)

### 1. Copy Environment Files
```bash
cp .env.example .env
# Edit .env if needed (default localhost:8000 is fine for development)
```

### 2. Install Backend Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 3. Start Backend Server
```bash
cd backend
python .\main.py
```
✅ You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

### 4. Start Frontend (New Terminal)
```bash
npm install
npm run dev
```
✅ You should see:
```
Local: http://localhost:5173
```

### 5. Open Browser
Navigate to: `http://localhost:5173`

---

## Configuration

### Backend URL
Edit `.env` file:
```env
VITE_BACKEND_URL=http://127.0.0.1:8000  # Local development
VITE_BACKEND_URL=https://api.example.com  # Production
```

### OpenAI API (Optional - Only for LLM Agent)
Set environment variable:
```bash
export OPENAI_API_KEY=sk-proj-your-key-here
python backend/openai_baseline.py
```

---

## What's Working ✅

- **Real Satellite Data**: ISS live position + orbital model
- **Realistic Battery/Storage**: Based on satellite specs
- **NASA Disasters**: Live events from EONET API
- **Space Weather**: Real Kp-index from NOAA
- **Auto-Refresh**: Frontend auto-updates every 10 seconds
- **Fallback System**: Uses mock data if APIs fail
- **Greedy Agent**: Baseline for testing
- **OpenAI Agent**: LLM-powered decision making (with API key)

---

## Troubleshooting

### Backend Won't Start
```bash
# Make sure Python 3.10+ is installed
python --version

# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

### Frontend Can't Connect to Backend
✅ Check `.env` file has correct `VITE_BACKEND_URL`
✅ Make sure backend is running on that URL
✅ Check browser console for errors

### Offline Badge Shows
✅ Normal - backend is optional
✅ Frontend will use mock data
✅ Check browser console for actual error

---

## Development

### Running Tests
```bash
cd backend
python baseline_agent.py  # Test greedy agent
```

### API Documentation
Once backend is running:
```
http://127.0.0.1:8000/docs  # Interactive API docs (Swagger)
```

### Adding More Satellites
Edit `backend/satellite_specs.py` to add new satellites

---

## Production Deployment

### Option 1: Docker
```bash
docker build -t antariksh .
docker run -p 7860:7860 antariksh
```

### Option 2: Manual
```bash
# Build frontend
npm run build

# Serve with backend
python backend/main.py  # Will serve dist/ files
```

---

## File Structure

```
meta_frontend/
├── backend/                    # Python FastAPI server
│   ├── main.py               # FastAPI app
│   ├── real_data.py          # Real API fetching
│   ├── satellite_specs.py    # ✅ NEW: Real specs
│   ├── env.py                # RL environment
│   ├── graders.py            # Scoring system
│   ├── baseline_agent.py     # Greedy reference
│   ├── openai_baseline.py    # LLM agent
│   └── requirements.txt       # Python deps
├── src/                        # React/TypeScript
│   ├── components/
│   └── App.tsx
├── public/                     # Static files
├── .env                        # ✅ NEW: Config file
├── .env.example               # ✅ NEW: Template
└── package.json               # Node deps
```

---

## Recent Fixes (Phase 1 ✅ COMPLETE)

✅ Created `satellite_specs.py` - Real satellite specifications
✅ Fixed `real_data.py` - Uses realistic battery/storage calculations
✅ Removed hardcoded OpenAI API key - Uses env variable
✅ Made backend URL configurable - Via `.env` file

---

## Next Steps (Optional)

- [ ] Add request logging
- [ ] Add error monitoring
- [ ] Create unit tests
- [ ] Add performance optimizations
- [ ] Deploy to cloud provider

---

Happy coding! 🚀
