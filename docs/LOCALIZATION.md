# Localization groundwork

UI strings are centralized in `apps/mobile/src/strings.ts` so translations can
drop in without touching components.

## How it works

- `strings.ts` exports the `Strings` interface, the default English catalog `en`,
  a `setLocale()` switch, and a `strings` Proxy that always serves the active
  locale: components read `strings.<section>.<key>`.
- Only the sign-in screen (`apps/mobile/App.tsx`) is migrated so far; it is the
  reference implementation. Other screens still carry inline English and should
  be migrated one screen at a time: add their keys under a new section in the
  `Strings` interface, add English text to `en`, and replace the literals.

## Adding a locale (e.g. Burmese)

1. Create `apps/mobile/src/strings.my.ts` exporting a `Strings` object with the
   translated text. Every key in the interface must be present.
2. At startup (before first render, e.g. in `apps/mobile/App.tsx`), choose the
   locale — for example from `process.env.EXPO_PUBLIC_LOCALE` — and call
   `setLocale(my)`.
3. Brand strings (app name, logo) live in the brand module, not here; see the
   rebrand notes in the main README.

## Rules

- Never put secrets in translated strings.
- Keep placeholders (`{apiUrl}`-style function args) in every translation.
- The default English catalog must always stay complete; it is the fallback
  reference for translators.
