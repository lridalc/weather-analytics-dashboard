# Weather Analytics Dashboard - Architecture Decision Records (ADRs)

## Project Context

**Purpose:** Portfolio project demonstrating modern Python practices for a data-focused web application.

**Scale:** Local development + potential public demo (<100 requests/day expected)

**Core constraint:** OpenWeatherMap free tier limits (60 calls/minute)

---

## Guiding Principles

1. **Simplicity until proven otherwise (YAGNI)** – Start minimal, add complexity only when metrics justify it
2. **Async everywhere** – Consistency across layers > micro-optimizations
3. **Clear boundaries** – Domain must remain independent from infrastructure
4. **Encapsulation of external complexity** – Provider-specific logic must not leak into the domain
5. **Pragmatic abstraction** – Introduce abstractions only when they provide clear value
6. **Documentation as code** – ADRs + OpenAPI + type hints + docstrings

---

## Non-decisions (obvious choices not requiring ADRs)

- Python 3.12+ with `uv` as package manager
- `ruff` for linting/formatting (fast, replaces flake8/black/isort)
- Type hints on all public APIs (mypy strict mode)

---

## How to read these ADRs

Each ADR follows this structure:

- **Status:** Accepted / Deprecated / Superseded
- **Context:** Why we need to decide this
- **Decision:** What we chose
- **Consequences:** Positive and negative outcomes
- **When to revisit:** Conditions that would trigger reconsideration

---

# FOUNDATIONAL ARCHITECTURE DECISIONS

## ADR-001: Ports (Interfaces) in Domain Layer

### Status

Accepted

### Context

Clean Architecture requires clear abstraction boundaries between business logic and infrastructure. A key design question is where these abstractions should be defined.

### Decision

All ports (interfaces) are defined in the domain layer (`domain/ports.py`).

### Rationale

- The domain defines **what capabilities are required**
- Infrastructure provides implementations
- Application orchestrates interactions

This enforces Dependency Inversion across the system.

### Consequences

**Positive:**

- Clear dependency direction (outer → inner)
- High testability via mocks
- Infrastructure can be replaced without affecting core logic

**Negative:**

- Requires discipline to keep ports technology-agnostic
- Adds boilerplate

### When to Revisit

If a port becomes purely technical and loses business meaning.

---

## ADR-002: Async Throughout vs Mixed Sync/Async

### Status

Accepted

### Context

The system performs multiple I/O-bound operations:

- External API calls
- Database access
- Concurrent request handling

Mixing sync and async introduces complexity and risk of blocking.

### Decision

Use async/await consistently across all layers.

### Chosen Stack

- FastAPI
- HTTPX
- SQLAlchemy async + aiosqlite

### Consequences

**Positive:**

- Efficient concurrency
- No blocking I/O
- Unified programming model

**Negative:**

- Higher complexity for debugging
- Async testing setup required

### When to Revisit

If CPU-bound workloads dominate execution time.

---

## ADR-003: Pydantic v2 for All Data Validation

### Status

Accepted

### Context

Validation is required for API input, external responses, and internal data consistency.

### Decision

Use Pydantic v2 for all validation and serialization.

### Consequences

**Positive:**

- Single source of truth for data schemas
- Automatic OpenAPI generation
- Strong typing and validation

**Negative:**

- Learning curve
- Slight overhead vs raw structures

### When to Revisit

If validation becomes a performance bottleneck or requirements change significantly.

---

## ADR-004: Layered Error Handling Strategy

### Status

Accepted

### Context

Errors can occur at multiple architectural layers:

- Presentation: invalid inputs, malformed requests
- Application: business rule violations, orchestration failures
- Domain: domain invariants broken
- Infrastructure: network failures, API errors, database issues

Without a consistent strategy, errors become:

- Leaky (infrastructure details exposed to clients)
- Inconsistent (different formats per layer)
- Untestable (tight coupling to implementation)

### Decision

Implement layered error handling with explicit mapping at each boundary:

1. **Infrastructure Layer:** Catch external exceptions, wrap as domain errors
2. **Domain Layer:** Raise domain-specific exceptions only
3. **Application Layer:** Map domain exceptions to application error codes
4. **Presentation Layer:** Format errors for interface (JSON for API, text for CLI)

### Error Code Taxonomy

| Code               | Description                              |
| ------------------ | ---------------------------------------- |
| INVALID_INPUT      | Bad request parameters                   |
| CITY_NOT_FOUND     | Geocoding failed — location not resolved |
| EXTERNAL_API_ERROR | External API failure after retries       |
| INTERNAL_ERROR     | Unexpected server-side error             |

Cache misses are **not** exposed as error codes. They are an internal infrastructure state and must not leak to clients.

### Error Flow Example

```
OpenWeatherMap API timeout
  ↓ (infrastructure catches httpx.TimeoutException, retries exhausted)
WeatherProviderUnavailableError (domain exception)
  ↓ (application maps to error code)
ErrorCode.EXTERNAL_API_ERROR
  ↓ (API formats as JSON, CLI formats as text)
{"error": {"code": "EXTERNAL_API_ERROR", "message": "..."}}
```

### Consequences

**Positive:**

- Consistent error experience across interfaces
- Infrastructure failures never leak to clients
- Testable at each layer independently
- Clear error code taxonomy

**Negative:**

- Requires explicit mapping code at each boundary
- Some duplication in error definitions

### When to Revisit

If error taxonomy becomes unwieldy (>20 error codes) or if interfaces need fundamentally different error formats.

---

# EXTERNAL INTEGRATION DECISIONS

## ADR-005: Single Weather Provider Port

### Status

Accepted

### Context

Weather providers differ in how they accept input:

- Some require city names
- Others require coordinates
- Some may introduce additional constraints

Exposing these differences at the domain level would couple business logic to infrastructure.

### Decision

Define a single domain port:

```python
class WeatherProviderPort:
    async def get_current(location: str): ...
    async def get_forecast(location: str, days: int): ...
```

### Rationale

- The domain operates on **location as text**
- Location is treated as an opaque value by the domain. The domain does not parse, validate, or attempt to interpret this string. It is purely a reference token passed to the infrastructure layer
- Provider requirements (e.g., city ID vs. lat/lon) are implementation details

### Consequences

**Positive:**

- Stable and minimal domain interface
- Easy provider replacement
- Clear separation of concerns

**Negative:**

- Providers may require internal orchestration logic

### When to Revisit

If new providers require fundamentally different interaction models.

---

## ADR-006: Geocoding as a Shared Infrastructure Service

### Status

Accepted

### Context

Some providers require coordinates instead of location names, introducing a geocoding step.

The design question is whether geocoding should be exposed to the domain, duplicated inside each provider, or extracted as a shared infrastructure service.

Three options were considered:

1. **Expose to domain** — Unnecessary complexity; geocoding is not a business concept
2. **Duplicate per provider** — Simple initially, but causes behavioral divergence if multiple providers implement it differently (e.g., one uses exact match, another uses fuzzy search)
3. **Shared infrastructure service** — Encapsulated, reusable, consistent

### Decision

Implement geocoding as a **shared infrastructure service** (`GeocodingService`), injected into provider adapters that require it.

The service is not exposed as a domain port. It remains an infrastructure-only component.

### Consequences

**Positive:**

- Single implementation → consistent behavior across providers
- DRY: no duplication of geocoding logic
- Includes its own cache (7-day TTL) managed in one place
- Easy to update or replace without touching provider logic

**Negative:**

- Requires dependency injection into adapters
- Slightly more wiring at startup

### When to Revisit

If geocoding requirements diverge significantly between providers (e.g., one requires a completely different resolution strategy). In that case, provider-specific geocoding implementations would be acceptable.

---

## ADR-007: Adapter Pattern for Weather Providers

### Status

Accepted

### Context

External APIs must be integrated without coupling them to domain logic.

### Decision

Use adapter implementations of `WeatherProviderPort`.

### Consequences

**Positive:**

- Clear separation of concerns
- Easy mocking in tests
- Extensible to multiple providers

**Negative:**

- Additional abstraction layer

### When to Revisit

If multiple providers require shared abstraction or base classes.

---

## ADR-008: HTTPX over Requests for Async Support

### Status

Accepted

### Context

External API calls must be non-blocking.

### Decision

Use HTTPX as the HTTP client.

### Consequences

**Positive:**

- Native async support
- Connection pooling
- Modern API

**Negative:**

- Additional dependency

### When to Revisit

If alternative protocols (e.g., gRPC) are introduced.

---

## ADR-009: Retry with Exponential Backoff via Tenacity

### Status

Accepted

### Context

External APIs can fail transiently (network timeouts, temporary 5xx errors). Without retry logic, these failures surface directly to users even when a second attempt would succeed.

Options considered:

1. **No retry** — Simple, but poor resilience
2. **Manual retry in each adapter** — Duplicates logic across providers
3. **Centralized retry at HTTP client level** — Single implementation, transparent to all callers

### Decision

Use `tenacity` to apply retry with exponential backoff at the HTTP client level, wrapping all outbound calls uniformly.

Configuration (via settings):

- `RETRY_MAX_ATTEMPTS` (default: 3)
- `RETRY_WAIT_SECONDS` initial wait (default: 1s, doubles each attempt)

Retry applies only to recoverable errors: connection errors, timeouts, and 5xx responses. 4xx errors (e.g., invalid API key, city not found) are not retried.

After retries are exhausted, a domain exception is raised and handled by the layered error strategy (ADR-004).

### Consequences

**Positive:**

- Transparent resilience for all external calls
- No retry logic in provider adapters (SRP)
- Configurable without code changes

**Negative:**

- `tenacity` adds a dependency
- Retry delays can increase response latency in degraded scenarios

### When to Revisit

If circuit breaker patterns become necessary (e.g., to avoid hammering a failing provider).

---

# DATA LAYER DECISIONS

## ADR-010: SQLite instead of PostgreSQL

### Status

Accepted

### Context

The system requires persistence for query history with low expected load.

### Decision

Use SQLite with async support (`aiosqlite`).

### Consequences

**Positive:**

- Zero configuration
- Simple setup
- Ideal for project scale

**Negative:**

- Limited scalability
- Single-writer constraint

### When to Revisit

- High traffic (>1000 users/day)
- Increased write contention

---

## ADR-011: Repository Pattern for Database Access

### Status

Accepted

### Context

Need abstraction between business logic and persistence.

### Decision

Use Repository pattern for database interactions. **The repository interface returns Domain Entities, not SQLAlchemy ORM objects.** This reinforces ADR-012 (Separation of Models) and prevents database implementation details from leaking into the application or domain layers.

### Consequences

**Positive:**

- Decoupled persistence logic
- Easy database replacement
- Testability

**Negative:**

- Additional layer

### When to Revisit

If persistence becomes trivial or tightly coupled to domain.

---

## ADR-012: Separation of Domain and ORM Models

### Status

Accepted

### Context

Validation models and database models serve different purposes.

### Decision

Keep Pydantic (domain) and SQLAlchemy (ORM) models separate.

### Consequences

**Positive:**

- Clear separation of concerns
- Independent evolution

**Negative:**

- Mapping overhead

### When to Revisit

If model duplication becomes excessive.

---

# CACHING STRATEGY DECISIONS

## ADR-013: In-Memory Cache vs External Cache

### Status

Accepted

### Context

Caching is required to reduce API calls and improve performance. The data fetching
pipeline creates two distinct caching opportunities at different architectural layers:

1. **Weather Provider Cache (Domain Layer boundary):** Caches complete weather responses using the domain `location` string as key. This is a system-wide concern, applied via decorator.

2. **Geocoding Cache (Infrastructure Layer):** Caches city→coordinate mappings inside the shared `GeocodingService`. This is an internal optimization invisible to upper layers.

### Decision

Use in-memory caches (Python dictionary with TTL) for both purposes:

- **Weather cache:** 5-minute TTL, managed at the `WeatherProviderPort` boundary
- **Geocoding cache:** 7-day TTL, managed internally by `GeocodingService`

### Critical Distinction

These are **not peer layers** in the architecture:

- The Weather cache is a **decorator** wrapping any `WeatherProviderPort` implementation
- The Geocoding cache is an **internal detail** of the shared `GeocodingService`

This explains why the system is described as having "two-layer caching" in user-facing
documentation, while ADRs treat geocoding as an infrastructure concern.

### Consequences

**Positive:**

- Weather cache provides fast responses for repeated city queries regardless of provider
- Geocoding cache prevents redundant coordinate lookups, centralized in one service
- Both are simple, fast, and require no external dependencies

**Negative:**

- Not shared across instances
- Lost on restart

### When to Revisit

If scaling beyond a single instance or requiring cache persistence.

---

## ADR-014: Cache via Decorator Pattern

### Status

Accepted

### Context

Caching should not be embedded inside provider logic.

### Decision

Apply caching via a decorator wrapping `WeatherProviderPort`.

**Implementation Constraint:** The decorator must be **idempotent with respect to the provider**. The cache key must depend **only on the method arguments** (e.g., `location` string), not on the specific adapter class name or its internal state. This ensures consistency: swapping the underlying adapter implementation results in the same cache key for the same input, preventing cache fragmentation or stale data confusion.

### Consequences

**Positive:**

- Single responsibility for providers
- Composable design
- Clean separation

**Negative:**

- Additional indirection

### When to Revisit

If caching requirements become tightly coupled to provider logic.

---

## ADR-015: Cache Eviction Strategy (FIFO + TTL)

### Status

Accepted

### Context

Cache size must be bounded to prevent memory growth. Leverages Python's guaranteed dict insertion order (since 3.7).

### Decision

Use FIFO eviction combined with TTL expiration.

### Consequences

**Positive:**

- Simple and predictable
- Efficient implementation
- Leverages native dict ordering

**Negative:**

- Not optimal for all access patterns

### When to Revisit

If cache miss rate becomes unacceptable.

---

# CONFIGURATION & OBSERVABILITY DECISIONS

## ADR-016: Pydantic Settings for Configuration Management

### Status

Accepted

### Context

The application requires structured configuration for API keys, cache settings, database connections, and retry parameters.

### Decision

Use Pydantic Settings for configuration management.

### Consequences

**Positive:**

- Type-safe configuration
- Centralized management
- Environment variable support

**Negative:**

- Additional dependency

### When to Revisit

If configuration becomes distributed or requires remote sources.

---

## ADR-017: Standard Library Logging over Structlog

### Status

Accepted

### Context

Logging is required for debugging and observability.

### Decision

Use Python's standard `logging` module.

### Rationale

- Zero additional dependencies
- Sufficient for project scale
- Any Python developer understands it immediately

### Consequences

**Positive:**

- No dependencies
- Simple and familiar
- Works out of the box

**Negative:**

- Limited structured logging capabilities

### When to Revisit

If advanced observability or log aggregation is required.

---

# PRESENTATION LAYER DECISIONS

## ADR-018: Click over Typer for CLI Framework

### Status

Accepted

### Context

The CLI requires a simple interface with a small number of commands.

### Decision

Use Click for CLI implementation.

### Consequences

**Positive:**

- Mature and stable
- No additional dependencies beyond Click itself
- Explicit command definitions

**Negative:**

- More verbose than Typer

### When to Revisit

If CLI complexity grows significantly.

---

# DEPLOYMENT DECISIONS

## ADR-019: No Docker Initially

### Status

Accepted

### Context

The project is intended for portfolio use and easy local execution.

### Decision

Do not include Docker in v1.0.

### Consequences

**Positive:**

- Simpler setup
- Faster development cycle
- Lower barrier for reviewers

**Negative:**

- Less environment consistency
- Harder to scale deployment

### When to Revisit

If deploying to production or multiple environments.

---

## Decision Summary

| ADR     | Category       | Decision                                          |
| ------- | -------------- | ------------------------------------------------- |
| ADR-001 | Architecture   | Ports in domain layer                             |
| ADR-002 | Architecture   | Async everywhere                                  |
| ADR-003 | Validation     | Pydantic v2                                       |
| ADR-004 | Error Handling | Layered error strategy, no internal codes exposed |
| ADR-005 | External       | Single provider port                              |
| ADR-006 | External       | Geocoding as shared infrastructure service        |
| ADR-007 | External       | Adapter pattern                                   |
| ADR-008 | External       | HTTPX                                             |
| ADR-009 | Resilience     | Retry with exponential backoff (tenacity)         |
| ADR-010 | Data           | SQLite                                            |
| ADR-011 | Data           | Repository pattern                                |
| ADR-012 | Data           | Separate domain and ORM models                    |
| ADR-013 | Cache          | In-memory cache                                   |
| ADR-014 | Cache          | Decorator pattern                                 |
| ADR-015 | Cache          | FIFO eviction + TTL                               |
| ADR-016 | Config         | Pydantic settings                                 |
| ADR-017 | Observability  | Standard logging                                  |
| ADR-018 | Presentation   | Click CLI                                         |
| ADR-019 | Deployment     | No Docker (v1.0)                                  |

---

## Quick Reference: Technology Stack

| Layer               | Technology              | Decision Reference    |
| ------------------- | ----------------------- | --------------------- |
| **Language**        | Python 3.12+            | Non-decision          |
| **Package Manager** | `uv`                    | Non-decision          |
| **Linting**         | `ruff`                  | Non-decision          |
| **Type Checking**   | mypy (strict mode)      | Non-decision          |
| **Web Framework**   | FastAPI                 | ADR-002               |
| **Validation**      | Pydantic v2             | ADR-003               |
| **Error Handling**  | Layered exceptions      | ADR-004               |
| **Configuration**   | Pydantic Settings       | ADR-016               |
| **HTTP Client**     | HTTPX                   | ADR-008               |
| **Retry Logic**     | tenacity                | ADR-009               |
| **Database**        | SQLite + aiosqlite      | ADR-010               |
| **ORM**             | SQLAlchemy 2.0+ (async) | ADR-002               |
| **Cache Strategy**  | In-memory dict + TTL    | ADR-013, ADR-015      |
| **Logging**         | Python `logging` module | ADR-017               |
| **CLI Framework**   | Click                   | ADR-018               |
| **Container**       | None (v1.0)             | ADR-019               |

---

## Metrics That Trigger Revisits

| Metric                 | Threshold            | ADRs Affected                      |
| ---------------------- | -------------------- | ---------------------------------- |
| Daily Active Users     | >1000                | ADR-010 (PostgreSQL)               |
| Cache Miss Rate        | >10% due to eviction | ADR-015 (eviction strategy)        |
| Write Contention       | >50 writes/second    | ADR-010 (PostgreSQL)               |
| Memory Usage           | >100MB for cache     | ADR-013 (Redis)                    |
| Concurrent Instances   | >1                   | ADR-013 (Redis), ADR-019           |
| CPU-bound Work         | >50% CPU time        | ADR-002 (reconsider async)         |
| Persistent API Failure | Circuit trips needed | ADR-009 (circuit breaker pattern)  |