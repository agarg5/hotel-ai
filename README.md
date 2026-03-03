# Hotel AI Booking Agent

An intelligent hotel booking system that processes natural-language requests, checks room availability across 25 rooms, suggests split stays when needed, and applies dynamic pricing policies — all powered by OpenAI's language models.

**Try it live:** https://hotel-ai-booking-production.up.railway.app

## What It Does

A guest writes something like *"Book a room for John Smith, 2 guests, checking in June 10 and checking out June 14"* and the system:

1. **Parses the request** using OpenAI — handles multiple languages, relative dates ("tomorrow for 3 nights"), and varied formats
2. **Checks availability** against the hotel's 25-room inventory
3. **Suggests split stays** if no single room covers the full stay (e.g., Room 5 for 2 nights then Room 12 for 2 nights)
4. **Applies discount policies** defined in `hotel_policy.txt` (e.g., 10% off for stays >= 7 nights)
5. **Returns a structured result** with available rooms, pricing, and any applicable discounts

## Architecture

```
┌─────────────────────────────────┐
│   React Frontend (Vite SPA)     │  ← Natural language input form
├─────────────────────────────────┤
│   FastAPI Server                │  ← REST API + static file serving
├─────────────────────────────────┤
│   Booking Agent (Python)        │  ← Availability, split-stay, pricing logic
├─────────────────────────────────┤
│   OpenAI API                    │  ← NLU for date/intent extraction
├─────────────────────────────────┤
│   CSV Data Store                │  ← bookings.csv, hotel_policy.txt
└─────────────────────────────────┘
```

**Key design decisions:**
- Single service deployment — React frontend is built at deploy time and served by FastAPI via `StaticFiles`, keeping infrastructure simple
- No database — CSV files simulate the hotel's booking system, making the project self-contained and easy to demo
- LLM-powered parsing — instead of rigid date formats, guests can write naturally in any language

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 19, Vite |
| Backend | FastAPI, Python 3 |
| NLU | OpenAI API (GPT) |
| Deployment | Railway (Nixpacks: Python + Node) |

## API

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Health check |
| `POST` | `/booking` | Process a booking request |

### Example

```bash
curl -X POST https://hotel-ai-booking-production.up.railway.app/booking \
  -H "Content-Type: application/json" \
  -d '{"request_text": "Hi, my name is Alex. I would like to book a room for tomorrow for 3 nights."}'
```

Response:
```json
{
  "guest_name": "Alex",
  "check_in": "2025-06-11",
  "check_out": "2025-06-14",
  "num_guests": 1,
  "stay_nights": 3,
  "booking_possible": true,
  "available_rooms": ["Room 1", "Room 2", "Room 5"],
  "split_stay": null,
  "estimated_price": 450,
  "discount_applied": null
}
```

## Running Locally

```bash
# Backend
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
echo 'OPENAI_API_KEY=your_key_here' > .env
uvicorn main:app --reload

# Frontend (dev mode with hot reload)
cd frontend && npm install && npm run dev
```

## Deployment

The app auto-deploys to Railway on push to `main`. Railway's Nixpacks builder handles both Python and Node:

1. **Build phase:** `cd frontend && npm ci && npm run build` → outputs to `static/`
2. **Start phase:** `uvicorn main:app --host 0.0.0.0 --port $PORT`

Only requirement: set `OPENAI_API_KEY` in the Railway dashboard.

## Project Structure

```
├── main.py                  # FastAPI server + static file serving
├── booking_agent.py         # Core booking logic (availability, split-stay, pricing)
├── bookings.csv             # Simulated hotel reservation data (25 rooms)
├── hotel_policy.txt         # Discount rules and hotel policies
├── frontend/                # React SPA (Vite)
│   ├── src/
│   │   ├── App.jsx          # Main app with booking form and results
│   │   └── components/      # BookingForm, BookingResult, SplitStayCard
│   └── vite.config.js       # Build output → ../static/, dev proxy
├── nixpacks.toml            # Python + Node providers for Railway
└── railway.toml             # Build and start commands
```
