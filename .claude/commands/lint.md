Run linting and type checking on the onecortex SDK.

## Step 1: Ruff Lint

```
uv run ruff check src/ tests/
```

## Step 2: Mypy Type Check

```
uv run mypy src/onecortex/
```

## Reporting

Summarize results:
- Total ruff issues (by rule category)
- Total mypy errors (by error code)
- List each issue with file, line number, rule/code, and message

## Auto-fix

If ruff found fixable issues, ask the user if they want to auto-fix:
```
uv run ruff check src/ tests/ --fix
```

For mypy errors, suggest specific code changes to resolve each error.
