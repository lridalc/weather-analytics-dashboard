# 🌦 Weather Analytics Dashboard

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.135+-green.svg)](https://fastapi.tiangolo.com/)
[![uv](https://img.shields.io/badge/uv-Package%20Manager-purple.svg)](https://github.com/astral-sh/uv)
[![SQLite](https://img.shields.io/badge/SQLite-Async-blue.svg)](https://www.sqlite.org/)
[![Architecture](https://img.shields.io/badge/architecture-clean%20architecture-blue)](docs/architecture.md)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A production-style weather data service with intelligent caching, query history, and dual interfaces (REST API + CLI). Built to demonstrate **clean architecture, async Python, and real-world backend patterns**.

> 🚧 **PROJECT STATUS:** Architecture and documentation completed. Development in progress — vertical slice (/health endpoint) currently being implemented.

---

## 🎯 Why This Project Exists

This is a **portfolio project** designed to demonstrate:

- Clean Architecture (Ports & Adapters)
- Async Python across the entire stack
- Separation of concerns (API / domain / infrastructure)
- External API integration with caching, retry logic, and fallback strategies
- Professional engineering practices (ADRs, testing strategy, documentation)

---

## 🚀 Quick Start

```bash
git clone https://github.com/lridalc/weather-analytics-dashboard
cd weather-analytics-dashboard

# Install dependencies
make install-dev

# Configure environment
cp .env.example .env
# Add your OpenWeatherMap API key (https://openweathermap.org/api)
# The .env file expects: API_KEY=your_api_key_here

# Run API
make dev

# Test endpoints
curl http://localhost:8000/health
curl "http://localhost:8000/weather/current?city=London"

# CLI usage
make cli now London
```

---

## 🗺️ Development Roadmap

This project follows a **vertical-slice, test-driven development approach**, where each milestone delivers a fully working feature across all layers.

> [!NOTE]
> For a more detailed insight, see [development plan](docs/development-plan.md).

---

### 📦 Version Milestones

| Version | Focus                                    | Status |
| :-----: | ---------------------------------------- | :----: |
| 0.1.0   | Foundation (`/health`)                   | [ ]    |
| 0.2.0   | Current Weather API (`/weather/current`) | [ ]    |
| 0.3.0   | Forecast System (`/weather/forecast`)    | [ ]    |
| 0.4.0   | History Persistence (`/weather/history`) | [ ]    |
| 0.5.0   | Retry & Resilience                       | [ ]    |
| 0.6.0   | Caching Layer                            | [ ]    |
| 1.0.0   | Production Release                       | [ ]    |

---

### 🧱 Development Phases

#### 🚀 Foundation & Setup

- [x] Project scaffolding
- [x] Documentation structure (README, ADRs, scope)
- [x] Smoke tests (API + CLI)
- [x] CI/CD pipeline setup and automation
- [x] Settings & configuration system
- [x] Base FastAPI application bootstrap

---

#### Health Endpoint (Vertical Slice #0)

- [ ] `/health` endpoint implementation
- [ ] Health check tests
- [ ] Minimal API wiring validation

---

#### Current Weather (Vertical Slice #1)

- [ ] Domain models for weather
- [ ] Use case: get current weather
- [ ] OpenWeatherMap adapter integration
- [ ] `/weather/current` endpoint
- [ ] CLI: `weather now <city>`
- [ ] Full integration tests

---

#### Forecast (Vertical Slice #2)

- [ ] Forecast domain logic
- [ ] Forecast use case implementation
- [ ] `/weather/forecast` endpoint
- [ ] CLI: `weather forecast <city>`
- [ ] External API extension for forecasts

---

#### History System (Vertical Slice #3)

- [ ] SQLite schema + repository
- [ ] Persist query history
- [ ] `/weather/history` endpoint
- [ ] CLI: `weather history <city>`
- [ ] FIFO cleanup (max 10 entries)

---

#### Resilience & Retry Logic

- [ ] Retry mechanism with exponential backoff
- [ ] Configurable retry settings
- [ ] Handling 5xx and timeout errors
- [ ] Failure simulation tests

---

#### Caching Layer

- [ ] Weather cache (5 min TTL)
- [ ] Geocoding cache (7 days TTL)
- [ ] FIFO eviction strategy
- [ ] Cache decorator implementation
- [ ] Cache hit/miss tests
- [ ] Cached fallback on failure

---

### 🎯 Final Release (v1.0.0)

- [ ] All endpoints complete
- [ ] CLI feature parity with API
- [ ] Full async execution (no blocking I/O)
- [ ] Clean Architecture enforced across layers
- [ ] High test coverage achieved
- [ ] Production-ready documentation

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

### ⚡ Smart Caching

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

- Automatic retry with exponential backoff on transient external API failures
- Global rate limiting (55 req/min) to protect the external API quota
- Graceful degradation when the provider is unavailable

---

### 📜 Query History

- SQLite persistence
- Last 10 queries per location
- FIFO eviction
- Survives restarts

---

### 🔄 Async Throughout

- FastAPI (ASGI)
- HTTPX (non-blocking HTTP)
- SQLAlchemy async + aiosqlite

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

- **Provider Pattern (Port + Adapter)** → external weather services abstraction
- **Repository Pattern** → database abstraction
- **Decorator Pattern** → caching layer
- **Service Layer** → use case orchestration
- **Dependency Injection** → testability

📚 Documentation:

- [`docs/architecture.md`](docs/architecture.md)
- [`docs/decisions.md`](docs/decisions.md)

---

## 🌐 External API Integration

Weather data retrieval is **provider-driven**:

- The domain interacts with a single abstraction: `WeatherProvider`
- Each provider implementation decides how to resolve a location

### Example: OpenWeatherMap

1. Resolve location → coordinates (via shared geocoding service)
2. Fetch weather data using coordinates

This logic is **fully encapsulated inside the provider adapter**, keeping the domain and application layers independent of provider-specific requirements.

✔ No geocoding concepts leak into the domain
✔ Shared geocoding service prevents logic duplication across providers
✔ Easy to swap providers without changing business logic

---

## 📁 Project Structure

The current structure is the foundational layer. The system will evolve incrementally following the design defined in [ADR-023](docs/decisions.md).

```bash
.
├── docs/                  # Architecture, ADRs, and development planning
│   ├── architecture.md
│   ├── decisions.md
│   ├── development-plan.md
│   └── project-scope.md
│
├── src/weather_analytics_dashboard/
│   ├── application/       # Use cases (business workflows)
│   ├── domain/            # Core business logic and models
│   ├── infrastructure/    # External systems (DB, APIs, cache)
│   ├── presentation/      # Interfaces (API + CLI)
│   │   ├── api/
│   │   └── cli/
│   └── main.py            # Application entry point
│
├── tests/
│   ├── unit/              # Unit tests (domain & services)
│   └── integration/       # Integration tests (API, DB)
│
├── .github/               # CI/CD and PR templates
├── Makefile               # Development commands
├── pyproject.toml         # Project configuration
└── README.md
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
make test
```

---

## ⚙️ Configuration

| Variable              | Required | Default |
| --------------------- | :------: | ------- |
| `API_KEY`             | ✅       | —       |
| `CACHE_TTL_WEATHER`   | ❌       | 300     |
| `CACHE_TTL_GEOCODING` | ❌       | 604800  |
| `CACHE_MAX_SIZE`      | ❌       | 100     |
| `RATE_LIMIT_REQUESTS` | ❌       | 55      |
| `RETRY_MAX_ATTEMPTS`  | ❌       | 3       |
| `RETRY_WAIT_SECONDS`  | ❌       | 1       |
| `LOG_LEVEL`           | ❌       | INFO    |

---

## 📊 Performance

| Metric          | Expected   |
| --------------- | ---------- |
| Cached response | <200ms     |
| Cache hit rate  | ~60–90%    |
| Memory usage    | <50MB      |

---

## 🛠️ Development Commands

This project uses a `Makefile` to standardize development workflows and ensure consistency across environments.

> 💡 All commands are executed via `uv run`, so you don’t need to manually activate a virtual environment.

---

### 📦 Installation

```bash
make install      # Install production dependencies
make install-dev  # Install all dependencies including development tools
```

---

### 🚀 Running the application

```bash
make dev  # Run API with hot reload (development)
make run  # Run API without reload (production-like)
make cli  # Run CLI tool
```

---

### 🧪 Testing

```bash
make test
```

Runs the full test suite with verbose output.

---

### 🎨 Code Quality

```bash
make lint         # Run ruff linter
make format       # Auto-format code
make format-check # Check formatting without modifying files
make type-check   # Run mypy static type checking
```

---

### ✅ Full project checks

```bash
make check
```

Runs all quality checks:

* Linting (ruff)
* Formatting validation
* Tests (pytest)
* Type checking (mypy)

---

### 🧹 Cleanup

```bash
make clean
```

Removes cache files and temporary artifacts:

* `__pycache__`
* `.pyc`
* `.mypy_cache`
* `.pytest_cache`
* `.ruff_cache`

---

### 📋 Help

```bash
make help
```

Displays all available commands.

---

## 🚢 Deployment

### Local

```bash
gunicorn weather_analytics_dashboard.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker
```

### Planned

- Redis cache
- Docker support
- Cloud deployment (Railway / Render)

---

## 📈 Future Roadmap

- [ ] Metrics endpoint (Prometheus)
- [ ] Redis cache
- [ ] PostgreSQL support
- [ ] Docker

---

## 📝 License

[MIT License](LICENSE)

---

## 👤 Author

**lridalc** - <https://github.com/lridalc>

**Project Link** - <https://github.com/lridalc/weather-analytics-dashboard>

---

## 💡 What This Project Demonstrates

This project is intentionally designed to reflect **real-world backend engineering**, including:

- Clear architectural boundaries
- Explicit trade-offs (documented via ADRs)
- Provider abstraction without leaking infrastructure details
- Resilience patterns (retry with exponential backoff)
- Async-first design
- Testable, modular components

This project was built to practice designing a production-ready backend system from scratch, focusing on maintainability, scalability, and real-world trade-offs.

It is not just a weather API wrapper—it is a **system design exercise implemented in code**.