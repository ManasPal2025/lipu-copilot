# Contributing to LIPU Platform

Thank you for your interest in contributing to the LIPU Platform! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- No harassment or discrimination
- Focus on constructive feedback
- Respect different perspectives

## Getting Started

### 1. Fork & Clone

```bash
git clone https://github.com/your-username/lipu-platform.git
cd lipu-platform
git remote add upstream https://github.com/lipu/lipu-platform.git
```

### 2. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-name
# or
git checkout -b docs/documentation-update
```

### 3. Setup Development Environment

See [docs/guides/development-setup.md](docs/guides/development-setup.md)

## Development Standards

### Git Commit Messages

Follow conventional commits:

```
feat: add new feature
fix: fix bug
docs: update documentation
style: code style changes
refactor: refactor code
perf: performance improvements
test: add tests
chore: maintenance
```

Example:
```
feat: add house visualization upload component

- Create upload component with drag-and-drop
- Integrate with AI visualization API
- Add error handling and validation
- Add 3 unit tests
```

### Code Quality

#### Frontend

```bash
npm run -w apps/web lint       # ESLint
npm run -w apps/web type-check # TypeScript
npm run -w apps/web format     # Prettier
npm run -w apps/web test       # Jest
```

Requirements:
- No ESLint warnings
- TypeScript strict mode (no `any`)
- 80%+ test coverage
- Formatted with Prettier

#### Backend

```bash
cd apps/api
black --check .               # Format check
flake8 .                      # Linting
mypy .                        # Type checking
pytest                        # Tests
```

Requirements:
- No Black formatting issues
- Flake8 clean (max line length: 100)
- MyPy strict mode
- 80%+ test coverage

## Pull Request Process

### Before Submitting

1. **Update branch**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Run tests locally**
   ```bash
   npm run test        # Frontend
   cd apps/api && pytest  # Backend
   ```

3. **Check linting**
   ```bash
   npm run lint
   npm run type-check
   ```

### Create Pull Request

1. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Open PR on GitHub**
   - Title: Clear, descriptive title
   - Description: Use the PR template
   - Reference: Link related issues (#123)

3. **PR Template**

```markdown
## Description
Brief description of changes

## Type
- [ ] Feature
- [ ] Bug fix
- [ ] Documentation
- [ ] Performance
- [ ] Refactor

## Related Issue
Closes #123

## How to Test
1. Step 1
2. Step 2
3. Step 3

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Tests added (80%+ coverage)
- [ ] Documentation updated
- [ ] No new warnings generated
```

## Code Review

Your PR will be reviewed by at least 2 maintainers.

### What Reviewers Look For

- ✅ Code quality and standards
- ✅ Test coverage
- ✅ Performance impact
- ✅ Security considerations
- ✅ Documentation completeness
- ✅ API contract compliance

### Addressing Feedback

- Respond to all comments
- Don't push force-update unless agreed
- Respond with "Done" or explanations
- Re-request review after changes

## Issues

### Reporting Bugs

Use the bug template:

```markdown
## Description
Clear bug description

## Reproduction Steps
1. Step 1
2. Step 2
3. Step 3

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: Windows/Mac/Linux
- Node: 20.0.0
- Python: 3.11

## Screenshots
If applicable
```

### Feature Requests

Use the feature template:

```markdown
## Description
Feature description and use case

## Motivation
Why is this needed?

## Proposed Solution
How should this be implemented?

## Alternatives
Other solutions considered
```

## Project Structure References

- [03-FOLDER-STRUCTURE.md](docs/architecture/03-FOLDER-STRUCTURE.md) - Code organization
- [07-SPRINT-0-EXECUTION-PLAN.md](docs/architecture/07-SPRINT-0-EXECUTION-PLAN.md) - Technical blueprint

## Development Guides

- [Development Setup](docs/guides/development-setup.md)
- [Database Migrations](docs/guides/database-migrations.md)
- [API Development](docs/guides/api-development.md)
- [Testing Strategy](docs/guides/testing-strategy.md)

## Questions?

- Check existing issues/discussions
- Read documentation in [docs/](docs/)
- Create a new discussion

## License

By contributing, you agree to license your work under MIT License.

---

Thank you for contributing to LIPU! 🚀
