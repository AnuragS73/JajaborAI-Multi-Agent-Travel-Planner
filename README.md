# Jajabor AI (যাযাবর)

**Intelligence Meets Exploration**

Jajabor AI is a personal multi-agent AI travel planner for exploring India. It combines flight information, hotel recommendations, day-wise itineraries and estimated travel budgets in a single web interface.

## Features

- Flight information using Aviationstack API
- Hotel recommendations using Tavily Search
- AI-generated itineraries and estimated trip budgets
- Persistent workflow state using PostgreSQL
- Web interface powered by FastAPI

## Tech Stack

- **Python:** 3.13.9
- **AI:** LangChain, LangGraph, Groq (`openai/gpt-oss-120b`)
- **Frontend:** HTML, CSS, JavaScript, Jinja2
- **Backend:** FastAPI, Uvicorn
- **Database:** PostgreSQL
- **Deployment:** Docker, Render (planned)

## Agent Workflow

```mermaid
flowchart LR
    A[User Query] --> B[Flight Agent]
    B --> C[Hotel Agent]
    C --> D[Itinerary Agent]
    D --> E[Final Agent]
    E --> F[Travel Plan]
```

## Project Structure

```text
JajaborAI-Multi-Agent-Travel-Planner/
├── static/
│   ├── script.js
│   └── style.css
├── templates/
│   └── index.html
├── tools/
│   ├── flight_tool.py
│   └── tavily_tool.py
├── utils/
│   └── airport_mappings.py
├── .env (local only)
├── .gitignore
├── .dockerignore
├── app.py
├── backend.py
├── Dockerfile
├── LICENSE
├── README.md
├── requirements.txt
└── test.py
```

## Getting Started

Run the following commands from the project root using Windows PowerShell.

### 1. Create and activate a virtual environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root and add your credentials:

```dotenv
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
AVIATIONSTACK_API_KEY=your_aviationstack_api_key
DATABASE_URL=your_postgresql_connection_url
LANGSMITH_TRACING=false
```

Do not commit `.env` or database credentials to GitHub.

### 4. Test the backend

```powershell
python test.py
```

### 5. Run the application

```powershell
python app.py
```

Open http://127.0.0.1:8000 in your browser.

## Run with Docker (Optional)

```powershell
docker build -t jajabor-ai .
docker run --env-file .env -p 8000:8000 jajabor-ai
```

## Example Query

> Plan a 5-day Kashmir trip from Bengaluru, including flights, hotels and sightseeing, within a budget of ₹1 lakh.

## Project Status

Under active development. Render deployment is planned. Flight information depends on API availability, and budget estimates are indicative. The application does not support actual travel bookings.

## License

MIT License.