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

# SUMMARY

## Summary Table

| ADR     | Category       | Title                            | Decision                           |   |
| ------- | -------------- | -------------------------------- | ---------------------------------- | - |
| ADR-001 | Architecture   | Ports location                   | In domain layer                    | [🔗](#adr-001-ports-interfaces-location-domain-vs-application-layer) |
| ADR-002 | Architecture   | Async strategy                   | Async throughout                   | [🔗](#adr-002-async-strategy-async-throughout-vs-mixed-syncasync) |
| ADR-003 | Validation     | Data validation tool             | Pydantic v2                        | [🔗](#adr-003-data-validation-pydantic-v2) |
| ADR-004 | Error Handling | Error handling strategy          | Layered with explicit mapping      | [🔗](#adr-004-error-handling-strategy-layered-with-mapping) |
| ADR-005 | External       | Weather provider port            | Single port interface              | [🔗](#adr-005-weather-provider-port-single-port-interface) |
| ADR-006 | External       | Geocoding responsibility         | Shared infrastructure service      | [🔗](#adr-006-geocoding-shared-infrastructure-service) |
| ADR-007 | External       | Weather provider implementation  | Adapter pattern                    | [🔗](#adr-007-weather-provider-adapter-pattern) |
| ADR-008 | External       | HTTP client                      | HTTPX (async)                      | [🔗](#adr-008-http-client-httpx-async-vs-requests) |
| ADR-009 | Resilience     | Retry strategy                   | Tenacity with exponential backoff  | [🔗](#adr-009-retry-tenacity-with-exponential-backoff) |
| ADR-010 | Data           | Database                         | SQLite + aiosqlite                 | [🔗](#adr-010-local-persistence-sqlite-vs-postgresql) |
| ADR-011 | Data           | Database access pattern          | Repository pattern                 | [🔗](#adr-011-database-access-repository-pattern) |
| ADR-012 | Data           | Domain vs ORM models             | Separate (Pydantic ≠ SQLAlchemy)   | [🔗](#adr-012-domain-vs-orm-separate-models) |
| ADR-013 | Cache          | Cache type                       | In-memory cache                    | [🔗](#adr-013-cache-type-in-memory-cache-vs-external-cache) |
| ADR-014 | Cache          | Cache application method         | Decorator pattern                  | [🔗](#adr-014-cache-application-decorator-pattern) |
| ADR-015 | Cache          | Cache eviction                   | FIFO + TTL                         | [🔗](#adr-015-cache-eviction-strategy-fifo--ttl) |
| ADR-016 | Config         | Configuration management         | Pydantic settings                  | [🔗](#adr-016-configuration-management-pydantic-settings) |
| ADR-017 | Observability  | Logging                          | Standard library logging           | [🔗](#adr-017-logging-standard-library-logging-vs-structlog) |
| ADR-018 | Presentation   | CLI framework                    | Click                              | [🔗](#adr-018-cli-framework-click-vs-typer) |
| ADR-019 | Deployment     | Containerization                 | No Docker initially                | [🔗](#adr-019-containerization-no-docker-initially) |
| ADR-020 | Testing        | Testing strategy                 | Layered testing approach           | [🔗](#adr-020-testing-strategy-layered-testing-approach) |
| ADR-021 | Resilience     | Rate limiting strategy           | Global quota protection            | [🔗](#adr-021-rate-limiting-strategy-global-quota-protection) |
| ADR-022 | Architecture   | Dependency injection strategy    | Composition root (manual DI)       | [🔗](#adr-022-dependency-injection-strategy-composition-root-manual-di) |
| ADR-023 | Architecture   | Module organization & naming     | Layer-first structure              | [🔗](#adr-023-module-organization--naming-convention) |

---

# FOUNDATIONAL ARCHITECTURE DECISIONS

## ADR-001: Ports (Interfaces) Location: Domain vs Application Layer

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

## ADR-002: Async Strategy: Async throughout vs Mixed Sync/Async

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

## ADR-003: Data validation: Pydantic v2

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

## ADR-004: Error Handling Strategy: Layered with mapping

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

## ADR-005: Weather Provider Port: Single Port Interface

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

## ADR-006: Geocoding: Shared Infrastructure Service

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

## ADR-007: Weather Provider: Adapter Pattern

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

## ADR-008: HTTP Client: HTTPX (async) vs Requests

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

## ADR-009: Retry: Tenacity with Exponential Backoff

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

After retries are exhausted, a domain exception is raised and handled by the layered error strategy (see [ADR-004](#adr-004-error-handling-strategy-layered-with-mapping)).

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

## ADR-010: Local Persistence: SQLite vs PostgreSQL

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

## ADR-011: Database Access: Repository Pattern

### Status

Accepted

### Context

Need abstraction between business logic and persistence.

### Decision

Use Repository pattern for database interactions. **The repository interface returns Domain Entities, not SQLAlchemy ORM objects.** This reinforces separation of models (see [ADR-012](#adr-012-domain-vs-orm-separate-models)) and prevents database implementation details from leaking into the application or domain layers.

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

## ADR-012: Domain vs ORM: Separate Models

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

## ADR-013: Cache Type: In-Memory Cache vs External Cache

### Status

Accepted

### Context

Caching is required to reduce API calls and improve performance. The data fetching pipeline creates two distinct caching opportunities at different architectural layers:

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

This explains why the system is described as having "two-layer caching" in user-facing documentation, while ADRs treat geocoding as an infrastructure concern.

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

## ADR-014: Cache Application: Decorator Pattern

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

## ADR-015: Cache Eviction Strategy: FIFO + TTL

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

## ADR-016: Configuration Management: Pydantic Settings

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

## ADR-017: Logging: Standard Library Logging vs Structlog

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

## ADR-018: CLI Framework: Click vs Typer

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

## ADR-019: Containerization: No Docker Initially

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

# LATER DECISIONS

## ADR-020: Testing Strategy: Layered Testing Approach

### Status

Accepted

### Context

The system spans multiple architectural layers (Presentation, Application, Domain, Infrastructure) and integrates with external systems (OpenWeatherMap API, SQLite database).

A testing strategy must:

- Ensure correctness across layers
- Preserve domain independence from infrastructure
- Provide fast feedback during development
- Avoid reliance on external systems (network, API limits)

Naive approaches (full end-to-end testing or excessive mocking) introduce trade-offs:

- **E2E-heavy:** Slow, fragile, dependent on external APIs
- **Mock-heavy:** Unrealistic, brittle, low confidence

### Decision

Adopt a **layered testing strategy** strictly aligned with the system architecture (Clean Architecture / Ports & Adapters), combining unit, integration, and end-to-end tests:

#### 1. Domain Layer

- **Type:** Pure Unit Tests
- **Dependencies:** None (no mocks, no I/O)
- **Validation:** Business rules, value objects, and domain invariants

#### 2. Application Layer

- **Type:** Solitary Unit Tests
- **Dependencies:** **Fakes** for stateful ports (e.g., `FakeHistoryRepository`), **Mocks** for stateless ports (e.g., `WeatherProviderPort`)
- **Validation:** Orchestration logic, use case workflows, and error mapping from domain exceptions to application errors

#### 3. Infrastructure Layer

- **Type:** Sociable Integration Tests (Component Tests)
- **Constraint:** These tests validate adapters against the **contract of the HTTPX client**, not the OpenWeatherMap API itself

**HTTP Integration (`pytest-httpx`):**

- Intercept all outbound HTTP calls
- Validate:
    - Request URL and query parameter construction
    - JSON response parsing
    - **Retry behavior (Tenacity):** Simulate `HTTP_500` or `TimeoutException` to verify exponential backoff is triggered
    - Translation of HTTP errors to Domain Exceptions

**Persistence Integration (`aiosqlite`):**

- Use SQLite **in-memory** database (`sqlite+aiosqlite:///:memory:`)
- Test the real `Repository` implementation against a real SQL engine without file I/O

#### 4. Presentation Layer

- **API:** `FastAPI TestClient` with dependency overrides (injecting Application Layer Fakes/Mocks)
- **CLI:** Subprocess execution or `CliRunner` with dependency overrides
- **Validation:** Input parsing, HTTP status codes, JSON response structure, and CLI exit codes

#### 5. Smoke Tests (CI Gate)

- Validate application bootstrapping (Dependency Injection wiring)
- Ensure `uv run weather --help` and `GET /` return successfully without crashing

### Testing Principles

- **Boundary Mocking:** Mocks/Fakes are applied **only at architectural boundaries (domain ports)**
- **No Internal Mocking:** Core domain and application logic is **never mocked**
- **Zero External Calls:** The test suite makes zero network calls to `api.openweathermap.org`
- **Determinism:** Tests are fast and repeatable regardless of network conditions

### Consequences

**Positive:**

- **Fast Feedback:** The entire suite runs in seconds, enabling rapid TDD
- **High Confidence:** Validates both business logic (Unit) and integration wiring (Component)
- **Verifiable Resilience:** Allows testing of retry logic (Tenacity) and cache TTLs without waiting
- **Clean Architecture Validation:** The test suite proves the Domain layer has no dependency on external frameworks

**Negative:**

- **Discipline Required:** Developers must consciously decide which test layer is appropriate for new code
- **Fixture Maintenance:** Requires maintaining realistic JSON fixtures (`pytest-httpx`) for OpenWeatherMap responses
- **Complexity:** Multiple test types increase initial cognitive load

### Testing Performance Expectations (Non-Normative Guidance)

The following metrics serve as design targets, not strict failure criteria:

| Layer                    | Scope                              | Expected Execution Time (Target) |
| ------------------------ | ---------------------------------- | -------------------------------- |
| **Domain / Application** | Solitary Unit Tests                | **< 10 seconds**                 |
| **Infrastructure**       | Sociable Component Tests (DB/HTTP) | **< 15 seconds**                 |
| **Full Suite**           | All tests (Unit + Integration)     | **< 25 seconds**                 |

*Note: These targets assume local execution on standard development hardware. CI runners may exhibit slight variance due to resource constraints.*

### When to Revisit

This ADR should be re-evaluated if the test suite exhibits signs of architectural decay rather than simply growing in size. Triggers for revisiting include:

- **Degraded Developer Experience:** Core unit and application layer tests **exceed 10 seconds**. This indicates accidental I/O or heavy mocking overhead that breaks the fast feedback loop required for TDD
- **Systemic Slowness:** The full integration suite **exceeds 25 seconds**. This threshold signals that infrastructure setup/teardown has become a bottleneck (e.g., database migrations running per-test instead of per-session)
- **Flakiness:** Introduction of "flaky" tests (tests that fail randomly without code changes), often caused by shared async state or improper `freezegun` usage with retry logic
- **False Confidence:** Bugs repeatedly slipping through to production/staging that indicate the `pytest-httpx` fixtures have drifted from the real OpenWeatherMap API contract

---

## ADR-021: Rate Limiting Strategy: Global Quota Protection

### Status

Accepted

### Context

The system depends on the **OpenWeatherMap Free Tier**, which imposes a hard limit of:

- 60 API calls per minute

Exceeding this limit results in failed requests (HTTP 429) and potential API key suspension.

Given the project constraints:

- Expected load: **<100 requests/day**
- No multi-instance deployment
- No user-level authentication

A rate limiting strategy is required to **protect the external dependency**, not to enforce fairness between users.

### Decision

Implement a **Global Quota Protection (Fail Fast)** strategy at the **Infrastructure Layer**.

- **Location:** `HttpClientManager`
- **Mechanism:** In-memory fixed window counter
- **Limit:** **55 requests/minute** (safety margin)
- **Behavior:**
  - If limit is exceeded → **do not perform HTTP call**
  - Raise domain exception: `ProviderQuotaExceededError`
  - No queuing, no sleeping

### Rationale

- **Protects external dependency** from accidental overuse
- **Encapsulates provider constraints** within Infrastructure (aligned with ADR-001)
- **Avoids unnecessary complexity** (no Redis, no token bucket)
- **Integrates cleanly with error strategy** (see ADR-004)

### Consequences

**Positive:**

- Prevents API key throttling or bans
- Extremely simple implementation (~10–15 LOC)
- Zero operational overhead
- Fully transparent to Domain and Application layers

**Negative:**

- **Burst sensitivity:** Short spikes can exhaust quota early in the window
- **Fail-fast UX:** Users receive immediate errors instead of delayed responses
- **Single-instance only:** Not safe for multi-worker deployments

### When to Revisit

- Running multiple instances or workers
- Sustained traffic approaching provider limits
- Need for user-level fairness or prioritization

---

## ADR-022: Dependency Injection Strategy: Composition Root (Manual DI)

### Status

Accepted

### Context

The system requires dependency injection to:

- Enforce **dependency inversion** (ADR-001)
- Enable **testability** via mocks/fakes (ADR-020)
- Allow **infrastructure substitution** (providers, repositories)

Available approaches:

1. Framework-driven DI (FastAPI `Depends`)
2. External DI containers (`dependency-injector`, `punq`)
3. Manual DI (pure Python)

### Decision

Use **Manual Dependency Injection via a Composition Root**.

No external DI framework will be introduced.

### Implementation Approach

#### 1. Composition Root

- Located in:
  - `main.py` (FastAPI entrypoint)
  - CLI bootstrap module
- Responsible for building the **entire object graph**

**Construction order:**

```
Infrastructure → Decorators → Application Services → Presentation wiring
```

#### 2. Injection Pattern

- **Constructor Injection only**
- No service locators
- No global singletons

#### 3. FastAPI Integration

- FastAPI `Depends` is used **only as a retrieval mechanism**
- Dependencies are retrieved from a pre-built container (`AppState`)

**Constraint:**

- `Depends` must NOT:
  - Instantiate objects
  - Contain business logic
  - Perform I/O

### Rationale

- Aligns with Clean Architecture (explicit boundaries)
- Keeps dependency graph **fully explicit and inspectable**
- Avoids framework lock-in
- Keeps complexity proportional to project size (YAGNI)

### Consequences

**Positive:**

- Full control over object lifecycle
- No hidden magic or runtime indirection
- Excellent testability (direct constructor injection)
- Debuggable and predictable

**Negative:**

- Manual wiring required when adding dependencies
- Composition root can grow over time

### When to Revisit

- Dependency graph grows beyond ~20–30 services
- Need for runtime/dynamic wiring based on configuration
- Introduction of scoped lifetimes (e.g., request-scoped DB sessions)

---

## ADR-023: Module Organization & Naming Convention

### Status

Accepted

### Context

The project follows Clean Architecture with strict separation between:

- Domain
- Application
- Infrastructure
- Presentation

Without enforced structure:

- Boundaries are easily violated
- Imports become inconsistent
- Codebase becomes harder to navigate and reason about

### Decision

Adopt a **layer-first module organization** using Python **regular packages**, strictly mirroring architectural boundaries.

### Directory Structure

```
weather-analytics-dashboard/
├── src/
│   └── weather_analytics_dashboard/
│       ├── __init__.py
│       ├── main.py                 # FastAPI app creation & Composition Root
│       │
│       ├── presentation/           # Layer: Interface Adapters
│       │   ├── __init__.py
│       │   ├── api/
│       │   │   ├── __init__.py
│       │   │   ├── routes/         # Grouped by feature (weather.py, health.py)
│       │   │   └── dependencies.py # FastAPI Depends retrieval logic
│       │   └── cli/
│       │       ├── __init__.py
│       │       └── commands/       # Grouped by feature
│       │
│       ├── application/            # Layer: Use Cases
│       │   ├── __init__.py
│       │   └── services/           # Orchestration logic
│       │
│       ├── domain/                 # Layer: Enterprise Business Rules
│       │   ├── __init__.py
│       │   ├── models.py           # Pydantic entities & value objects
│       │   ├── ports.py            # Abstract interfaces (WeatherProviderPort, etc.)
│       │   └── exceptions.py       # Domain-specific errors
│       │
│       ├── infrastructure/         # Layer: Frameworks & Drivers
│       │   ├── __init__.py
│       │   ├── weather_providers/  # Adapters (openweather_adapter.py)
│       │   ├── geocoding/          # Shared service
│       │   ├── cache/              # Cached provider decorator & TTL store
│       │   ├── persistence/        # SQLAlchemy models & Repository impl
│       │   └── http/               # HTTPX client manager & retry logic
│       │
│       └── config/                 # Cross-cutting concern
│           ├── __init__.py
│           └── settings.py         # Pydantic Settings
│
├── tests/                          # Mirrors src/ structure
│   ├── unit/
│   ├── integration/
│   └── conftest.py
│
├── docs/                           # ADRs, Scope, Architecture
├── pyproject.toml
└── .env.example
```

### Naming Conventions

| Scope          | Convention                 | Example                    |
| -------------- | -------------------------- | -------------------------- |
| Files/Modules  | `snake_case`               | `weather_service.py`       |
| Classes        | `PascalCase`               | `OpenWeatherAdapter`       |
| Domain Ports   | `*Port`                    | `WeatherProviderPort`      |
| Infrastructure | `*Adapter` / `*Repository` | `SqliteHistoryRepository`  |
| Application    | `*Service`                 | `GetCurrentWeatherService` |

### Architectural Constraints

Strict dependency rules:

| From → To      | Allowed                |
| -------------- | ---------------------- |
| Domain         | ❌ none                |
| Application    | ✅ Domain              |
| Infrastructure | ✅ Domain              |
| Presentation   | ✅ Application, Domain |

**Explicitly forbidden:**

- Domain → anything
- Application → Infrastructure
- Infrastructure → Application
- Presentation → Infrastructure

### Test Structure Alignment

The `tests/` directory mirrors `src/`:

- `tests/unit/` → Domain & Application
- `tests/integration/` → Infrastructure & Presentation

This reinforces the testing strategy defined in ADR-020.

### Consequences

**Positive:**

- Strong architectural clarity
- Easier onboarding and navigation
- Prevents accidental coupling between layers
- Aligns directly with testing strategy

**Negative:**

- Longer import paths
- Requires discipline to maintain boundaries

### When to Revisit

- If modules exceed ~15–20 files → consider feature-based grouping
- If extracting services into separate deployables (microservices)

---

# QUICK REFERENCE

## Technology Stack

| Layer               | Technology              | Decision Reference |
| ------------------- | ----------------------- | ------------------ |
| **Language**        | Python 3.12+            | Non-decision       |
| **Package Manager** | `uv`                    | Non-decision       |
| **Linting**         | `ruff`                  | Non-decision       |
| **Type Checking**   | mypy (strict mode)      | Non-decision       |
| **Web Framework**   | FastAPI                 | [ADR-002](#adr-002-async-strategy-async-throughout-vs-mixed-syncasync) |
| **Validation**      | Pydantic v2             | [ADR-003](#adr-003-data-validation-pydantic-v2) |
| **Error Handling**  | Layered exceptions      | [ADR-004](#adr-004-error-handling-strategy-layered-with-mapping) |
| **Configuration**   | Pydantic Settings       | [ADR-016](#adr-016-configuration-management-pydantic-settings) |
| **HTTP Client**     | HTTPX                   | [ADR-008](#adr-008-http-client-httpx-async-vs-requests) |
| **Retry Logic**     | tenacity                | [ADR-009](#adr-009-retry-tenacity-with-exponential-backoff) |
| **Database**        | SQLite + aiosqlite      | [ADR-010](#adr-010-local-persistence-sqlite-vs-postgresql) |
| **ORM**             | SQLAlchemy 2.0+ (async) | [ADR-002](#adr-002-async-strategy-async-throughout-vs-mixed-syncasync) |
| **Cache Strategy**  | In-memory dict + TTL    | [ADR-013](#adr-013-cache-type-in-memory-cache-vs-external-cache), [ADR-015](#adr-015-cache-eviction-strategy-fifo--ttl) |
| **Logging**         | Python `logging` module | [ADR-017](#adr-017-logging-standard-library-logging-vs-structlog) |
| **CLI Framework**   | Click                   | [ADR-018](#adr-018-cli-framework-click-vs-typer) |
| **Testing**         | pytest ecosystem        | [ADR-020](#adr-020-testing-strategy-layered-testing-approach) |
| **Container**       | None (v1.0)             | [ADR-019](#adr-019-containerization-no-docker-initially) |

---

## Metrics That Trigger Revisits

| Metric                 | Threshold            | ADRs Affected |
| ---------------------- | -------------------- | ------------- |
| Daily Active Users     | >1000                | [ADR-010](#adr-010-local-persistence-sqlite-vs-postgresql) (PostgreSQL) |
| Cache Miss Rate        | >10% due to eviction | [ADR-015](#adr-015-cache-eviction-strategy-fifo--ttl) (eviction strategy) |
| Write Contention       | >50 writes/second    | [ADR-010](#adr-010-local-persistence-sqlite-vs-postgresql) (PostgreSQL) |
| Memory Usage           | >100MB for cache     | [ADR-013](#adr-013-cache-type-in-memory-cache-vs-external-cache) (Redis) |
| Concurrent Instances   | >1                   | [ADR-013](#adr-013-cache-type-in-memory-cache-vs-external-cache) (Redis), [ADR-019](#adr-019-containerization-no-docker-initially) (Docker) |
| CPU-bound Work         | >50% CPU time        | [ADR-002](#adr-002-async-strategy-async-throughout-vs-mixed-syncasync) (reconsider async) |
| Persistent API Failure | >3 failures/minute   | [ADR-009](#adr-009-retry-tenacity-with-exponential-backoff) (circuit breaker pattern) |
| Test Suite Duration    | >25 seconds          | [ADR-020](#adr-020-testing-strategy-layered-testing-pyramid) (optimize tests) |
| Dependency Graph Size  | >25 services         | [ADR-022](#adr-022-dependency-injection-strategy-composition-root-manual-di) (consider DI container) |
| Module Size            | >20 files/module     | [ADR-023](#adr-023-module-organization--naming-convention) (restructure by feature) |

---

# CHANGELOG

| Date       | ADR     | Decision                                          | Change     |   |
| ---------- | ------- | ------------------------------------------------- | ---------- | - |
| 2026-04-09 | ADR-001 | Ports in domain layer                             | Accepted   | [🔗](#adr-001-ports-interfaces-location-domain-vs-application-layer) |
| 2026-04-09 | ADR-002 | Async everywhere                                  | Accepted   | [🔗](#adr-002-async-strategy-async-throughout-vs-mixed-syncasync) |
| 2026-04-09 | ADR-003 | Pydantic v2 for data validation                   | Accepted   | [🔗](#adr-003-data-validation-pydantic-v2) |
| 2026-04-09 | ADR-004 | Layered error strategy, no internal codes exposed | Accepted   | [🔗](#adr-004-error-handling-strategy-layered-with-mapping) |
| 2026-04-09 | ADR-005 | Single provider port                              | Accepted   | [🔗](#adr-005-weather-provider-port-single-port-interface) |
| 2026-04-09 | ADR-006 | Geocoding as shared infrastructure service        | Accepted   | [🔗](#adr-006-geocoding-shared-infrastructure-service) |
| 2026-04-09 | ADR-007 | Adapter pattern                                   | Accepted   | [🔗](#adr-007-weather-provider-adapter-pattern) |
| 2026-04-09 | ADR-008 | HTTPX                                             | Accepted   | [🔗](#adr-008-http-client-httpx-async-vs-requests) |
| 2026-04-09 | ADR-009 | Retry with exponential backoff (tenacity)         | Accepted   | [🔗](#adr-009-retry-tenacity-with-exponential-backoff) |
| 2026-04-09 | ADR-010 | SQLite                                            | Accepted   | [🔗](#adr-010-local-persistence-sqlite-vs-postgresql) |
| 2026-04-09 | ADR-011 | Repository pattern                                | Accepted   | [🔗](#adr-011-database-access-repository-pattern) |
| 2026-04-09 | ADR-012 | Separate domain and ORM models                    | Accepted   | [🔗](#adr-012-domain-vs-orm-separate-models) |
| 2026-04-09 | ADR-013 | In-memory cache                                   | Accepted   | [🔗](#adr-013-cache-type-in-memory-cache-vs-external-cache) |
| 2026-04-09 | ADR-014 | Decorator pattern                                 | Accepted   | [🔗](#adr-014-cache-application-decorator-pattern) |
| 2026-04-09 | ADR-015 | FIFO eviction + TTL                               | Accepted   | [🔗](#adr-015-cache-eviction-strategy-fifo--ttl) |
| 2026-04-09 | ADR-016 | Pydantic settings                                 | Accepted   | [🔗](#adr-016-configuration-management-pydantic-settings) |
| 2026-04-09 | ADR-017 | Standard logging                                  | Accepted   | [🔗](#adr-017-logging-standard-library-logging-vs-structlog) |
| 2026-04-09 | ADR-018 | Click CLI                                         | Accepted   | [🔗](#adr-018-cli-framework-click-vs-typer) |
| 2026-04-09 | ADR-019 | No Docker Initially                               | Accepted   | [🔗](#adr-019-containerization-no-docker-initially) |
| 2026-04-12 | ADR-020 | Layered testing approach                          | Accepted   | [🔗](#adr-020-testing-strategy-layered-testing-approach) |
| 2026-04-12 | ADR-021 | Global quota protection                           | Accepted   | [🔗](#adr-021-rate-limiting-strategy-global-quota-protection) |
| 2026-04-12 | ADR-022 | Composition root (manual DI)                      | Accepted   | [🔗](#adr-022-dependency-injection-strategy-composition-root-manual-di) |
| 2026-04-12 | ADR-023 | Layer-first module organization                  | Accepted   | [🔗](#adr-023-module-organization--naming-convention) |