# Pull Request - Weather Analytics Dashboard

## 📋 Description
<!-- What does this PR do? Why is it needed? -->
<!-- Reference the phase from docs/development-plan.md if applicable (e.g., Phase 8: /health endpoint) -->

---

## 🔗 Related Issues
Closes #

Relates to #

---

## 🎯 Type of Change
- [ ] 🐛 Bug fix
- [ ] ✨ New feature
- [ ] 💥 Breaking change
- [ ] 📝 Documentation
- [ ] 🎨 Refactor / code improvement
- [ ] ⚡ Performance improvement
- [ ] ✅ Tests
- [ ] 🔧 Configuration

---

## 🏗️ Architecture Impact

- [ ] Domain layer
- [ ] Application layer
- [ ] Infrastructure layer
- [ ] Presentation layer (API / CLI)
- [ ] Dependency Injection (composition root)
- [ ] Requires ADR update (`docs/decisions.md`)

### If architecture changes:
- [ ] Architecture docs updated (`docs/architecture.md`)
- [ ] ADR created/updated
- [ ] Backward compatibility considered

---

## 🧪 Testing

- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Smoke tests pass (app boots correctly)
- [ ] Tests pass locally (`make test`)

### Manual testing performed
```bash
# Example:
make dev
curl http://localhost:8000/health
```

---

## ✅ Checklist

### Code Quality

- [ ] Commit messages follow Conventional Commits (`feat:`, `test:`, etc.)
- [ ] Follows Clean Architecture (no layer violations)
- [ ] Async-first (no blocking I/O)
- [ ] Proper error handling across layers
- [ ] Uses existing ports/adapters correctly

### Tooling

- [ ] Lint passes (`make lint`)
- [ ] Format passes (`make format`)
- [ ] Type check passes (`make type-check`)

### Configuration

- [ ] `.env.example` updated if needed
- [ ] `pyproject.toml` updated if needed
- [ ] No secrets committed

---

## 📊 Impact

- [ ] Affects caching behavior
- [ ] Affects database layer
- [ ] Affects external API usage
- [ ] Affects performance

### Notes

<!-- Optional: describe impact -->

---

## 🚀 Deployment Notes

- [ ] No special action required
- [ ] Requires env variables update
- [ ] Requires database changes
- [ ] Requires service restart

---

## 📝 Additional Context

<!-- Anything else reviewers should know -->

---

## 🔄 Breaking Changes (if applicable)

- **Impact:**
- **Migration steps:**

---

## 🔍 Reviewer Guidelines

- Check architecture boundaries (domain ↔ infra)
- Ensure no HTTP/database logic leaks into domain
- Verify async usage (no blocking calls)
- Validate tests cover the change

---

**By submitting this PR, I confirm that:**
- [ ] This code is ready for review (or marked as draft if WIP)
- [ ] I have tested my changes locally
- [ ] I have updated documentation if needed