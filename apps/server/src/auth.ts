import {
  createHash,
  createHmac,
  randomBytes,
  scrypt as scryptCallback,
  timingSafeEqual,
} from "node:crypto";
import { link, mkdir, readFile, unlink, writeFile } from "node:fs/promises";
import { join } from "node:path";
import type { Config } from "./config.ts";
import type { Store } from "./db.ts";
import { AppError } from "./errors.ts";

const digest = (value: string) => createHash("sha256").update(value).digest();

const USERNAME_PATTERN = /^[a-z0-9][a-z0-9._-]{2,31}$/i;
const RESERVED_USERNAMES = new Set(["local-user", "system"]);

export interface UserRecord {
  id: string;
  username: string;
  passwordHash: string;
  createdAt: string;
}

const scryptAsync = (password: string, salt: Buffer): Promise<Buffer> =>
  new Promise((resolve, reject) => {
    scryptCallback(password, salt, 64, (error, derived) =>
      error ? reject(error) : resolve(derived),
    );
  });

async function hashPassword(password: string): Promise<string> {
  const salt = randomBytes(16);
  const derived = await scryptAsync(password, salt);
  return `scrypt$${salt.toString("hex")}$${derived.toString("hex")}`;
}

async function verifyPassword(password: string, stored: string): Promise<boolean> {
  const [scheme, saltHex, hashHex] = stored.split("$");
  if (scheme !== "scrypt" || !saltHex || !hashHex) return false;
  const expected = Buffer.from(hashHex, "hex");
  const derived = await scryptAsync(password, Buffer.from(saltHex, "hex"));
  return derived.length === expected.length && timingSafeEqual(derived, expected);
}

function validUsername(username: string): string | null {
  const name = username.trim();
  if (!USERNAME_PATTERN.test(name)) return null;
  if (RESERVED_USERNAMES.has(name.toLowerCase())) return null;
  return name;
}

export class Auth {
  constructor(
    private readonly db: Store,
    private readonly config: Config,
    private readonly signingKey: string,
  ) {}
  async session(accessKey?: string) {
    if (
      this.config.mode === "live" &&
      (!accessKey ||
        !this.config.accessKey ||
        !timingSafeEqual(digest(accessKey), digest(this.config.accessKey)))
    )
      throw new AppError("Access key is incorrect", 401);
    return this.createSession("local-user");
  }
  /** Register a new user account. Always allowed when no users exist yet (bootstrap);
   * afterwards gated by ALLOW_SIGNUP. */
  async signup(username: string, password: string) {
    const name = validUsername(username);
    if (!name)
      throw new AppError(
        "Username must be 3-32 characters: letters, numbers, dot, underscore or dash",
        422,
      );
    if (password.length < 8) throw new AppError("Password must be at least 8 characters", 422);
    const id = name.toLowerCase();
    if (await this.db.get("system", "users", id))
      throw new AppError("That username is taken", 409);
    const users = await this.db.list("system", "users");
    if (users.length > 0 && !this.config.allowSignup)
      throw new AppError("Account creation is disabled on this server", 403);
    await this.db.put("system", "users", {
      id,
      username: name,
      passwordHash: await hashPassword(password),
      createdAt: new Date().toISOString(),
    } satisfies UserRecord);
    return this.createSession(id);
  }
  async login(username: string, password: string) {
    const id = username.trim().toLowerCase();
    const user = await this.db.get<UserRecord>("system", "users", id);
    const ok = user ? await verifyPassword(password, user.passwordHash) : false;
    if (!ok) throw new AppError("Incorrect username or password", 401);
    return this.createSession(id);
  }
  private async createSession(owner: string) {
    const token = randomBytes(32).toString("base64url");
    await this.db.put("system", "sessions", {
      id: digest(token).toString("hex"),
      owner,
      expiresAt: Date.now() + 24 * 60 * 60 * 1000,
    });
    return { token, mode: this.config.mode };
  }
  async owner(authorization?: string) {
    if (!authorization?.startsWith("Bearer ")) throw new AppError("Sign in to OpenMuse", 401);
    const session = await this.db.get<{ owner: string; expiresAt: number }>(
      "system",
      "sessions",
      digest(authorization.slice(7)).toString("hex"),
    );
    if (!session || session.expiresAt < Date.now())
      throw new AppError("Session expired. Sign in again.", 401);
    return session.owner;
  }
  sign(owner: string, path: string) {
    const expires = String(Date.now() + 15 * 60 * 1000);
    const signature = createHmac("sha256", this.signingKey)
      .update(`${owner}\n${path}\n${expires}`)
      .digest("hex");
    return `${this.config.publicUrl}${path}?owner=${encodeURIComponent(owner)}&expires=${expires}&signature=${signature}`;
  }
  verify(url: URL) {
    const owner = url.searchParams.get("owner") ?? "";
    const expires = url.searchParams.get("expires") ?? "";
    const signature = url.searchParams.get("signature") ?? "";
    if (
      !owner ||
      !/^\d+$/.test(expires) ||
      Number(expires) < Date.now() ||
      !/^\w{64}$/.test(signature)
    )
      throw new AppError("Document link expired; refresh the workspace", 401);
    const expected = createHmac("sha256", this.signingKey)
      .update(`${owner}\n${url.pathname}\n${expires}`)
      .digest("hex");
    if (!timingSafeEqual(Buffer.from(expected), Buffer.from(signature)))
      throw new AppError("Invalid access link", 403);
    return owner;
  }
}
export async function createAuth(db: Store, config: Config) {
  await mkdir(config.dataDir, { recursive: true, mode: 0o700 });
  const path = join(config.dataDir, "session-signing-key");
  let key: string;
  try {
    key = await readFile(path, "utf8");
  } catch (error) {
    if (!(error instanceof Error && "code" in error && error.code === "ENOENT")) throw error;
    key = randomBytes(32).toString("base64");
    const temporary = `${path}.${randomBytes(16).toString("hex")}.tmp`;
    await writeFile(temporary, key, { mode: 0o600, flag: "wx" });
    try {
      // Publish only complete bytes, without replacing another process's key.
      await link(temporary, path);
    } catch (error) {
      if (!(error instanceof Error && "code" in error && error.code === "EEXIST")) throw error;
      key = await readFile(path, "utf8");
    } finally {
      await unlink(temporary);
    }
  }
  return new Auth(db, config, key);
}
