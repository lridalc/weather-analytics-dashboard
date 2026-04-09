# Weather Analytics Dashboard - Project Scope

## Project Overview

The Weather Analytics Dashboard is a portfolio project demonstrating proficiency in building a production-ready weather data service. The application provides real-time weather information, forecasts, and query history through both a REST API and a command-line interface.

## Core Objectives

- Build a reliable weather data service that integrates with OpenWeatherMap.
- Implement efficient data fetching with appropriate caching strategies.
- Provide both programmatic (API) and interactive (CLI) access to weather information.
- Implement efficient caching to reduce external API calls and improve response times.
- Maintain a local history of weather queries for analytics and audit purposes.
- Handle transient external API failures gracefully through retry logic.
- Showcase clean architecture, testing practices, and professional documentation.

---

## Functional Requirements

### API Service

| Endpoint | Method | Description | Query Parameters |
|----------|--------|-------------|------------------|
| `/weather/current` | GET | Retrieve current temperature for a city | `city` (required) |
| `/weather/forecast` | GET | Forecast data | `city` (required), `days` (default: 5) |
| `/weather/history` | GET | Last 10 queries for a city | `city` (required) |
| `/health` | GET | Health check | None |

**Response Details:**

- Current: temperature in Celsius
- Forecast: min, max, avg per day
- History: timestamps + past results
- Consistent JSON responses

### Command Line Interface

| Command | Description | Arguments/Options |
|---------|-------------|-------------------|
| `weather now <city>` | Display current weather for specified city | City name (positional) |
| `weather forecast <city>` | Display forecast for specified city | `--days` option (default: 5) |
| `weather history <city>` | Display local query history for city | City name (positional) |

### Caching System

- In-memory dictionary cache
- TTL-based expiration
- Separate caches:
  - Geocoding (7 days) — managed by the shared geocoding service
  - Weather (5 minutes) — managed by the provider decorator
- FIFO eviction strategy

### Retry Logic

- Automatic retry on transient external API failures
- Exponential backoff strategy
- Configurable: max attempts and initial wait time
- Applies only to recoverable errors (network timeouts, 5xx responses)

### Query History Storage

- Store each successful weather query locally
- Record includes: city name, timestamp, temperature data, request type
- Maximum 10 most recent entries per city (FIFO eviction)
- History persists across application restarts

---

## Non-Functional Requirements

### Performance
- <200ms for cached responses
- Non-blocking API calls

### Reliability
- Graceful API failure handling
- Retry with exponential backoff for transient errors
- Cache fallback strategy

### Maintainability
- Clean architecture
- High test coverage

### Usability
- Simple CLI
- Clear API errors

---

## Error Handling

```json
{
  "error": {
    "code": "STRING",
    "message": "Human-readable message"
  }
}
```

### Error Codes

| Code               | Description                              |
| ------------------ | ---------------------------------------- |
| INVALID_INPUT      | Bad request parameters                   |
| CITY_NOT_FOUND     | Geocoding failed — location not resolved |
| EXTERNAL_API_ERROR | External API failure after retries       |
| INTERNAL_ERROR     | Unexpected server-side error             |

---

## Configuration

| Variable              | Description              | Default    |
| --------------------- | ------------------------ | ---------- |
| `OPENWEATHER_API_KEY` | OpenWeatherMap key       | Required   |
| `CACHE_TTL_WEATHER`   | Weather TTL (seconds)    | 300        |
| `CACHE_TTL_GEOCODING` | Geocoding TTL (seconds)  | 604800     |
| `CACHE_MAX_SIZE`      | Cache size (entries)     | 100        |
| `DATABASE_URL`        | SQLite path              | weather.db |
| `RETRY_MAX_ATTEMPTS`  | Max retry attempts       | 3          |
| `RETRY_WAIT_SECONDS`  | Initial backoff (seconds)| 1          |

---

## Assumptions

* City names are valid English strings
* External API is mostly available (transient failures handled via retry)
* Single-process execution

---

## Risks & Mitigations

| Risk                        | Mitigation                           |
| --------------------------- | ------------------------------------ |
| Rate limiting               | Cache aggressively                   |
| Transient API failures      | Retry with exponential backoff       |
| Extended API downtime       | Return cached data if available      |
| Memory growth               | FIFO eviction                        |
| Geocoding logic duplication | Shared geocoding service             |

---

## Out of Scope

* Authentication
* Multiple temperature units
* GUI
* Multi-provider support (v1.0)

## Success Criteria

1. All endpoints work correctly
2. CLI behaves correctly
3. Cache reduces external API calls by ~60%
4. Query history persists across restarts
5. Retry logic handles transient failures transparently
6. Tests pass

## Project Deliverables

* Source code
* README
* ADRs
* API docs
* CLI docs
* Tests

---

> [!NOTE]
> This document defines the project scope and requirements. Technical decisions regarding specific libraries, frameworks, or architectural patterns will be documented separately through Architecture Decision Records. See `architecture.md` and `decisions.md` for technical specifications.