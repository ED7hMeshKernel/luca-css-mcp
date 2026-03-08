# LUCA CSS — MCP Server for AI Coding Agents

**Biological CSS immunity for AI agents.** LUCA scans your code for silent bugs that browsers never report — before you deploy.

61 pathogens across 7 languages. 12 axioms. 3 compiled CSS profiles. Built from 130+ real bugs across 40+ sessions.

## What it does

| Tool | When | What |
|------|------|------|
| `css_preflight` | **Before** coding | Get pathogens to avoid + axioms for your language |
| `css_scan` | **After** coding | Scan for infections (critical/high) and warnings |
| `css_compile` | **Anytime** | Compile production-ready CSS (dashboard, vitrine, ecommerce) |

## Quick start

### 1. Install

```bash
pip install httpx
```

### 2. Configure your MCP client

Add to your MCP settings:

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

- *"Preflight CSS for a dark dashboard with hover animations"*
- *"Scan this code for anti-patterns"*
- *"Compile a vitrine CSS profile"*

## What LUCA catches

Real bugs that AI generates and browsers silently accept:

| ID | Bug | Impact |
|----|-----|--------|
| CSS_001 | `var()` used before `:root` declaration | Element renders without color |
| CSS_002 | Empty `grid-template-columns` from unresolved template | Layout breaks completely |
| CSS_004 | `transition: all` on hover with layout changes | 60fps reflows, janky UI |
| CSS_007 | `calc(100%-20px)` without spaces | Silently ignored by browser |
| CSS_008 | `@keyframes` animating `width`/`height` | Reflow every frame, 10fps |
| CSS_009 | `will-change` on many elements | GPU memory exhaustion |
| CSS_010 | `@property` without `syntax` field | Browser ignores registration |
| CSS_011 | `contain: strict` on scrollable content | Breaks scroll and overflow |

Plus 53 more across Python, Bash, JavaScript, HTML, PowerShell, and Network.

## Example: scan result

```bash
curl -s -X POST https://synthetic-context.net/css/api/scan \
  -H "Content-Type: application/json" \
  -d '{"code": ".sidebar { transition: all 0.3s; } @keyframes grow { from { width: 0 } to { width: 100% } }", "lang": "css"}'
```

```json
{
  "infections": [
    {
      "id": "CSS_008",
      "title": "Layout-triggering property in animation — causes reflow every frame",
      "severity": "high",
      "fix": "Replace width/height with transform: scale(). Only animate transform and opacity for 60fps."
    }
  ],
  "warnings": [
    {
      "id": "CSS_004",
      "title": "transition:all on components with layout-changing hover",
      "severity": "medium",
      "fix": "Specify exact properties: transition: transform 0.2s, box-shadow 0.2s."
    }
  ],
  "clean": false
}
```

## API

Public API at `https://synthetic-context.net/css/api/`:

| Endpoint | Method | Description | Rate |
|----------|--------|-------------|------|
| `/compile` | POST | Compile CSS profile | 30/min |
| `/preflight` | POST | Pre-flight pathogen check | 30/min |
| `/scan` | POST | Scan code for anti-patterns | 30/min |
| `/health` | GET | Engine status + stats | 30/min |

Free. No signup. No API key required.

## Configuration

Optional config file at `~/.luca/config.json`:

```json
{
  "api_url": "https://synthetic-context.net/css/api",
  "api_key": null
}
```

## How it works

LUCA (Last Universal Common Ancestor) uses a biological model:

- **Genome** — CSS DNA: codons, profiles, design patterns
- **Ribosome** — Compiler: genome + profile = production CSS
- **Membrane** — Validator: rejects invalid output before it ships
- **Pathogen DB** — Immune memory: 61 real bugs that must never recur

Every pathogen comes from a real production incident. Not theory — lived experience across 40+ sessions.

## Architecture

```
AI Agent ──→ MCP Client (this repo) ──→ LUCA API (server)
               luca_css_mcp.py              synthetic-context.net
               3 tools exposed              engine stays private
               httpx only                   source never exposed
```

The engine source code never leaves the server. You receive compiled CSS and scan results only.

## License

MIT — Client (this file) is open source.
Engine is proprietary (ECOBIO micro-enterprise).
