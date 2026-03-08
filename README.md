# LUCA — Immune System for Code

Your body has an immune system that recognizes viruses before they make you sick.
LUCA does the same for your code: **79 known pathogens** across 7 languages,
caught before they break your production.

Built from **130+ real bugs** across 40+ coding sessions. Not theory — lived experience.

## What it catches

Silent bugs that AI generates and browsers/runtimes never report:

| ID | Lang | Sev | What goes wrong |
|----|------|:---:|-----------------|
| CSS_001 | CSS | critical | `var()` used before `:root` declaration — element renders without color |
| CSS_007 | CSS | high | `calc(100%-20px)` missing spaces — silently ignored by browser |
| JS_001 | JS | critical | `const`/`let` used before declaration in same scope |
| JS_002 | JS | high | Multiple `setInterval` polls without mutex — race condition |
| HTML_005 | HTML | critical | `innerHTML` with user input — XSS (CWE-79) |
| PY_001 | Python | critical | Wrong port number for service — silent connection failure |
| PY_017 | Python | critical | `render_template_string` with user input — SSTI (CWE-1336) |
| BASH_001 | Bash | critical | `pgrep` pattern doesn't match actual process name |
| PS_001 | PowerShell | high | BOM + CRLF encoding when writing PS1 from Linux |
| NET_002 | Network | critical | Service port exposed to entire internet (`from any`) |

Plus 69 more. Every pathogen has a fix, a severity, and most have a CWE reference.

## Quick start

### 1. Install

```bash
pip install httpx
```

### 2. Configure your MCP client

Add to your MCP settings (Claude Code, Cursor, etc.):

```json
{
  "mcpServers": {
    "luca-css": {
      "command": "python3",
      "args": ["/path/to/luca_css_mcp.py"]
    }
  }
}
```

### 3. Use

| Tool | When | What |
|------|------|------|
| `css_preflight` | **Before** coding | Get pathogens to avoid + axioms for your language |
| `css_scan` | **After** coding | Scan for infections (critical/high) and warnings |
| `css_compile` | **Anytime** | Compile production-ready CSS (dashboard, vitrine, ecommerce) |

- *"Preflight CSS for a dark dashboard"*
- *"Scan this Python code for anti-patterns"*
- *"Compile a vitrine CSS profile"*

## Scanner Web

Try it without installing anything:

**[synthetic-context.net/css/](https://synthetic-context.net/css/)**

Paste code, pick a language, hit Scan. Results in seconds.

## How it works

```
                    ┌──────────────────────────┐
                    │     LUCA Engine (BSD)     │
 Your code ──→ MCP │  Genome    → CSS DNA      │ ──→ Results only
   or curl     or  │  Ribosome  → Compiler     │     (no source
               Web │  Membrane  → Validator    │      ever leaves
                UI │  Pathogen  → 79 known bugs│      the server)
                    │  Thymus    → Adaptive sel.│
                    └──────────────────────────┘
```

**LUCA** (Last Universal Common Ancestor) uses a biological model:

- **Genome** — CSS DNA: codons, profiles, design patterns
- **Ribosome** — Compiler: genome + context = production CSS
- **Membrane** — Validator: rejects invalid output before it ships
- **Pathogen DB** — Immune memory: 79 real bugs that must never recur
- **Thymus** — Adaptive selection: filters pathogens by your tech stack
- **Marrow** — Self-improvement: adversarial testing → gap detection → human-approved new pathogens

## API Reference

Public API at `https://synthetic-context.net/css/api/` — free, no signup, no API key.

### POST `/scan`

Scan code for infections and warnings.

```bash
curl -s -X POST https://synthetic-context.net/css/api/scan \
  -H "Content-Type: application/json" \
  -d '{"code": "eval \"$CMD\"", "lang": "bash"}'
```

```json
{
  "infections": [
    {
      "id": "BASH_016",
      "title": "eval with variable expansion — arbitrary command execution",
      "severity": "critical",
      "fix": "Use arrays and direct execution instead of eval.",
      "cwe": "CWE-78"
    }
  ],
  "warnings": [],
  "clean": false
}
```

### POST `/preflight`

Get pathogens to avoid before writing code.

```bash
curl -s -X POST https://synthetic-context.net/css/api/preflight \
  -H "Content-Type: application/json" \
  -d '{"lang": "css", "context": "dark dashboard with hover animations"}'
```

### POST `/compile`

Compile a CSS profile (dashboard, vitrine, ecommerce).

```bash
curl -s -X POST https://synthetic-context.net/css/api/compile \
  -H "Content-Type: application/json" \
  -d '{"profile": "dashboard"}'
```

### GET `/health`

```bash
curl -s https://synthetic-context.net/css/api/health | jq .
```

| Field | Example |
|-------|---------|
| `pathogens` | 79 |
| `languages` | 7 |
| `axioms` | 12 |
| `profiles` | 3 |

Rate limit: 30 requests/min per IP.

## Languages

| Language | Pathogens | Focus |
|----------|:---------:|-------|
| Python | 20 | SSTI, eval, path traversal, encoding, imports |
| Bash | 16 | pgrep, grep patterns, unquoted vars, eval, pipes |
| CSS | 13 | var() order, calc(), transitions, animations, GPU |
| Network | 11 | PF rules, port exposure, DNS, firewall misconfig |
| JavaScript | 8 | scope, race conditions, DOM, event listeners |
| HTML | 6 | XSS, route order, meta tags, form security |
| PowerShell | 5 | encoding, paths, execution policy, credentials |

12 cross-language **axioms** (universal rules that apply regardless of language).

## Philosophy

- **Zero false positives > catch everything.** Every pathogen proven on real code.
- **Human in the loop.** Preflight before coding, scan after. You decide what to fix.
- **Static analysis only.** No runtime, no sandbox, no data collection. Fast and non-intrusive.
- **Built from real bugs.** 130+ bugs from 40+ sessions, not academic theory.

## Configuration

Optional config file at `~/.luca/config.json`:

```json
{
  "api_url": "https://synthetic-context.net/css/api",
  "api_key": null
}
```

## Architecture

```
AI Agent ──→ MCP Client (this repo) ──→ LUCA API (server)
               luca_css_mcp.py              synthetic-context.net
               3 tools exposed              engine stays private
               httpx only                   source never exposed
```

The engine source code never leaves the server. You receive scan results and compiled CSS only.

## Stats

| Metric | Value |
|--------|------:|
| Pathogens | 79 |
| Languages | 7 |
| Axioms | 12 |
| CSS profiles | 3 |
| Test suite | 1305 tests |
| False positives | 0 (by design) |

## License

**MIT** — Client (`luca_css_mcp.py`) is open source.
Engine is proprietary (ECOBIO micro-enterprise).
