# Rebrand checklist

Brand constants are centralized so a rename needs no code archaeology. The
final name is **ShweMind** (decided 2026-10-15) — applied to code + app.json +
README. Still open: **logo asset** (currently the upstream capybara).

## One-place changes (code)

- Mobile: `apps/mobile/src/brand.ts` — `name`, `slug`, `scheme`, `welcomeTitle`,
  `logo` (asset path), and the `colors` palette. Everything else reads from here.
- Server: `apps/server/src/brand.ts` — `name` (telemetry title, API root, user label).

## Must also change (config / assets)

- `apps/mobile/app.json` — `name`, `slug`, `scheme`, `ios.bundleIdentifier`,
  `android.package`, `web.name`.
- Logo asset — replace `apps/mobile/assets/capybara.png` (or point `brand.logo`
  at the new file). Also check `assets/` at the repo root for README art.
- `README.md` title, tagline and screenshots; `docs/` references to "OpenMuse".

## Nice to have

- Log prefixes (`[OpenMuse]`, "Sign in to OpenMuse") in `apps/server/src/*.ts`.
- Google OAuth consent screen / redirect docs if the public name changes.
- README badges and the `package.json` name.

## Out of scope for a rename

- `OPENMUSE_*` env var names (keep for backwards compatibility unless a major
  version bump is planned).
- Database kinds (`agent-settings`, `memory-file`, …) — internal only.
