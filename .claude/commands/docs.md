Update documentation to match the current SDK API surface.

## Step 1: Read Current Code

Read all source files under `src/onecortex/` to understand the current API:
- `__init__.py` — public exports
- `_client.py` — Onecortex facade
- `_http.py` — HttpClient
- `vector/_client.py` — VectorClient methods and signatures
- `vector/_index.py` — Index methods and signatures
- `vector/models.py` — all pydantic models and their fields
- `auth/_client.py` — AuthClient
- `exceptions.py` — exception classes

## Step 2: Read Current Docs

Read `docs/vector-api.md` and `README.md`.

## Step 3: Compare and Update

Identify discrepancies:
- Methods/parameters in code but not in docs
- Docs referencing removed or renamed methods
- Missing code examples for new features
- Incorrect method signatures or return types in docs
- New models or exception classes not documented

Update `docs/vector-api.md` and `README.md` to match the code. Preserve the existing documentation style, structure, and formatting conventions.

## Step 4: Report

Summarize what was changed and why. Show a brief diff summary.
