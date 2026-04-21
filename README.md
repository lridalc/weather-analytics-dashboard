# 🌦 Weather Analytics Dashboard

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.135+-green.svg)](https://fastapi.tiangolo.com/)
[![uv](https://img.shields.io/badge/uv-Package%20Manager-purple.svg)](https://github.com/astral-sh/uv)
[![SQLite](https://img.shields.io/badge/SQLite-Async-blue.svg)](https://www.sqlite.org/)
[![Architecture](https://img.shields.io/badge/architecture-clean%20architecture-blue)](docs/architecture.md)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A production-style weather data service with intelligent caching, query history, and dual interfaces (REST API + CLI). Built to demonstrate **clean architecture, async Python, and real-world backend patterns**.

> [!IMPORTANT]
> 🚧 **PROJECT STATUS:** Architecture and documentation completed. Development in progress — vertical slice (/weather/current endpoint) currently being implemented.

[![CI Pipeline](https://github.com/lridalc/weather-analytics-dashboard/actions/workflows/ci.yaml/badge.svg)](https://github.com/lridalc/weather-analytics-dashboard/actions/workflows/ci.yaml)

> [!NOTE]
> OpenWeatherMap was initially considered as first weather provider, but Open-Meteo has been selected as the preferred provider to simplify the MVP, as it does not require an API key. See [ADR-024](docs/decisions.md/#adr-024-mvp-weather-provider-selection).

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
| 0.1.0   | Foundation (`/health`)                   | ✅     |
| 0.2.0   | Current Weather API (`/weather/current`) | 🚧     |
| 0.3.0   | Forecast System (`/weather/forecast`)    | -      |
| 0.4.0   | History Persistence (`/weather/history`) | -      |
| 0.5.0   | Retry & Resilience                       | -      |
| 0.6.0   | Caching Layer                            | -      |
| 1.0.0   | Production Release                       | -      |

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

- [x] `/health` endpoint implementation
- [x] Health check tests
- [x] Minimal API wiring validation

---

#### Current Weather (Vertical Slice #1)

- [x] Domain models for weather
- [x] Use case: get current weather
- [ ] Geocoding service (shared infrastructure)
- [ ] Open-Meteo adapter integration
- [ ] `/weather/current` endpoint with error mapping
- [ ] CLI: `weather now <city>`
- [ ] Full integration tests

---

#### Forecast (Vertical Slice #2)

- [ ] Forecast domain model
- [ ] Forecast use case implementation
- [ ] Open-Meteo adapter extension for forecasts
- [ ] `/weather/forecast` endpoint with error mapping
- [ ] CLI: `weather forecast <city> --days N`

---

#### History System (Vertical Slice #3)

- [ ] History domain contracts (port + models)
- [ ] SQLite repository with aiosqlite
- [ ] FIFO eviction (max 10 entries per city)
- [ ] History retrieval service
- [ ] Automatic query persistence on current
- [ ] `/weather/history` endpoint with error mapping
- [ ] CLI: `weather history <city>`

---

#### Resilience & Retry Logic

- [ ] HTTP client with exponential backoff (tenacity)
- [ ] Global rate limiting (quota protection)
- [ ] Migration of OpenMeteoAtapter to retry-enabled client
- [ ] Retry only on transient errors (5xx, timeouts)

---

#### Caching Layer

- [ ] Weather cache decorator (5 min TTL)
- [ ] FIFO eviction for weather cache
- [ ] Geocoding cache (7 days TTL, internal to service)
- [ ] Cache hit/miss integration tests
- [ ] Dependency wiring for cached provider

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

### Example: Open-Meteo (MVP)

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
├── docs/                                  # Architecture, ADRs, and development planning
│   ├── architecture.md
│   ├── decisions.md
│   ├── development-plan.md
│   └── project-scope.md
│
├── src/weather_analytics_dashboard/
│   ├── application/                       # Use cases (business workflows)
│   │   └── services/
│   │       └── get_current_weather.py
│   ├── config/                            # Configuration, settings, constants, and exceptions
│   │   ├── constants.py
│   │   ├── exceptions.py
│   │   ├── logging.py
│   │   └── settings.py
│   ├── domain/                            # Core business logic and models
│   │   ├── exceptions.py
│   │   ├── models.py
│   │   └── ports.py
│   ├── infrastructure/                    # External systems (DB, APIs, cache)
│   ├── presentation/                      # Interfaces (API + CLI)
│   │   ├── api/
│   │   │   ├── app.py
│   │   │   ├── dependencies.py
│   │   │   ├── routes/
│   │   │   │   └── health.py
│   │   │   └── schemas/
│   │   │       └── health.py
│   │   └── cli/
│   │       └── main.py
│   ├── bootstrap.py                       # Dependency injection and app initialization
│   └── main.py                            # Application entry point
│
├── tests/
│   ├── integration/                       # Integration tests (API, DB)
│   │   ├── bootstrap/
│   │   ├── config/
│   │   ├── presentation/
│   │   │   ├── api/
│   │   │   └── cli/
│   │   └── test_00_smoke.py
│   ├── unit/                              # Unit tests (domain & services)
│   │   └── config/
│   │       └── test_settings.py
│   └── conftest.py                        # Pytest fixtures and configuration
│
├── .github/                               # CI/CD workflows, actions, and PR templates
│   ├── actions/
│   ├── workflows/
│   └── pull_request_template.md
│
├── Makefile                               # Development commands
├── pyproject.toml                         # Project configuration and dependencies
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

| Variable                     | Required | Default |
| ---------------------------- | :------: | ------- |
| `RATE_LIMIT_RPM`             | ❌       | 250     |
| `CACHE_TTL_WEATHER`          | ❌       | 300     |
| `CACHE_TTL_GEOCODING`        | ❌       | 604800  |
| `CACHE_MAX_SIZE`             | ❌       | 100     |
| `REQUEST_TIMEOUT_SECONDS`    | ❌       | 10      |
| `RETRY_MAX_ATTEMPTS`         | ❌       | 3       |
| `RETRY_INITIAL_WAIT_SECONDS` | ❌       | 1       |
| `ENVIRONMENT`                | ❌       | DEV     |
| `LOG_LEVEL`                  | ❌       | INFO    |

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

> [!TIP]  
> Running `make` without arguments shows all availble commands (equivalent to `make help`).  
> 💡 All commands use `uv run` internally, so you don’t need to manually activate a virtual environment.

---

### 📦 Installation

```bash
make all          # Install everything necessary for development (install-dev + pre-commit)
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
make test              # Run all tests
make test-smoke        # Run smoke tests
make test-bootstrap    # Run bootstrap tests
make test-unit         # Run unit tests
make test-integration  # Run integration tests
make test-cov          # Run tests with coverage report
```

All tests are run with verbose output.

---

### 🎨 Code Quality

```bash
make lint         # Run ruff linter
make format       # Auto-format code
make format-diff  # Show formatting differences without applying changes
make format-check # Check formatting without modifying files
make type-check   # Run mypy static type checking
```

---

### 🔧 Git Hooks

```bash
make pre-commit                    # Install pre-commit hooks
make pre-commit-force              # Force reinstall pre-commit hooks
make pre-commit-all                # Run all hooks on all files
make pre-commit-run HOOK=ruff      # Run specific hook
make pre-commit-update             # Update hooks to latest versions
make pre-commit-uninstall          # Uninstall pre-commit hooks
```

---

### ✅ Full project checks

```bash
make check
```

Runs all quality checks:

- Linting (ruff)
- Formatting validation (ruff)
- Tests (pytest)
- Type checking (mypy)

---

### 🧹 Cleanup

```bash
make clean
```

Removes cache files and temporary artifacts:

- `__pycache__`
- `.pyc`
- `.mypy_cache`
- `.pytest_cache`
- `.ruff_cache`

---

### 🚢 Release

```bash
make version                      # Show current version
make release                      # Show release process steps
make release VERSION=0.2.0        # Execute release (creates tag, pushes, syncs branches)
```

---

### 🚦 CI Validation

```bash
make ci                           # Run complete CI pipeline locally (same as GitHub Actions)
```

---

### 📋 Help

```bash
make help
```

Displays all available commands (default).

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
