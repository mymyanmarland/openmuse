// Central UI string catalog (groundwork for localization).
//
// Default locale is English (`en`). To add a locale — e.g. Burmese — create
// `strings.<locale>.ts` exporting a `Strings` object, then call
// `setLocale(<locale>)` once at startup (see docs/LOCALIZATION.md).
// Components read `strings.<section>.<key>`; the Proxy below always serves the
// active locale. Only the auth screen is migrated so far; other screens keep
// inline English until they are migrated one by one.

export interface Strings {
  app: {
    /** Non-brand tagline under the welcome title. */
    tagline: string;
  };
  auth: {
    username: string;
    usernamePlaceholder: string;
    password: string;
    passwordPlaceholder: string;
    accessKey: string;
    accessKeyPlaceholder: string;
    signIn: string;
    createAccount: string;
    openWithAccessKey: string;
    /** Note about local workspaces; receives the API URL. */
    localNote: (apiUrl: string) => string;
  };
  common: {
    cancel: string;
    save: string;
    retry: string;
    close: string;
    loading: string;
  };
}

export const en: Strings = {
  app: {
    tagline: "A little room for your day.",
  },
  auth: {
    username: "Username",
    usernamePlaceholder: "Your account username",
    password: "Password",
    passwordPlaceholder: "Your account password",
    accessKey: "Workspace access key (legacy single-user)",
    accessKeyPlaceholder: "Required for a live workspace",
    signIn: "Sign in",
    createAccount: "Create account",
    openWithAccessKey: "Open with access key",
    localNote: (apiUrl) =>
      `Local workspaces open without a key. Make sure your OpenMuse server is running at ${apiUrl}.`,
  },
  common: {
    cancel: "Cancel",
    save: "Save",
    retry: "Retry",
    close: "Close",
    loading: "Loading…",
  },
};

let active: Strings = en;

/** Switch the active locale. Call once at startup, before first render. */
export function setLocale(next: Strings): void {
  active = next;
}

/** Always resolves keys against the active locale. */
export const strings: Strings = new Proxy({} as Strings, {
  get: (_target, key: string) => (active as unknown as Record<string, unknown>)[key],
});
