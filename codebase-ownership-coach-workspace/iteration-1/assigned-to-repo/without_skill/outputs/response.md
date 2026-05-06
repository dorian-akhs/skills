# Baseline response — Eval 1: assigned-to-repo

> User: "I just got assigned to this repo and I need to own it fast. Can you coach me on this codebase?"

---

# Codebase Coaching: wallet-agent

## What This Project Is

`wallet-agent` is a **self-hosted EVM wallet agent** built on Next.js. The concept: deploy it on your own infrastructure, configure it with an RPC endpoint and LLM API key, and interact with it through a web chat UI or CLI to execute on-chain transactions in plain language.

This is a **portfolio project** (not a regulated product), built as a full-stack app with a strict architectural boundary between framework code and pure business logic.

---

## Current Status: Early Foundation

You are inheriting a project where **Story 1.1 is in "review" status and everything else is backlog.** The skeleton is solid but the product doesn't exist yet.

**What's built:**
- Next.js 16 scaffold (App Router, Turbopack, Tailwind v4, TypeScript strict)
- `src/env.ts` — Zod-validated env config with caching and test helpers
- `src/middleware.ts` — API key auth via `X-API-Key` header (timing-safe)
- `src/lib/chain-config.ts` — loads/validates `config/chain.json`
- `src/lib/rpc-chain.ts` — validates RPC chain ID against config at startup
- `src/lib/startup.ts` — orchestrates DB migrations + chain ID check before serving
- `src/instrumentation.ts` — Next.js hook that triggers `runStartup()` on boot
- `src/lib/db/schema.ts` + `migrate.ts` — Drizzle + better-sqlite3, `system_config` table
- `src/lib/logger.ts` — Pino structured logger with redaction of sensitive keys
- `src/lib/errors.ts` + `src/lib/json.ts` — typed error codes and standardized API response helpers
- `src/app/api/health/route.ts` — public health endpoint (the only real API route)
- Docker: multi-stage `Dockerfile` + `docker-compose.yml` with health check
- Unit tests for `env`, `chain-config`, `rpc-chain`

**What's NOT built yet (all backlog):**
- Key onboarding (generate/import wallet)
- Web chat UI or CLI
- Agent core (LLM orchestration, tools)
- Wallet read tools (balances, gas, token price)
- Transaction construction, simulation, broadcast
- Swaps (Li.Fi / 1inch)
- Autonomous strategy scheduler

`src/app/page.tsx` is still the create-next-app placeholder. No real UI exists.

---

## Architecture Mental Model

### The Core Boundary Rule

```
src/core/   — Pure business logic. NO Next.js, NO React. Doesn't exist yet.
src/lib/    — Non-framework utilities (logger, db, errors, json helpers).
src/app/    — Next.js routes and API handlers. Entry points only.
```

This is **enforced by ESLint** in `eslint.config.mjs` — any `import` from `next/*` or `react` inside `src/core/` will fail CI. `src/core/` doesn't exist yet but is the destination for all agent logic in Epics 2–5.

### The 5 Key Invariants (from `AGENTS.md`)

1. **Build tx once → sign exact object → broadcast.** Never reconstruct after simulation.
2. **Only `account.address` exits `src/core/keys/`.** The `Account` object never leaves the key layer.
3. **All on-chain numerics use `bigint` in core.** Serialize at boundary via `apiResponse()`.
4. **Validate and checksum all addresses with `viem.getAddress()` at ingress and egress.**
5. **Import env vars from `src/env.ts` only.** Never `process.env` directly.

### The Startup Sequence

```
Next.js starts
  → instrumentation.ts (register())
    → runStartup()
      → runMigrations()      (Drizzle applies pending SQL migrations)
      → loadChainConfig()    (reads config/chain.json)
      → fetchRpcChainId()    (viem call to RPC_URL)
      → assertChainIdMatch() (process.exit(1) on mismatch)
```

Any failure in startup exits the process immediately. Fail fast, clear error, no silent broken state.

### API Security Model

All `/api/*` routes require `X-API-Key: <API_SECRET>` header **except** `/api/health`. The middleware uses a manual constant-time comparison to prevent timing attacks (Edge Runtime doesn't have `crypto.timingSafeEqual`).

### Response Shape Contract

Every API response looks like one of:
```json
{ "ok": true, "data": { ... } }
{ "ok": false, "error": { "code": "SOME_CODE", "message": "..." } }
```

Use `apiResponse()` and `apiError()` from `src/lib/json.ts`. Never call `NextResponse.json()` directly in domain code.

---

## Key Files Quick Reference

| File | What It Does |
|------|-------------|
| `/src/env.ts` | Single source of truth for all env vars. Always import from here. |
| `/src/middleware.ts` | API auth gate. Runs on every `/api/*` request. |
| `/src/lib/errors.ts` | All error code constants. Add new ones here. |
| `/src/lib/json.ts` | `apiResponse()` / `apiError()` — use for all API responses. |
| `/src/lib/startup.ts` | Boot sequence: migrations + chain ID validation. |
| `/src/lib/db/schema.ts` | Drizzle schema. Only table so far: `system_config` (key/value). |
| `/src/lib/db/migrate.ts` | Runs Drizzle migrations from `src/lib/db/migrations/`. |
| `/src/lib/chain-config.ts` | Loads and validates `config/chain.json`. |
| `/src/lib/rpc-chain.ts` | Fetches chain ID from RPC; compares to config. |
| `/src/lib/logger.ts` | Pino logger singleton. Redacts `privateKey`, `mnemonic`, etc. |
| `/config/chain.json` | Chain ID config. Default: `{ "chainId": 1, "name": "Ethereum Mainnet" }`. |
| `/AGENTS.md` | Rules for coding agents. Useful quick-reference for you too. |

---

## Tech Stack

| Concern | Choice |
|---------|--------|
| Framework | Next.js 16, App Router |
| Language | TypeScript (strict) |
| Styling | Tailwind CSS v4 |
| Testing | Vitest |
| Linting | ESLint + custom `no-restricted-imports` |
| Formatting | Prettier |
| EVM library | viem v2 |
| DB | better-sqlite3 + Drizzle ORM |
| Logging | Pino |
| Validation | Zod (everywhere) |
| LLM (planned) | Claude via Anthropic, Vercel AI SDK |
| Key mgmt (planned) | @ethereumjs/wallet v10, two-file keystore |
| Simulation (planned) | Anvil via prool |
| Swaps (planned) | Li.Fi + 1inch fallback |
| Scheduler (planned) | croner |
| Container | Docker multi-stage + docker-compose |

---

## How to Run Locally

```bash
pnpm install
cp .env.example .env
# Fill in: RPC_URL, LLM_API_KEY, ETHERSCAN_API_KEY, API_SECRET, DATA_DIR (absolute path)
# config/chain.json chainId must match your RPC_URL's chain (default: 1 = mainnet)
pnpm dev
```

Quality checks:
```bash
pnpm lint && pnpm format:check && pnpm typecheck && pnpm test
```

Docker:
```bash
docker compose up --build
curl -s http://localhost:3000/api/health  # {"ok":true,"data":{"status":"ok"}}
```

---

## Gotchas to Know Now

1. **`DATA_DIR` must be an absolute path.** Relative paths are rejected at startup — intentional.
2. **The Dockerfile uses `ARG` (not `ENV`) for build-time secrets** to prevent them leaking into Docker layer history.
3. **`system_config` is the persistence home base.** Planned: `onboarding_complete` flag, strategy paused state, deployer preferences. New persistent config goes here first.
4. **`src/core/` doesn't exist yet** — it's the destination for all agent/key/simulation/swap logic. It must never import from `next/*` or `react`.
5. **The wallet password is never stored anywhere.** Prompted at runtime only. Hard security requirement.
6. **Transaction immutability is non-negotiable.** Simulated tx object = signed tx object = broadcast tx object. No reconstruction allowed.

---

## What's Coming Next

- **Stories 1.2–1.4:** Key onboarding (`@ethereumjs/wallet`, two-file keystore)
- **Epic 2:** Web chat UI shell, wallet read tools, AI agent core with streaming, CLI
- **Epic 3:** Full transaction loop — construction, Anvil simulation, broadcast
- **Epic 4:** Swaps via Li.Fi / 1inch
- **Epic 5:** Autonomous DCA/rebalancing strategies

The full planning context is in `_bmad-output/planning-artifacts/` — architecture doc is the most valuable deep read.
