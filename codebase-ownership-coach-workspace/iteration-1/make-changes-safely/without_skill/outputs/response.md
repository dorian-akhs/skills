# Baseline response — Eval 3: make-changes-safely

> User: "Teach me this codebase. I want to understand it well enough to make changes without breaking things."

---

# Codebase Tour: wallet-agent

## What this project is

A **self-hosted EVM wallet agent** — a Next.js 16 API server you run yourself (via Docker or bare pnpm) that exposes HTTP endpoints for interacting with an Ethereum-compatible chain. It's an early scaffold: the infrastructure wiring is solid and well-designed, but the actual wallet/agent features are not built yet.

---

## Project structure (what matters)

```
wallet-agent/
├── config/
│   └── chain.json          ← which chain to connect to (chainId + name)
├── src/
│   ├── env.ts              ← THE single source of truth for all env vars
│   ├── middleware.ts        ← X-API-Key auth guard for all /api/* routes
│   ├── instrumentation.ts  ← Next.js startup hook (runs DB migrations + chain ID check)
│   ├── app/
│   │   ├── layout.tsx      ← root HTML shell
│   │   ├── page.tsx        ← placeholder home page (not relevant to API work)
│   │   └── api/
│   │       └── health/route.ts   ← GET /api/health (no auth required)
│   └── lib/
│       ├── errors.ts        ← centralized error code constants
│       ├── json.ts          ← apiResponse() / apiError() helpers
│       ├── logger.ts        ← pino logger singleton with secret redaction
│       ├── chain-config.ts  ← reads + validates config/chain.json via Zod
│       ├── rpc-chain.ts     ← fetches chain ID from RPC, asserts it matches config
│       ├── startup.ts       ← orchestrates migrations + chain validation at boot
│       └── db/
│           ├── schema.ts    ← Drizzle schema (currently: system_config table only)
│           ├── migrate.ts   ← runs Drizzle migrations against the SQLite DB file
│           └── migrations/  ← SQL migration files (auto-generated, never hand-edit)
├── .env.example            ← all required + optional env vars documented
├── drizzle.config.ts       ← drizzle-kit config (schema + migrations folder)
├── next.config.ts          ← standalone output + better-sqlite3 as external package
├── vitest.config.ts        ← test runner config (@/* alias, node env)
├── eslint.config.mjs       ← ESLint: enforces no Next.js/React in src/core/
├── Dockerfile              ← 3-stage build: deps → builder → runner
└── docker-compose.yml      ← single service, /data volume, health check
```

---

## Key concepts

### 1. `src/env.ts` is the ONLY way to read env vars

### 2. The startup sequence

`src/instrumentation.ts` runs once in Node.js runtime before any request:
1. `runMigrations()` — creates the SQLite DB, runs pending migrations. Process **exits** if fails.
2. `loadChainConfig()` — reads and validates `config/chain.json`.
3. `fetchRpcChainId()` — hits `RPC_URL` with viem. Process **exits** if RPC unreachable.
4. `assertChainIdMatch()` — verifies chain IDs match. Process **exits** if they differ.

### 3. API authentication

`src/middleware.ts` runs on every `/api/*` route **except** `/api/health`. Requires `X-API-Key: <API_SECRET>`. Timing-safe comparison.

### 4. Response shape contract

All API responses use `apiResponse()` / `apiError()` from `src/lib/json.ts`. Never `NextResponse.json()` directly.

### 5. Error codes

All in `src/lib/errors.ts` as `ErrorCodes`. Never inline error strings.

### 6. Layer boundary rules (enforced by ESLint)

`src/core/` cannot import `next/*` or `react`.

### 7. Database (SQLite via Drizzle ORM)

DB at `env.DATA_DIR + "/app.db"`. One table: `system_config` (key/value). Never hand-edit migrations.

### 8. Logging

Use `getLogger()` from `src/lib/logger.ts`. Redacts `privateKey`, `mnemonic`, `password`, `keystore`.

### 9. On-chain numerics

Use `bigint` for all on-chain values. Only convert at API boundaries.

---

## Trip wires — things that will break if you ignore them

1. **Reading `process.env` directly** — not validated, no defaults.
2. **`src/core/` importing `next/*` or `react`** — ESLint catches it.
3. **Adding an env var without updating `src/env.ts` AND `.env.example`** — fails at use time.
4. **Hand-editing migration files** — Drizzle checksum mismatch.
5. **Using `number` for on-chain values** — silent precision loss above 2^53.
6. **Calling `NextResponse.json()` directly** — wrong response envelope.
7. **`config/chain.json` chainId not matching `RPC_URL`** — immediate exit at startup.
8. **`DATA_DIR` being a relative path** — rejected at startup.

---

## How to add a new API route (the correct pattern)

```ts
// src/app/api/example/route.ts
import { apiResponse, apiError } from "@/lib/json";
import { ErrorCodes } from "@/lib/errors";
import { getLogger } from "@/lib/logger";

const log = () => getLogger();

export async function GET() {
  log().info("handling GET /api/example");
  return apiResponse({ hello: "world" });
}
```

Auth is handled by middleware — don't repeat it in routes.
