import assert from "node:assert/strict";
import { mkdtemp, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test, { type TestContext } from "node:test";
import { createAuth } from "../apps/server/src/auth.ts";
import type { Config } from "../apps/server/src/config.ts";
import { createStore, type Store } from "../apps/server/src/db.ts";

function config(dataDir: string, allowSignup = true): Config {
  return {
    mode: "sample",
    port: 8787,
    host: "127.0.0.1",
    publicUrl: "http://localhost:8787",
    dataDir,
    agentBackend: "sample",
    allowedOrigins: [],
    googleRedirectUri: "http://localhost:8787/api/google/callback",
    allowSignup,
  };
}

async function setup(t: TestContext, allowSignup = true) {
  const directory = await mkdtemp(join(tmpdir(), "openmuse-auth-accounts-"));
  t.after(() => rm(directory, { recursive: true, force: true }));
  const db: Store = await createStore();
  const auth = await createAuth(db, config(directory, allowSignup));
  return { db, auth };
}

test("signup creates a user and returns a working session", async (t) => {
  const { auth } = await setup(t);
  const session = await auth.signup("Alice", "correct-horse-123");
  assert.ok(session.token.length > 20);
  assert.equal(session.mode, "sample");
  const owner = await auth.owner(`Bearer ${session.token}`);
  assert.equal(owner, "alice");
});

test("signup rejects duplicate usernames case-insensitively", async (t) => {
  const { auth } = await setup(t);
  await auth.signup("Alice", "correct-horse-123");
  await assert.rejects(() => auth.signup("alice", "another-pass-123"), /taken/);
});

test("signup validates username and password", async (t) => {
  const { auth } = await setup(t);
  for (const bad of ["ab", "a b", "local-user", "system"]) {
    await assert.rejects(() => auth.signup(bad, "long-enough-123"), /Username/);
  }
  await assert.rejects(() => auth.signup("bob", "short"), /at least 8/);
});

test("login accepts the right password and rejects the wrong one", async (t) => {
  const { auth } = await setup(t);
  await auth.signup("carol", "correct-horse-123");
  const session = await auth.login("carol", "correct-horse-123");
  assert.equal(await auth.owner(`Bearer ${session.token}`), "carol");
  await assert.rejects(() => auth.login("carol", "wrong-password"), /Incorrect username or password/);
  await assert.rejects(() => auth.login("nobody", "whatever-123"), /Incorrect username or password/);
});

test("passwords are stored as scrypt hashes, never plaintext", async (t) => {
  const { db, auth } = await setup(t);
  await auth.signup("dave", "correct-horse-123");
  const stored = await db.get<{ passwordHash: string }>("system", "users", "dave");
  assert.ok(stored?.passwordHash.startsWith("scrypt$"));
  assert.ok(!stored?.passwordHash.includes("correct-horse-123"));
});

test("first user can bootstrap even when ALLOW_SIGNUP=false", async (t) => {
  const { auth } = await setup(t, false);
  const session = await auth.signup("erin", "correct-horse-123");
  assert.equal(await auth.owner(`Bearer ${session.token}`), "erin");
  await assert.rejects(() => auth.signup("frank", "correct-horse-123"), /disabled/);
});

test("legacy access-key sessions still resolve to local-user", async (t) => {
  const { auth } = await setup(t);
  const session = await auth.session(undefined);
  assert.equal(await auth.owner(`Bearer ${session.token}`), "local-user");
});
