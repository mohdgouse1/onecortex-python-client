Review current code changes for quality, correctness, and completeness.

## Step 1: Gather Changes

Run `git diff` (unstaged) and `git diff --cached` (staged) to see all changes.

## Step 2: Analyze Each Changed File

For each file with changes, check:

### Code Quality
- Naming conventions (snake_case methods, PascalCase classes)
- Code structure and readability
- Error handling patterns (use project's exception hierarchy)
- Adherence to project conventions from CLAUDE.md

### Correctness
- Logic errors and edge cases
- Potential runtime errors (None access, index out of bounds, etc.)
- API contract compliance (request/response shapes matching server API)

### Type Safety
- Proper type annotations on all public methods
- Pydantic model usage with correct aliases and ConfigDict
- Return types matching actual returns

### Test Coverage
- Do the changes have corresponding unit tests?
- Are edge cases tested?
- Suggest specific tests that should be added

### SDK-Specific Checks
- New public API re-exported in `src/onecortex/__init__.py` and `__all__`?
- New pydantic models using `Field(alias=...)` where server uses camelCase?
- HTTP calls going through `HttpClient`, not raw httpx?
- New exceptions inheriting from `OnecortexError`?

## Step 3: Report Findings

Organize by severity:
1. **Errors** — must fix (bugs, security issues, broken API contracts)
2. **Warnings** — should fix (missing tests, type issues, convention violations)
3. **Suggestions** — nice to have (readability, minor improvements)

Offer to fix any issues found.
