// Brand constants — the single place to change when rebranding the server.
// Defaults are the upstream OpenMuse identity; the final name is decided
// separately (see docs/REBRAND.md). Do not put secrets here.
export const brand = {
  /** Product name used in telemetry, logs and user-facing messages. */
  name: "OpenMuse",
} as const;
