Analyze this codebase to generate or update `.github/copilot-instructions.md` — a minimal operational contract that helps AI agents be immediately productive.

**IMPORTANT: Less is more.** Research shows verbose instruction files increase cost (+20%) without improving outcomes, and comprehensive documentation actually degrades performance. Write only what an AI cannot infer from the code itself.

## What to discover and include (in this order):

1. **Required commands** — Build, test, lint, format commands with exact flags. Only include if they differ from framework defaults or aren't obvious from config files (package.json scripts, Makefile targets, pyproject.toml).
2. **Toolchain constraints** — Package manager (uv, pnpm, poetry), runtime version requirements, or non-standard tooling that would cause failures if guessed wrong.
3. **Non-negotiable rules** — Security policies, compliance requirements, mandatory checks before commit/PR, or architectural boundaries that must never be violated. Include the *reason* behind each rule.
4. **Critical pitfalls** — Max 3–5 repo-specific traps that waste significant time if hit. Things that look like they should work one way but don't.
5. **Key conventions that deviate from norms** — Only patterns that differ from standard practice for the language/framework. Skip anything a linter or formatter already enforces.

## What to explicitly EXCLUDE:

- **Repository tours or directory listings** — AI agents navigate codebases through tool use; directory maps add noise without improving navigation.
- **Generic coding advice** — "Write tests," "handle errors," "use meaningful names" — the model already knows this.
- **Content already in README, docs, or docstrings** — Context files that duplicate existing docs hurt performance.
- **Language or framework basics** — Don't explain how Python/React/etc. works.
- **Style guides** — Move to `.instructions.md` files with `applyTo` patterns instead.
- **Framework-specific knowledge** — This belongs in `.instructions.md` files, skills, or `ai_docs`, not in global instructions.

## Process:

1. Source existing AI conventions from `**/{.github/copilot-instructions.md,AGENTS.md,CLAUDE.md,.cursorrules,.windsurfrules,README.md}` (one glob search).
2. Scan build/config files: `**/pyproject.toml`, `**/package.json`, `**/Makefile`, `**/*.toml`, `**/*.yaml` for commands and tooling.
3. Look for non-obvious patterns by sampling 3–5 core source files.
4. If `.github/copilot-instructions.md` exists, preserve content outside `<!-- devagent:start -->` / `<!-- devagent:end -->` markers and merge intelligently.

## Output format:

- **20–40 lines** of markdown (absolute maximum 50). If you need more, the extra content belongs in `.instructions.md` files or skills.
- Use markdown headers to separate sections.
- Include exact commands as code blocks, not prose descriptions.
- Every rule must include a brief *why* (one sentence max).
- No preamble, no "About this file" section — start with actionable content.
- End by asking the user which sections feel incomplete or unnecessary, and whether any critical pitfalls were missed.