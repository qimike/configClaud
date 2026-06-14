# Personal (user-scoped) MCP configuration example

The project ships a **project-scoped** MCP server in `.mcp.json` (committed to the
repo). Individual developers can *also* configure **user-scoped** MCP servers in
their personal `~/.claude.json`. This file is **not** committed — it lives in the
user's home directory and applies to every project they open.

## Example `~/.claude.json`

```json
{
  "mcpServers": {
    "experimental-notes": {
      "command": "npx",
      "args": [
        "-y",
        "@example/mcp-server-notes"
      ],
      "env": {
        "NOTES_API_KEY": "${NOTES_API_KEY}"
      }
    }
  }
}
```

`experimental-notes` is an example **experimental** server one engineer might be
trying out. Because it lives in their personal config, it does not affect
teammates and is not part of the repository.

> Like `.mcp.json`, the user config uses **environment variable expansion**
> (`${NOTES_API_KEY}`) so no secret is written into the file itself.

## Project-scoped vs. user-scoped MCP

| | Project-scoped (`.mcp.json`) | User-scoped (`~/.claude.json`) |
| --- | --- | --- |
| **Location** | Repo root, committed | Home directory, not committed |
| **Who gets it** | Everyone who clones the repo | Only that one developer, in every project |
| **Use for** | Servers the whole team needs (e.g. `github`) | Personal/experimental servers |
| **Versioned** | Yes | No |

## How both become available simultaneously

When Claude Code starts a session, it **merges** MCP servers from all scopes into a
single registry:

1. **User scope** — servers from `~/.claude.json`.
2. **Project scope** — servers from the repo's `.mcp.json`.

Both sets of servers are loaded and exposed as tools in the *same* session. So a
developer working in this project would have **both** the shared `github` server
(from `.mcp.json`) **and** their personal `experimental-notes` server (from
`~/.claude.json`) available at once. If two scopes define a server with the same
name, the more specific (project) scope takes precedence; otherwise the sets are
simply combined.
