Perform a release of the onecortex SDK. This is the full release workflow.

## Step 1: Pre-flight Checks

Run all checks and abort if any fail:

```
uv run pytest tests/unit/ -v
uv run ruff check src/ tests/
uv run mypy src/onecortex/
```

Also check `git status` for uncommitted changes. If there are uncommitted changes, warn the user and ask whether to proceed or commit first.

## Step 2: Determine Version Bump

Get the latest git tag matching `v*`:
```
git tag --list 'v*' --sort=-version:refname | head -1
```

If no tags exist, treat the base as `0.0.0`.

Get all commits since the last tag (or all commits if no tags):
```
git log <last-tag>..HEAD --oneline
```

Parse each commit for conventional commit prefixes to determine the bump:
- Any commit with `!` after type/scope OR `BREAKING CHANGE:` in body -> **major** bump
- Any `feat:` or `feat(scope):` commit -> **minor** bump
- Any `fix:` or `fix(scope):` commit -> **patch** bump
- If only `docs:`, `refactor:`, `test:`, `chore:`, `build:`, `ci:` commits -> **patch** bump

Apply the highest bump level found. Calculate the new version from the current version in `pyproject.toml`.

Show the proposed version to the user and ask for confirmation before proceeding.

## Step 3: Update Version

Edit `pyproject.toml` to update the `version = "X.Y.Z"` field to the new version.

## Step 4: Generate CHANGELOG

Create or update `CHANGELOG.md` at the project root. Group commits since last tag by type:

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Features
- description (commit hash)

### Bug Fixes
- description (commit hash)

### Documentation
- description

### Other Changes
- description
```

If `CHANGELOG.md` already exists, prepend the new section after the `# Changelog` header. If it doesn't exist, create it with:

```markdown
# Changelog

## [X.Y.Z] - YYYY-MM-DD
...
```

## Step 5: Commit and Tag

```
git add pyproject.toml CHANGELOG.md
git commit -m "chore(release): vX.Y.Z"
git tag vX.Y.Z
```

## Step 6: Build (Optional)

Ask the user if they want to build the package:
```
uv build
```

Show the built artifacts in `dist/`.

## Step 7: Next Steps

Print instructions:
- `git push && git push --tags` to push the release
- `uv publish` or `twine upload dist/*` when ready to publish to PyPI
- Remind about setting up PyPI credentials if not done yet
