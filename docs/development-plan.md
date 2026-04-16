# Development Plan - Weather Analytics Dashboard

This document outlines the complete development roadmap including branches, commits and version milestones.

## Version Milestones (Make it work, make it right, make it fast)

| Version | Feature                                              |
| :-----: | ---------------------------------------------------- |
| 0.1.0   | `/health` endpoint working                           |
| 0.2.0   | `/current` endpoint working                          |
| 0.3.0   | `/forecast` endpoint working                         |
| 0.4.0   | `/history` endpoint working (all endpoints complete) |
| 0.5.0   | Retry working                                        |
| 0.6.0   | Caching working                                      |
| 1.0.0   | Project finalized                                    |

---

## Quick Reference

| Branch Prefix | Commit Type | Purpose                                                    |
| ------------- | ----------- | ---------------------------------------------------------- |
| `docs/*`      | `docs:`     | Documentation (ADRs, README, architecture, planning)       |
| `build/*`     | `build:`    | Build tooling (Makefile)                                   |
| `ci/*`        | `ci:`       | CI configuration files and scripts (GitHub Actions)        |
| `chore/*`     | `chore:`    | Settings, maintenance, configuration, dependencies         |
| `test/*`      | `test:`     | Tests (fixtures, smoke tests, unit, integration)           |
| `feat/*`      | `feat:`     | Features (endpoints, CLI commands, caching, retry)         |
| `fix/*`       | `fix:`      | Bugs fixes                                                 |
| `perf/*`      | `perf:`     | Code that improves performance                             |
| `refactor/*`  | `refactor:` | Code changes that neither fix bugs nor add features        |
| `style/*`     | `style:`    | Changes that do not affect the meaning of the code         |

### Commit Message Convention (Conventional Commits)

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Merge Message Convention

```bash
git merge --no-ff <branch> -m "<type>: merge <description> into <branch>"
```

### Branch Cleanup

After merging each branch, delete it both locally and remotely:

```bash
git branch -d <branch-name>
git push origin --delete <branch-name>
```

---

## Phase 0: Project Initiation

**Branch:** `main` 

```bash
git init
git add README.md LICENSE
git commit -m "first commit"
git push -u origin main
git switch -c develop
```

---

## Phase 1: Project Planning & Documentation
	
**Branch:** `docs/project-foundation`

| Commit | Message                                          |
| :----: | ------------------------------------------------ |
| 1      | `docs: add project scope and requirements`       |
| 2      | `docs: define architecture and layer boundaries` |
| 3      | `docs: record architecture decisions (ADRs)`     |
| 4      | `docs: create README with project vision`        |

**Merge to develop:**
```bash
git merge --no-ff docs/project-foundation -m "docs: merge project foundation documentation into develop"
```

---
	
## Phase 2: Initial Project Setup

**Branch:** `chore/1-initial-setup`

| Commit | Message                                                                  |
| :----: | ------------------------------------------------------------------------ |
| 1      | `chore: add .gitignore, configure uv, dependencies and project skeleton` |

**Merge to develop:**
```bash
git merge --no-ff chore/1-initial-setup -m "chore: merge project initial setup into develop"
```

---
	
## Phase 3: Entrypoint Verification

**Branch:** `chore/2-entrypoint-verification`

| Commit | Message                                                  |
| :----: | -------------------------------------------------------- |
| 1      | `chore(cli): add minimal Click CLI group entrypoint`     |
| 2      | `chore(api): add minimal FastAPI entrypoint with / root` |

**Merge to develop:**
```bash
git merge --no-ff chore/2-entrypoint-verification -m "chore: merge minimal entrypoint verification into develop"
```

**Branch:** `test/smoke-tests`

| Commit | Message                                                                               |
| :----: | ------------------------------------------------------------------------------------- |
| 1      | `test(smoke): add automated smoke tests for CLI and API entrypoints with CI workflow` |

**Merge to develop:**
```bash
git merge --no-ff test/smoke-tests -m "test: merge smoke tests for entrypoint verification with CI workflow into develop"
```

---
	
## Phase 4: Missing ADRs

**Branch:** `docs/add-missing-adrs`

| Commit | Message                                           |
| :----: | ------------------------------------------------- |
| 1      | `docs(adr): add ADR-020 - testing strategy`       |
| 2      | `docs(adr): add ADR-021 - rate limiting strategy` |
| 3      | `docs(adr): add ADR-022 - DI strategy`            |
| 4      | `docs(adr): add ADR-023 - organization & naming`  |

**Merge to develop:**
```bash
git merge --no-ff docs/add-missing-adrs -m "docs(adr): merge ADRs for testing, rate limit, DI and conventions into develop"
```

| Commit | Message                                                             |
| :----: | ------------------------------------------------------------------- |
| 1      | `refactor(test): reorganize smoke tests into integration/bootstrap` |
| 2      | `test: add unit test placeholder`                                   |

---

## Phase 5: Development Process Planning

**Branch:** `docs/development-roadmap`

| Commit | Message                                 |
| :----: | --------------------------------------- |
| 1      | `docs: add development plan`            |
| 2      | `docs(readme): add development roadmap` |

**Merge to develop:**
```bash
git merge --no-ff docs/development-roadmap -m "docs: merge development plan and roadmap into develop"
```

---

## Phase 6: Automation - Makefile & PR Template

**Branch:** `build/makefile`

| Commit | Message                                 |
| :----: | --------------------------------------- |
| 1      | `build: add Makefile with common tasks` |

**Merge to develop:**
```bash
git merge --no-ff build/makefile -m "build: merge Makefile into develop"
```

**Branch:** `docs/pr-template`

| Commit | Message                           |
| :----: | --------------------------------- |
| 1      | `docs: add pull request template` |

**Merge to develop:**
```bash
git merge --no-ff docs/pr-template -m "docs: merge PR template into develop"
```

---
	
## Phase 7: Configuration Settings

**Branch:** `chore/3-config-settings`

| Commit | Message                                                      |
| :----: | ------------------------------------------------------------ |
| 1      | `test(config): add settings loading tests`                   |
| 2      | `feat(config): add base pydantic settings configuration`     |
| 3      | `feat(config): add settings cache and logging configuration` |
| 4      | `test(config): add config and logging integration tests`     |
| 5      | `chore(api): use settings in FastAPI app initialization`     |

**Merge to develop:**
```bash
git merge --no-ff chore/3-config-settings -m "chore: merge base configuration system with pydantic settings into develop"
```
```bash
git commit -m "ci: add CI workflows (bootstrap, test suite, code quality)"
```

---
	
## Phase 8: `/health` Endpoint

**Branch:** `feat/1-health-endpoint`

| Commit | Message                                                   |
| :----: | --------------------------------------------------------- |
| 1      | `test(api): add failing test for GET /health endpoint`    |
| 2      | `feat(api): implement GET /health endpoint`               |
| 3      | `refactor(api): clean health endpoint response structure` |

**Merge to develop:**
```bash
git merge --no-ff feat/1-health-endpoint -m "feat: add health endpoint (vertical slice)"
```

**Bump version in pyproject.toml**
```bash
git commit -m "chore(release): bump version to 0.1.0"
```

**Merge to main:**
```bash
git merge --no-ff develop -m "chore(release): merge develop into main for v0.1.0"
git tag -a "v0.1.0" -m "feat: release v0.1.0 - health endpoint working"
```

---
	
## Phase 9: `/current` Endpoint

### Subphase 9.1 - Domain & Application Layer

**Branch:** `feat/2-weather-current-domain-application`

| Commit | Message                                                                |
| :----: | ---------------------------------------------------------------------- |
| 1      | `test(application): add failing test for get current weather use case` |
| 2      | `feat(domain): add weather domain models and exceptions`               |
| 3      | `feat(application): implement current weather service`                 |

**Merge to develop:**
```bash
git merge --no-ff feat/2-weather-current-domain-application -m "feat: merge current weather domain and application layer into develop"
```

### Subphase 9.2 - API Endpoint

**Branch:** `feat/2-weather-current-api`

| Commit | Message                                                         |
| :----: | --------------------------------------------------------------- |
| 1      | `test(api): add failing test for GET /weather/current endpoint` |
| 2      | `feat(api): implement GET /weather/current endpoint`            |
| 3      | `chore(api): wire dependencies for weather current flow`        |

**Merge to develop:**
```bash
git merge --no-ff feat/2-weather-current-api -m "feat: merge current weather API endpoint into develop"
```

### Subphase 9.3 - Infrastructure Layer

**Branch:** `feat/2-weather-current-infra`

| Commit | Message                                                    |
| :----: | ---------------------------------------------------------- |
| 1      | `test(infra): add failing test for openweather adapter`    |
| 2      | `feat(infra): implement openweather adapter`               |
| 3      | `chore(infra): wire dependencies for weather current flow` |

**Merge to develop:**
```bash
git merge --no-ff feat/2-weather-current-infra -m "feat: merge OpenWeather adapter for current weather into develop"
```

### Subphase 9.4 - CLI Command

**Branch:** `feat/2-weather-current-cli`

| Commit | Message                                                             |
| :----: | ------------------------------------------------------------------- |
| 1      | `test(cli): add failing test for 'weather now <city>'`              |
| 2      | `feat(cli): implement weather now command`                          |
| 3      | `refactor: improve boundaries and naming for weather current slice` |

**Merge to develop:**
```bash
git merge --no-ff feat/2-weather-current-cli -m "feat: merge CLI command for current weather into develop"
```

**Bump version in pyproject.toml**
```bash
git commit -m "chore(release): bump version to 0.2.0"
```

**Merge to main:**
```bash
git merge --no-ff develop -m "chore(release): merge develop into main for v0.2.0"
git tag -a "v0.2.0" -m "feat: release v0.2.0 - current weather endpoint working"
```

---

## Phase 10: `/forecast` Endpoint

### Subphase 10.1 - Domain & Application Layer

**Branch:** `feat/3-weather-forecast-domain-application`

| Commit | Message                                          |
| :----: | ------------------------------------------------ |
| 1      | `test(application): add forecast use case tests` |
| 2      | `feat(application): implement forecast service`  |

**Merge to develop:**
```bash
git merge --no-ff feat/3-weather-forecast-domain-application -m "feat: merge forecast domain and application layer into develop"
```

### Subphase 10.2 - API Endpoint

**Branch:** `feat/3-weather-forecast-api`

| Commit | Message                                           |
| :----: | ------------------------------------------------- |
| 1      | `test(api): add forecast endpoint tests`          |
| 2      | `feat(api): implement GET /weather/forecast`      |
| 3      | `chore(api): wire dependencies for forecast flow` |

**Merge to develop:**
```bash
git merge --no-ff feat/3-weather-forecast-api -m "feat: merge forecast API endpoint into develop"
```

### Subphase 10.3 - CLI Command

**Branch:** `feat/3-weather-forecast-cli`

| Commit | Message                                              |
| :----: | ---------------------------------------------------- |
| 1      | `test(cli): add forecast command tests`              |
| 2      | `feat(cli): implement weather forecast command`      |
| 3      | `chore(cli): wire dependencies for forecast command` |

**Merge to develop:**
```bash
git merge --no-ff feat/3-weather-forecast-cli -m "feat: merge forecast CLI command into develop"
```

### Subphase 10.4 - Infrastructure Layer

**Branch:** `feat/3-weather-forecast-infra`

| Commit | Message                                              |
| :----: | ---------------------------------------------------- |
| 1      | `feat(infra): extend provider with forecast support` |
| 2      | `chore(infra): wire forecast provider dependencies`  |

**Merge to develop:**
```bash
git merge --no-ff feat/3-weather-forecast-infra -m "feat: merge OpenWeather forecast support into develop"
```

**Bump version in pyproject.toml**
```bash
git commit -m "chore(release): bump version to 0.3.0"
```

**Merge to main:**
```bash
git merge --no-ff develop -m "chore(release): merge develop into main for v0.3.0"
git tag -a "v0.3.0" -m "feat: release v0.3.0 - forecast endpoint working"
```

---

## Phase 11: `/history` Endpoint

### Subphase 11.1 - Domain Contracts

**Branch:** `feat/4-weather-history-domain-contracts`

| Commit | Message                                                            |
| :----: | ------------------------------------------------------------------ |
| 1      | `test(domain): define history repository contract tests`           |
| 2      | `feat(domain): add history domain models and repository interface` |

**Merge to develop:**
```bash
git merge --no-ff feat/4-weather-history-domain-contracts -m "feat: merge history domain contracts into develop"
```

### Subphase 11.2 - Infrastructure Layer

**Branch:** `feat/4-weather-history-infra`

| Commit | Message                                             |
| :----: | --------------------------------------------------- |
| 1      | `test(infra): add sqlite history repository tests`  |
| 2      | `feat(infra): implement sqlite history repository`  |
| 3      | `chore(infra): wire sqlite repository dependencies` |

**Merge to develop:**
```bash
git merge --no-ff feat/4-weather-history-infra -m "feat: merge SQLite history repository into develop"
```

### Subphase 11.3 - Application Layer

**Branch:** `feat/4-weather-history-application`

| Commit | Message                                                  |
| :----: | -------------------------------------------------------- |
| 1      | `test(application): add history service tests`           |
| 2      | `feat(application): implement history retrieval service` |
| 3      | `chore(application): wire history service dependencies`  |

**Merge to develop:**
```bash
git merge --no-ff feat/4-weather-history-application -m "feat: merge history application service into develop"
```

### Subphase 11.4 - API Endpoint

**Branch:** `feat/4-weather-history-api`

| Commit | Message                                          |
| :----: | ------------------------------------------------ |
| 1      | `test(api): add history endpoint tests`          |
| 2      | `feat(api): implement GET /weather/history`      |
| 3      | `chore(api): wire history endpoint dependencies` |

**Merge to develop:**
```bash
git merge --no-ff feat/4-weather-history-api -m "feat: merge history API endpoint into develop"
```

### Subphase 11.5 - CLI Command

**Branch:** `feat/4-weather-history-cli`

| Commit | Message                                         |
| :----: | ----------------------------------------------- |
| 1      | `test(cli): add history command tests`          |
| 2      | `feat(cli): implement weather history command`  |
| 3      | `chore(cli): wire history command dependencies` |

**Merge to develop:**
```bash
git merge --no-ff feat/4-weather-history-cli -m "feat: merge history CLI command into develop"
```

**Bump version in pyproject.toml**
```bash
git commit -m "chore(release): bump version to 0.4.0"
```

**Merge to main:**
```bash
git merge --no-ff develop -m "chore(release): merge develop into main for v0.4.0"
git tag -a "v0.4.0" -m "feat: release v0.4.0 - history endpoint working (all endpoints complete)"
```

---

## Phase 12: Retry Logic

**Branch:** `feat/5-retry-http`

| Commit | Message                                                    |
| :----: | ---------------------------------------------------------- |
| 1      | `test(infra): add retry behavior tests`                    |
| 2      | `feat(infra): implement http client with retry (tenacity)` |
| 3      | `chore(infra): wire retry http client into provider`       |

**Merge to develop:**
```bash
git merge --no-ff feat/5-retry-http -m "feat: merge retry http client into develop"
```

**Bump version in pyproject.toml**
```bash
git commit -m "chore(release): bump version to 0.5.0"
```

**Merge to main:**
```bash
git merge --no-ff develop -m "chore(release): merge develop into main for v0.5.0"
git tag -a "v0.5.0" -m "feat: release v0.5.0 - retry working"
```

---

## Phase 13: Caching

**Branch:** `feat/6-caching`

| Commit | Message                                             |
| :----: | --------------------------------------------------- |
| 1      | `test(infra): add caching decorator tests`          |
| 2      | `feat(infra): implement cached weather provider`    |
| 3      | `test(integration): verify cache hit/miss behavior` |
| 4      | `chore(infra): wire cached provider`                |

**Merge to develop:**
```bash
git merge --no-ff feat/6-caching -m "feat: merge caching decorator for weather provider into develop"
```

**Bump version in pyproject.toml**
```bash
git commit -m "chore(release): bump version to 0.6.0"
```

**Merge to main:**
```bash
git merge --no-ff develop -m "chore(release): merge develop into main for v0.6.0"
git tag -a "v0.6.0" -m "feat: release v0.6.0 - caching working"
```

---

## Final Tag

```bash
git switch main
git merge --no-ff develop -m "chore(release): merge develop into main for v1.0.0"
git tag -a "v1.0.0" -m "feat: release v1.0.0 - weather analytics dashboard with REST API, CLI, caching and retry"
git push origin main
git push origin v1.0.0
```

---

*This document is updated as the project progresses.*