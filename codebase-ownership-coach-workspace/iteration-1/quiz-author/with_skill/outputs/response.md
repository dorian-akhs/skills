# Skill response — Eval 2: quiz-author

> User: "I built this project myself 6 months ago, barely remember how it works. Quiz me hard on the architecture."

---

## Phase 2 — BRIEF

You built this. So I won't walk you through what a Next.js app is. Here's the current state — the non-obvious parts included — then we quiz.

- **What it is:** A self-hosted EVM wallet agent exposed as a Next.js 16 API-first backend. The UI (`page.tsx`) is still the default create-next-app scaffold — it's infrastructure-only right now.
- **Stack:** Next.js 16 (App Router, standalone output) · React 19 · TypeScript · Drizzle ORM + better-sqlite3 · viem · Zod · Pino · Vitest · Docker/Compose.
- **Entrypoints:** (1) `src/instrumentation.ts` → `register()` fires on Node.js runtime boot; (2) `src/middleware.ts` intercepts every `/api/*` request; (3) `src/app/api/health/route.ts` — the only live route.
- **Startup subsystem:** `runStartup()` runs two sequential guards — DB migrations, then RPC chain ID validation against `config/chain.json`. Either failure calls `process.exit(1)`.
- **Env subsystem:** `src/env.ts` — Zod-parsed, singleton-cached, lazy-resolved typed proxy. `DATA_DIR` must be an absolute path. All 5 required keys are batch-validated with a single descriptive error.
- **Auth subsystem:** `src/middleware.ts` — constant-time `X-API-Key` comparison against `env.API_SECRET`. One path is explicitly whitelisted.
- **DB subsystem:** SQLite via Drizzle. One table: `system_config (key PK, value)`. DB lives at `$DATA_DIR/app.db`, created on first startup.
- **Config subsystem:** `config/chain.json` — static file (not an env var) defining expected `chainId`, cross-checked against the live RPC at startup.
- **Non-obvious detail:** The `env` export is a *proxy of getters*, not a plain object. Validation fires on first property access, not at module load — meaning Edge runtime code that touches `env.*` will also trigger it. The `NEXT_RUNTIME === "nodejs"` guard in instrumentation explicitly scopes startup to Node only.
- **Sharp edge:** `fetchRpcChainId()` has no unit test for the live RPC call path. Only `assertChainIdMatch` (pure logic) is tested. The actual network → startup integration path has zero test coverage.

Ready to coach. I'll ask one question at a time. Take your time — think before you answer.

---

## Question 1

The middleware has a single explicit bypass. What is the bypassed path, where precisely is that bypass enforced in the code, and why would you design it that way rather than just excluding `/api/health` from the middleware `matcher`?
