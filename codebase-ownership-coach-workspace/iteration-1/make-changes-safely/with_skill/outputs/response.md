# Skill response — Eval 3: make-changes-safely

> User: "Teach me this codebase. I want to understand it well enough to make changes without breaking things."

---

## Phase 2 — BRIEF: wallet-agent orientation

**What the system is:**
A self-hosted EVM wallet agent served as a Next.js API. The UI is a placeholder — the real surface is a JSON HTTP API that an LLM orchestrator (or external caller) uses to interact with an Ethereum wallet on a configured chain.

**10-bullet orient:**

- **Stack**: Next.js 16 (App Router, standalone output) · React 19 · TypeScript · Drizzle ORM + better-sqlite3 (SQLite) · viem (EVM) · pino (logging) · zod (validation) · Vitest
- **Entrypoints**: `src/instrumentation.ts` fires at server boot via Next.js `register()` hook; `src/middleware.ts` guards every `/api/*` request; `src/app/api/health/route.ts` is the only implemented route so far
- **Startup guard**: On boot, the server (1) runs DB migrations, (2) fetches the chain ID from the RPC and compares it to `config/chain.json`. If either fails, `process.exit(1)` is called immediately — no soft degradation
- **Auth boundary**: All `/api/*` routes except `/api/health` require `X-API-Key` matching `API_SECRET`. The check uses a constant-time string compare in `src/middleware.ts` to prevent timing attacks
- **Env contract**: `src/env.ts` is the single source of truth for all environment variables — nothing else reads `process.env` directly (convention enforced by AGENTS.md)
- **Database**: SQLite at `$DATA_DIR/app.db`. One table currently: `system_config (key PK, value)`. Migrations run synchronously at startup before any request is served
- **Layer boundary rule**: `src/core/` (not yet populated) must never import `next/*` or `react` — enforced by ESLint in `eslint.config.mjs`. This separates domain logic from framework glue
- **Three documented invariants (AGENTS.md)**: (1) build tx once → sign exact object → broadcast, never reconstruct after simulation; (2) only `account.address` exits `src/core/keys/`, never the `Account` object; (3) all on-chain numerics use `bigint` in core, serialised at the API boundary only
- **Deployment**: 3-stage Docker build (deps → builder → runner). Build-time secrets passed as `ARG` (not `ENV`) to avoid layer history leakage. Docker Compose mounts a named volume at `/data` and overrides `DATA_DIR` to match
- **Tests**: Vitest, node environment. Coverage focused on `env.ts`, `chain-config.ts`, and `rpc-chain.ts` — all startup-critical. CI runs lint → format-check → typecheck → test → build

**Non-obvious observation (the sharp edge):**

`src/core/` is declared empty, but AGENTS.md already commits to three invariants that assume it's populated — most critically, invariant #2: only `account.address` leaves `src/core/keys/`, never the full `Account` object. This is not enforced by the type system, tests, or ESLint. It exists only in documentation. The logger does redact `privateKey` fields in pino output, but that is a fallback — not a guarantee. The first developer to implement `src/core/keys/` without reading AGENTS.md could silently leak private key material into API responses or logs, and nothing will catch it at compile or test time.

---

Ready to coach. I'll ask one question at a time. Take your time — think before you answer.

**First question:**

The server runs a startup sequence before it can serve requests. What are the two things it validates during startup, and what happens if either validation fails?
