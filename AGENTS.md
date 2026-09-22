# Portfolio development workflow

- Follow the seven-day Version 1 plan and the requirements in `docs/requirements.md`.
- The user requests that completed implementation work be committed in focused,
  logical commits with relevant messages, then pushed to the configured GitHub
  upstream. Keep this preference for subsequent portfolio work.
- Use descriptive prefixes such as `chore:`, `feat:`, `test:`, and `docs:`.
  Group related changes together; avoid combining unrelated work in one commit.
- Run checks appropriate to the changed functionality before pushing. Report
  the checks and resulting commits to the user.
- Keep local environments, caches, and graphify outputs out of the repository.
- Preserve unrelated user changes and existing history. Do not force-push or
  amend published commits unless the user specifically requests it.
