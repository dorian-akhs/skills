# Baseline response — Eval 2: quiz-author

> User: "I built this project myself 6 months ago, barely remember how it works. Quiz me hard on the architecture."

---

I've read every file. Ten questions, no hand-holding. Answer from memory.

---

**Q1 — Startup sequence**

When the Next.js server boots (Node.js runtime only), what is the exact sequence of operations `runStartup()` performs, and what happens if any step fails?

---

**Q2 — Chain ID validation**

You have two sources of chain ID at runtime. Name them both. What data type does each use to represent the chain ID? What is the exact error message format when they don't match?

---

**Q3 — Env validation design**

`src/env.ts` exports both a `getEnv()` function and an `env` object. What is the architectural difference between them? Why does the file derive `REQUIRED_KEYS` from `requiredFieldsSchema.shape` instead of maintaining a separate constant array?

---

**Q4 — Middleware auth**

The middleware uses a hand-rolled `timingSafeEqual` instead of Node's built-in `crypto.timingSafeEqual`. Why? What constraint makes the built-in unavailable here, and how does your implementation handle strings of different lengths?

---

**Q5 — Database**

How many tables does the Drizzle schema define? Name the table and all its columns with their types. Where does the SQLite file live at runtime, and which env variable controls its location?

---

**Q6 — Migration connection lifecycle**

`runMigrations()` closes the SQLite connection in a `finally` block. Why `finally` specifically, and what would go wrong if it were placed after the `migrate()` call instead?

---

**Q7 — Docker build secret handling**

The Dockerfile uses `ARG` instead of `ENV` for the five sensitive build-time variables. Why does that matter for security? What placeholder value is used for `RPC_URL` during the build?

---

**Q8 — Next.js standalone output**

`next.config.ts` sets `output: "standalone"` and adds `better-sqlite3` to `serverExternalPackages`. What does each setting do, and why does `better-sqlite3` specifically need to be listed there?

---

**Q9 — Auth bypass**

One API route skips the `X-API-Key` check entirely. Which one, how is the bypass implemented at the middleware level, and why is that architecturally safe?

---

**Q10 — Logger redaction**

List every field path the pino logger redacts. The config includes both bare names (like `password`) and `**`-prefixed versions (like `**.password`). What is the practical difference between them — what does the bare name cover that `**` doesn't, or vice versa?

---

Answer whatever you can. I'll tell you exactly what you got right, what you got wrong, and what the code actually does.
