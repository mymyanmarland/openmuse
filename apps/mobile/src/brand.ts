// Brand constants — the single place to change when rebranding.
// Defaults are the upstream OpenMuse identity; the final name/logo are decided
// separately (see docs/REBRAND.md). Do not put secrets here.

export const brand = {
  /** Product name shown in the UI. */
  name: "OpenMuse",
  /** Expo slug / URL scheme. Changing this also needs app.json + native identifiers. */
  slug: "openmuse",
  scheme: "openmuse",
  /** Title on the sign-in screen. */
  welcomeTitle: "Welcome to OpenMuse.",
  /** Logo asset. Swap the file to rebrand the mascot everywhere. */
  logo: require("../assets/capybara.png"),
} as const;

/** App color palette (moved here from ui.tsx so brand + colors live together). */
export const colors = {
  canvas: "#FCFCFC",
  card: "#FFFFFF",
  text: "#11191C",
  muted: "#697176",
  line: "#EEEEF0",
  blue: "#C8E7FF",
  blueDark: "#1473C8",
  sky: "#EDF7FD",
  green: "#E3F3E8",
  lavender: "#F0EEFA",
  orange: "#FDF0DF",
  danger: "#AA4A45",
};
