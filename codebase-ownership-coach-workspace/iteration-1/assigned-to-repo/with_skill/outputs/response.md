# Skill response — Eval 1: assigned-to-repo

> User: "I just got assigned to this repo and I need to own it fast. Can you coach me on this codebase?"

---

## Phase 2 — BRIEF

Here's your orientation. This is a self-hosted EVM wallet agent — a Next.js backend that will eventually accept natural-language instructions and execute Ethereum transactions on behalf of a user.

- **What it is**: A Next.js 16 app deployed as a Docker container. The UI layer (`src/app/page.tsx`) is a stock placeholder — this is effectively a backend API project right now.
- **Stack**: Node.js 22, Next.js 16 App Router, TypeScript 5, SQLite via Drizzle ORM + `better-sqlite3`, viem for EVM interaction, Pino for structured logging, Zod for schema validation, Vitest for tests.
- **Entrypoints**: (1) `src/instrumentation.ts` — fires `runStartup()` on server boot (Node.js runtime only). (2) `src/middleware.ts` — guards all `/api/*` routes with `X-API-Key` auth, except `/api/health`. (3) `src/app/api/health/route.ts` — the only live API route today.
- **Subsystems** (4 implemented, several planned):
  - **Config & env** (`src/env.ts`, `config/chain.json`) — Zod-validated env singleton; chain ID locked by a static JSON file.
  - **Startup validation** (`src/lib/startup.ts`) — on boot: runs DB migrations, loads chain config, fetches RPC chain ID, asserts match. Calls `process.exit(1)` on any failure.
  - **DB layer** (`src/lib/db/`) — Drizzle + SQLite. One table so far: `system_config` (key/value store). Migrations in `src/lib/db/migrations/`.
  - **Shared utilities** (`src/lib/errors.ts`, `src/lib/json.ts`, `src/lib/logger.ts`, `src/lib/rpc-chain.ts`) — centralized error codes, typed JSON response helpers, Pino singleton with key-material redaction, viem public client for chain ID queries.
- **Planned but absent**: `src/core/` (key management, tx building, simulation, LLM agent loop) — referenced in `AGENTS.md` boundary rules but not yet implemented.
- **Non-obvious thing**: The middleware implements a **custom timing-safe string comparison** for the API key check. Node's `crypto.timingSafeEqual` is not available in the Edge-compatible middleware runtime, so it was written from scratch using bitwise OR accumulation. Most devs would reach for `===` and introduce a timing oracle.

---

Ready to coach. I'll ask one question at a time. Take your time — think before you answer.

---

**Question 1:**

When the Next.js server boots, `src/instrumentation.ts` triggers a startup sequence. Walk me through what that sequence does — what is called, in what order, and what causes the process to abort rather than continue serving requests?
