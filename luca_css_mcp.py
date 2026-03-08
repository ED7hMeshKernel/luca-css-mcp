"""
LUCA CSS MCP Client v1.0 — MCP server exposing LUCA CSS Engine tools to Claude Code.

3 tools: css_compile, css_preflight, css_scan
Single file, single dependency (httpx). Communicates with LUCA CSS API server.

Config: ~/.luca/config.json → {"api_url": "https://synthetic-context.net/css/api", "api_key": null}

Usage:
  claude_desktop_config.json:
    {"mcpServers": {"luca-css": {"command": "python3", "args": ["/path/to/luca_css_mcp.py"]}}}
"""

import json
import sys
import os
import httpx

# === Config ===

DEFAULT_API_URL = "https://synthetic-context.net/css/api"
CONFIG_PATH = os.path.expanduser("~/.luca/config.json")


def load_config() -> dict:
    try:
        with open(CONFIG_PATH) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def get_api_url() -> str:
    return load_config().get("api_url", os.environ.get("LUCA_API_URL", DEFAULT_API_URL))


def get_api_key() -> str | None:
    return load_config().get("api_key", os.environ.get("LUCA_API_KEY"))


# === MCP Protocol (stdio JSON-RPC) ===

TOOLS = [
    {
        "name": "css_compile",
        "description": "Compile a CSS profile (dashboard, vitrine, ecommerce). Returns production-ready CSS with validation. Optionally override defaults (vars, font, colors).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "profile": {
                    "type": "string",
                    "enum": ["dashboard", "vitrine", "ecommerce"],
                    "description": "CSS profile to compile",
                },
                "overrides": {
                    "type": "object",
                    "description": "Optional overrides for profile defaults (e.g. {\"vars\": {\"--gold\": \"#ff0\"}})",
                },
            },
            "required": ["profile"],
        },
    },
    {
        "name": "css_preflight",
        "description": "Get anti-patterns (pathogens) to avoid and axioms to follow before writing code in a given language. Call this BEFORE coding.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "lang": {
                    "type": "string",
                    "enum": ["css", "js", "html", "bash", "python", "powershell", "network"],
                    "description": "Programming language",
                },
                "context": {
                    "type": "string",
                    "description": "Brief description of what you're about to code",
                },
            },
            "required": ["lang"],
        },
    },
    {
        "name": "css_scan",
        "description": "Scan source code for known anti-patterns and bugs. Returns infections (critical/high) and warnings (medium/low). Call this AFTER writing code.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "Source code to scan",
                },
                "lang": {
                    "type": "string",
                    "enum": ["css", "js", "html", "bash", "python", "powershell", "network"],
                    "description": "Language of the code",
                },
            },
            "required": ["code", "lang"],
        },
    },
]


def api_call(endpoint: str, payload: dict) -> dict:
    """Call the LUCA CSS API."""
    url = get_api_url().rstrip("/") + "/" + endpoint
    headers = {"Content-Type": "application/json", "User-Agent": "luca-css-mcp/1.0"}
    key = get_api_key()
    if key:
        headers["X-Luca-Key"] = key
    try:
        resp = httpx.post(url, json=payload, headers=headers, timeout=30)
        resp.raise_for_status()
        return resp.json()
    except httpx.HTTPStatusError as e:
        return {"error": f"HTTP {e.response.status_code}", "detail": e.response.text[:500]}
    except httpx.ConnectError:
        return {"error": "connection_failed", "detail": f"Cannot reach {url}"}
    except Exception as e:
        return {"error": "request_failed", "detail": str(e)[:500]}


def handle_tool_call(name: str, args: dict) -> dict:
    """Route tool call to API endpoint."""
    if name == "css_compile":
        return api_call("compile", {"profile": args["profile"], "overrides": args.get("overrides")})
    elif name == "css_preflight":
        return api_call("preflight", {"lang": args["lang"], "context": args.get("context", "")})
    elif name == "css_scan":
        return api_call("scan", {"code": args["code"], "lang": args["lang"]})
    else:
        return {"error": f"Unknown tool: {name}"}


def handle_message(msg: dict) -> dict | None:
    """Handle a JSON-RPC message."""
    method = msg.get("method", "")
    msg_id = msg.get("id")

    if method == "initialize":
        return {
            "jsonrpc": "2.0", "id": msg_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {"name": "luca-css", "version": "1.0"},
            },
        }

    elif method == "notifications/initialized":
        return None  # notification, no response

    elif method == "tools/list":
        return {"jsonrpc": "2.0", "id": msg_id, "result": {"tools": TOOLS}}

    elif method == "tools/call":
        params = msg.get("params", {})
        tool_name = params.get("name", "")
        tool_args = params.get("arguments", {})
        result = handle_tool_call(tool_name, tool_args)
        text = json.dumps(result, indent=2, ensure_ascii=False)
        return {
            "jsonrpc": "2.0", "id": msg_id,
            "result": {"content": [{"type": "text", "text": text}]},
        }

    elif method == "ping":
        return {"jsonrpc": "2.0", "id": msg_id, "result": {}}

    else:
        return {
            "jsonrpc": "2.0", "id": msg_id,
            "error": {"code": -32601, "message": f"Method not found: {method}"},
        }


def main():
    """Run MCP server on stdio."""
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue
        response = handle_message(msg)
        if response is not None:
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
