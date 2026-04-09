# 🌦 Weather Analytics Dashboard

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.135+-green.svg)](https://fastapi.tiangolo.com/)
[![uv](https://img.shields.io/badge/uv-Package%20Manager-purple.svg)](https://github.com/astral-sh/uv)
[![SQLite](https://img.shields.io/badge/SQLite-Async-blue.svg)](https://www.sqlite.org/)
[![Architecture](https://img.shields.io/badge/architecture-clean%20architecture-blue)](docs/architecture.md)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A production-style weather data service with intelligent caching, query history, and dual interfaces (REST API + CLI). Built to demonstrate **clean architecture, async Python, and real-world backend patterns**.

---

## 🎯 Why This Project Exists

This is a **portfolio project** designed to demonstrate:

* Clean Architecture (Ports & Adapters)
* Async Python across the entire stack
* Separation of concerns (API / domain / infrastructure)
* External API integration with caching, retry logic, and fallback strategies
* Professional engineering practices (ADRs, testing strategy, documentation)

---

## 🚀 Quick Start

```bash
git clone https://github.com/lridalc/weather-analytics-dashboard
cd weather-analytics-dashboard

# Install dependencies
uv sync

# Configure environment
cp .env.example .env
# Add your OpenWeatherMap API key (https://openweathermap.org/api)

# Run API
uv run uvicorn src.weather_analytics_dashboard.main:app --reload

# Test endpoints
curl http://localhost:8000/health
curl "http://localhost:8000/weather/current?city=London"

# CLI usage
uv run weather now London
```

---

## ✨ Features

### 🌍 REST API

| Endpoint            | Description         |
| ------------------- | ------------------- |
| `/weather/current`  | Current temperature |
| `/weather/forecast` | Multi-day forecast  |
| `/weather/history`  | Last 10 queries     |
| `/health`           | Service health      |

✔ Automatic OpenAPI docs at `/docs`

---

### 🖥 CLI Interface

```bash
weather now Madrid
weather forecast Paris --days 5
weather history Tokyo
```

Same business logic as API → different interface.

---

### ⚡ Smart Caching (Key Feature)

Two-layer cache system:

| Layer     | TTL       | Purpose             |
| --------- | --------- | ------------------- |
| Geocoding | 7 days    | Location resolution |
| Weather   | 5 minutes | Weather data        |

✔ Reduces API calls significantly
✔ Improves response time (<200ms cached)
✔ FIFO eviction prevents memory leaks

**Architectural note:** These two caches operate at different layers:
- Weather cache wraps the domain port (system-wide)
- Geocoding cache is internal to the shared geocoding service (infrastructure detail)

From a user perspective, both contribute to performance optimization.

---

### 🔁 Resilience

* Automatic retry with exponential backoff on transient external API failures
* Graceful degradation when the provider is unavailable

---

### 📜 Query History

* SQLite persistence
* Last 10 queries per location
* FIFO eviction
* Survives restarts

---

### 🔄 Async Throughout

* FastAPI (ASGI)
* HTTPX (non-blocking HTTP)
* SQLAlchemy async + aiosqlite

✔ No blocking I/O
✔ Efficient concurrent handling

---

## 🏗 Architecture

This project follows **Clean Architecture + Ports & Adapters**:

```
Presentation (API / CLI)
        ↓
Application (Use Cases)
        ↓
Domain (Business Logic)
        ↑
Infrastructure (DB, Cache, External APIs)
```

### Key Patterns

* **Provider Pattern (Port + Adapter)** → external weather services abstraction
* **Repository Pattern** → database abstraction
* **Decorator Pattern** → caching layer
* **Service Layer** → use case orchestration
* **Dependency Injection** → testability

📚 Documentation:

* [`docs/architecture.md`](docs/architecture.md)
* [`docs/decisions.md`](docs/decisions.md)

---

## 🌐 External API Integration

Weather data retrieval is **provider-driven**:

* The domain interacts with a single abstraction: `WeatherProvider`
* Each provider implementation decides how to resolve a location

### Example: OpenWeatherMap

1. Resolve location → coordinates (via shared geocoding service)
2. Fetch weather data using coordinates

This logic is **fully encapsulated inside the provider adapter**, keeping the domain and application layers independent of provider-specific requirements.

✔ No geocoding concepts leak into the domain
✔ Shared geocoding service prevents logic duplication across providers
✔ Easy to swap providers without changing business logic

---

## 📁 Project Structure

```bash
src/weather_analytics_dashboard/
├── presentation/
│   ├── api/
│   └── cli/
│
├── application/
│   └── services/
│
├── domain/
│   ├── models.py
│   └── ports.py
│
├── infrastructure/
│   ├── weather_providers/
│   │   └── openweather_adapter.py
│   │
│   ├── geocoding/
│   │   └── geocoding_service.py
│   │
│   ├── cache/
│   │   ├── in_memory_cache.py
│   │   └── cached_provider.py
│   │
│   ├── persistence/
│   │   ├── orm_models.py
│   │   └── repository.py
│   │
│   └── http/
│       └── client_manager.py
│
├── config/
│   └── settings.py
│
└── main.py
```

---

## 📡 Example API Responses

### ✅ Current Weather

```http
GET /weather/current?city=London
```

```json
{
  "city": "London",
  "temperature": 18.5,
  "timestamp": "2026-04-08T12:00:00Z"
}
```

---

### 📅 Forecast

```http
GET /weather/forecast?city=London&days=3
```

```json
{
  "city": "London",
  "forecast": [
    {
      "date": "2026-04-09",
      "min_temp": 12.1,
      "max_temp": 19.3,
      "avg_temp": 15.7
    }
  ]
}
```

---

### 🕘 Query History

```http
GET /weather/history?city=London
```

```json
{
  "city": "London",
  "history": [
    {
      "timestamp": "2026-04-08T12:00:00Z",
      "temperature": 18.5
    }
  ]
}
```

---

### ❗ Error Response

```json
{
  "error": {
    "code": "CITY_NOT_FOUND",
    "message": "Location could not be resolved"
  }
}
```

---

## 🧪 Testing Strategy

| Type        | Scope              |
| ----------- | ------------------ |
| Unit        | Domain + services  |
| Integration | API + DB           |
| Mocks       | External providers |

```bash
uv run pytest -v
uv run pytest --cov=src/weather_analytics_dashboard
```

---

## ⚙️ Configuration

| Variable              | Required | Default |
| --------------------- | -------- | ------- |
| `OPENWEATHER_API_KEY` | ✅       | —       |
| `CACHE_TTL_WEATHER`   | ❌       | 300     |
| `CACHE_TTL_GEOCODING` | ❌       | 604800  |
| `CACHE_MAX_SIZE`      | ❌       | 100     |
| `DATABASE_URL`        | ❌       | sqlite  |
| `LOG_LEVEL`           | ❌       | INFO    |
| `RETRY_MAX_ATTEMPTS`  | ❌       | 3       |
| `RETRY_WAIT_SECONDS`  | ❌       | 1       |

---

## 📊 Performance

| Metric          | Expected   |
| --------------- | ---------- |
| Cached response | <200ms     |
| Cache hit rate  | ~60–90%    |
| Memory usage    | <50MB      |

---

## 🚢 Deployment

### Local

```bash
gunicorn src.weather_analytics_dashboard.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker
```

### Planned

* Redis cache
* Docker support
* Cloud deployment (Railway / Render)

---

## 📈 Roadmap

* [ ] Metrics endpoint (Prometheus)
* [ ] Redis cache
* [ ] PostgreSQL support
* [ ] Docker

---

## 📝 License

[MIT License](LICENSE)

---

## 👤 Author

**lridalc** - [https://github.com/lridalc](https://github.com/lridalc)

**Project Link** - [https://github.com/lridalc/weather-analytics-dashboard](https://github.com/lridalc/weather-analytics-dashboard)

---

## 💡 What This Project Demonstrates

This project is intentionally designed to reflect **real-world backend engineering**, including:

* Clear architectural boundaries
* Explicit trade-offs (documented via ADRs)
* Provider abstraction without leaking infrastructure details
* Resilience patterns (retry with exponential backoff)
* Async-first design
* Testable, modular components

It is not just a weather API wrapper—it is a **system design exercise implemented in code**.