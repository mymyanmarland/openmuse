# Curated long-term memory (MEMORY.md)

Each owner has one curated memory file, stored in the server database under
`memory-file` / `MEMORY.md` and seeded on first run (see `AgentService.ensure`).
It is the agent's durable notebook: facts, preferences, decisions and open loops
that should survive across threads and restarts.

## How it works

- The chat agent reads the file's content at the start of every run (injected into
  the system prompt, capped at 6000 characters) and delegated tasks receive it as
  `curatedMemory` in their personal context.
- The agent maintains the file itself with two tools:
  - `read_memory` — read the current file (always read before writing).
  - `write_memory` — replace the file with the full updated text.
- `remember_fact` remains for single confirmed facts; MEMORY.md is for the curated,
  organized record.

## Maintenance rules (mirrored in the chat system prompt)

1. Read MEMORY.md when personal context matters; update it when the user shares
   durable facts, preferences, decisions, corrections or commitments.
2. Read before every write. Keep entries tight and dated; drop what no longer holds.
3. Never store passwords, tokens or other secrets in the file.
4. The file is per-owner: one user's memory never leaks into another's.

## Sections

- **Facts** — durable facts: name, timezone, accounts, projects, devices.
- **Preferences** — how things should be done; standing directives.
- **Decisions** — decisions made together, with dates.
- **Open loops** — commitments and follow-ups not yet resolved.
