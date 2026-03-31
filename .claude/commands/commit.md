Create a conventional commit for the current changes.

## Step 1: Analyze Changes

Run `git status` and `git diff` (both staged and unstaged) to understand all changes. Summarize the changes in bullet points.

## Step 2: Determine Commit Type and Scope

Choose the appropriate conventional commit type:
- `feat` — new functionality (new method, class, parameter, endpoint)
- `fix` — bug fix
- `docs` — documentation only changes
- `refactor` — code restructuring without behavior change
- `test` — adding or modifying tests
- `chore` — build config, dependencies, tooling, automation
- `build` — build system changes
- `ci` — CI/CD changes

Choose scope from: `vector`, `auth`, `http`, `models`, `tests`, `docs`, or omit if changes span multiple areas.

If the change is breaking, add `!` after the scope: `feat(vector)!: remove deprecated method`

## Step 3: Write Commit Message

Format: `type(scope): short description`
- First line under 72 characters, lowercase, no period
- Add a body paragraph if the change is complex (separated by blank line)
- If breaking, include `BREAKING CHANGE:` footer explaining what breaks

## Step 4: Create the Commit

- Stage the appropriate files individually (be specific — never `git add .` or `git add -A`)
- Never stage `.env`, credentials, or secret files
- Show the proposed commit message and ask the user for confirmation
- Create the commit
