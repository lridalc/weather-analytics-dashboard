# Weather Analytics Dashboard - Architecture Documentation

## Overview

The Weather Analytics Dashboard follows a layered architecture inspired by Clean Architecture and Ports & Adapters (Hexagonal Architecture). The system is designed to separate concerns clearly, isolate business logic from external dependencies, and enable multiple entry points (API and CLI) to interact with the same core functionality.

The architecture emphasizes:

- Clear boundaries between layers
- Independence of business logic from infrastructure concerns
- Testability through abstraction and dependency inversion
- Flexibility to replace external systems without impacting core logic

The core idea is simple:

> Business logic remains independent, while external concerns plug into it.

---

## High-Level Architecture

```
┌───────────────────────────────────────────────┐
│               PRESENTATION LAYER              │
│                                               │
│       API Interface        CLI Interface      │
└───────────────────────┬───────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────┐
│              APPLICATION LAYER                │
│                                               │
│        Orchestrates use cases & flow          │
└───────────────────────┬───────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────┐
│                DOMAIN LAYER                   │
│                                               │
│          Core models & business rules         │
└───────────────────────────────────────────────┘
                        ▲
                        │
┌───────────────────────┴───────────────────────┐
│            INFRASTRUCTURE LAYER               │
│                                               │
│   Weather Providers   Storage   Cache   HTTP  │
└───────────────────────────────────────────────┘
```

---

## Layer Responsibilities

### 1. Presentation Layer

The presentation layer handles all user interaction.

**Responsibilities:**

- Accept user input from API or CLI
- Validate request parameters
- Invoke application services
- Format and return responses (JSON for API, text for CLI)

The presentation layer does **not** contain business logic. It serves purely as an entry point and response formatter.

---

### 2. Application Layer

The application layer orchestrates the execution of use cases. It acts as the coordination layer between the presentation layer and the domain.

**Responsibilities:**

- Implement application-specific workflows
- Coordinate between domain logic and external systems
- Handle application-level errors
- Persist query history

This layer defines the operations that the system supports (e.g., retrieving current weather, forecasting, retrieving history).

---

### 3. Domain Layer

The domain layer contains the core business logic and domain models. It defines what weather data is and how it should be handled.

**Responsibilities:**

- Define domain entities and value objects
- Encapsulate business rules and transformations
- Define **ports (interfaces)** required by the application
- Remain **completely independent** of external systems and frameworks

The domain layer operates on **location as text** (e.g., `"Madrid"`), without knowledge of how that location is resolved.

---

### 4. Infrastructure Layer

The infrastructure layer provides concrete implementations for external dependencies required by the application.

**Responsibilities:**

- Implement weather providers (external APIs)
- Handle data persistence for query history
- Implement caching mechanisms
- Perform HTTP communication with retry logic
- Provide the shared geocoding service used by providers that require coordinate resolution

Infrastructure components implement **interfaces defined in the domain layer**, adhering to the Dependency Inversion Principle.

---

## External API Integration

Weather data retrieval is implemented through a **provider abstraction**.

### Core Principle

> Location resolution (e.g., geocoding) is an implementation detail of the provider, not a domain concern.

### Provider Model

The system defines a single domain port:

```python
class WeatherProviderPort:
    async def get_current(location: str): ...
    async def get_forecast(location: str, days: int): ...
```

- The domain works with **location as a string**
- No mention of coordinates, geocoding, or provider-specific requirements
- All provider-specific logic is encapsulated in infrastructure

---

## Provider Implementations

Each provider adapter implements `WeatherProviderPort` differently depending on external API requirements.

### Example: OpenWeatherMap

Flow inside the adapter:

1. Resolve location → coordinates (via shared `GeocodingService`)
2. Fetch weather data using coordinates
3. Return domain models

This logic is **fully internal to the adapter** and invisible to the domain and application layers.

---

## Infrastructure Services

### Geocoding Service

- Responsibility: resolve location names into coordinates
- Scope: infrastructure-only, **shared across all providers that require it**
- Not exposed as a domain port
- Includes its own in-memory cache (7-day TTL) to avoid redundant lookups

Making the geocoding service shared (rather than duplicated per provider) prevents behavioral divergence and keeps the codebase DRY, while still treating it as a pure infrastructure concern.

Example:

```python
coordinates = await geocoding_service.resolve("Madrid")
```

---

## Resilience: Retry Logic

HTTP calls to external APIs are wrapped with **automatic retry using exponential backoff**.

- Applied at the HTTP client level, transparent to providers
- Retries only on transient errors (network timeouts, 5xx responses)
- Configurable: max attempts and initial wait time
- After all retries are exhausted, a domain exception is raised

This keeps retry logic out of provider adapters and centralizes it in the HTTP layer.

---

## Caching Strategy

Caching is implemented using the **Decorator Pattern**.

### Principles

- The base provider **does not handle caching**
- Caching is applied transparently by wrapping the provider
- Keeps responsibilities separated (SRP)

### Structure

```
CachedWeatherProvider (decorator)
        ↓
Concrete Provider (e.g., OpenWeatherMapAdapter)
        ↓
GeocodingService (shared, with internal cache)
```

### Cache Types

| Cache     | TTL       | Scope                           |
| --------- | --------- | ------------------------------- |
| Geocoding | 7 days    | Shared infrastructure service   |
| Weather   | 5 minutes | Provider decorator              |

---

## Data Flow

User → API/CLI → Application → WeatherProvider → (Decorator Cache) → Provider Adapter → GeocodingService → External API → Response

---

## Weather Request Flow

1. Validate location
2. Call `WeatherProvider.get_current(location)`
3. Check cache (decorator)
4. Delegate to provider adapter
5. Resolve location via shared `GeocodingService` (uses internal cache)
6. Call external API (with retry on transient failures)
7. Return data
8. Save query history
9. Return response

---

## Application Services

- GetCurrentWeatherService
- GetForecastService
- GetHistoryService

---

## Domain Models

```python
class WeatherData:
    temperature: float
    timestamp: datetime

class ForecastData:
    min_temp: float
    max_temp: float
    avg_temp: float
```

---

## Ports

```python
class WeatherProviderPort:
    async def get_current(location): ...
    async def get_forecast(location, days): ...

class HistoryRepositoryPort:
    async def save(): ...
    async def get_last(): ...
```

---

## Error Handling

Errors are handled in layers, with explicit mapping at each boundary:

1. **Infrastructure Layer:** Catches external exceptions (e.g., HTTPX errors), wraps as domain exceptions
2. **Domain Layer:** Raises domain-specific exceptions only
3. **Application Layer:** Maps domain exceptions to error codes
4. **Presentation Layer:** Formats errors for the interface (JSON for API, text for CLI)

Infrastructure failures never leak to clients. The same error taxonomy is applied consistently across both interfaces.

---

## Cross-Cutting Concerns

### Configuration

- Centralized configuration via a `pydantic-settings` module
- Configuration is loaded from environment variables or a `.env` file
- Infrastructure-specific details (such as the provider API key) are read using generic variable names (e.g., `WEATHER_API_KEY`) to maintain abstraction and avoid coupling the configuration layer to a specific vendor

### Logging

- Request logs
- External API call logs

### Observability (future)

- Cache metrics
- Latency tracking

---

## Deployment (v1.0)

- Single FastAPI application
- Local file-based persistence (SQLite)
- In-memory cache

---

## Key Architectural Decisions Reflected

- Domain depends only on **abstractions, not implementations**
- External API details are **fully encapsulated in providers**
- Geocoding is treated as an **internal infrastructure concern**, implemented as a **shared service**
- Caching is applied via **composition (decorator), not inheritance**
- Retry logic is centralized at the **HTTP layer**, not scattered across adapters
- System is designed for **extensibility without modifying core logic**
