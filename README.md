# Discord Notify MCP

Let Claude send messages, reports, and rich embeds directly to your Discord server. No webhooks, no third-party services — just a simple MCP connector and your own Discord bot.

```
You (Claude) → MCP Server → Discord Bot → #your-channel
```

## Quick Start

### Prerequisites

- **Python 3.10+** — [Download](https://www.python.org/downloads/)
- **A Discord server** you own or have admin access to
- **Claude Desktop** — [Download](https://claude.ai/download)

### 1. Create a Discord Bot

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Click **New Application** → name it (e.g. "Claude Bot") → **Create**
3. Go to **Bot** in the sidebar
4. Click **Reset Token** → copy the token and save it somewhere safe
5. Scroll down → enable **Message Content Intent** → **Save Changes**

### 2. Invite the Bot to Your Server

1. Go to **OAuth2 → URL Generator** in the sidebar
2. Under **Scopes**, check `bot`
3. Under **Bot Permissions**, check:
   - `Send Messages`
   - `Embed Links`
   - `Read Message History`
4. Copy the generated URL → open it in your browser → select your server → **Authorize**

### 3. Get Your Channel ID

1. In Discord, go to **Settings → Advanced → Developer Mode → ON**
2. Right-click the channel you want Claude to post to (e.g. `#general`)
3. Click **Copy Channel ID**

### 4. Install & Run Setup

```bash
git clone https://github.com/abhishekdeore/discord-notify-mcp.git
cd discord-notify-mcp

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate        # macOS / Linux
# venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt

# Run the setup wizard
python setup.py
```

The setup wizard will:
- Ask for your bot token and channel ID
- Create your `.env` file
- Register the MCP connector with Claude Desktop

### 5. Restart Claude & Try It

Fully quit and reopen Claude Desktop, then try:

- *"Send a message to my Discord saying hello!"*
- *"Post my spending analysis to Discord"*
- *"Send a formatted report to my Discord server"*

---

## Use Cases & Examples

Not sure what to do with it? Check out the **[Use Cases & Prompt Examples](examples/USE_CASES.md)** — a full guide with ready-to-use prompts for:

- **Personal productivity** — morning briefings, expense tracking, reading lists
- **Developer workflows** — changelogs, incident reports, code review summaries
- **Team collaboration** — meeting notes, standups, weekly digests
- **Multi-MCP pipelines** — Gmail + Calendar + Discord morning dashboards
- **Monitoring & alerts** — server health, security scans, budget burn rate
- **Fun & engagement** — trivia, coding challenges, tech history

---

## Available Tools

| Tool | Description |
|------|-------------|
| `discord_send_message` | Send a plain text message to a channel |
| `discord_send_embed` | Send a styled embed card with title, description, color, and footer |
| `discord_send_report` | Send a formatted report with headline, summary, and body |
| `discord_get_channel_info` | Look up a channel's name, type, and topic |
| `discord_list_channels` | List all text channels in a server |

## What Messages Look Like

**Plain message** (`discord_send_message`):
> Your spending report is ready.

**Report embed** (`discord_send_report`):
```
┌──────────────────────────────────────┐
│  Monthly Spending Analysis           │
│  You spent $1,240 this month.        │
│                                      │
│  **Food & Dining**: $320             │
│  **Subscriptions**: $89              │
│  **Shopping**: $210                  │
│                          Sent by Claude │
└──────────────────────────────────────┘
```

---

## Manual Configuration

If you prefer not to use the setup wizard, you can configure everything manually.

### Create `.env`

```bash
cp .env.example .env
```

Edit `.env` with your values:
```env
DISCORD_BOT_TOKEN=your_bot_token_here
DISCORD_DEFAULT_CHANNEL=your_channel_id_here
```

### Register with Claude Desktop

Add this to your Claude config file:

| OS | Config Location |
|----|----------------|
| macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Windows | `%APPDATA%\Claude\claude_desktop_config.json` |
| Linux | `~/.config/Claude/claude_desktop_config.json` |

```json
{
  "mcpServers": {
    "discord-notify": {
      "command": "/absolute/path/to/discord-notify-mcp/venv/bin/python",
      "args": ["/absolute/path/to/discord-notify-mcp/server.py"],
      "env": {
        "DISCORD_BOT_TOKEN": "your_bot_token_here",
        "DISCORD_DEFAULT_CHANNEL": "your_channel_id_here"
      }
    }
  }
}
```

> Replace the paths with the actual absolute paths on your machine.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `Invalid bot token` | Go to Developer Portal → Bot → **Reset Token** → copy the new one into `.env` |
| `Bot doesn't have permission` | Make sure the bot has **Send Messages** and **Embed Links** permissions in the target channel |
| `Channel not found` | Double-check Developer Mode is on and you copied the correct channel ID |
| Bot shows offline | Normal — the bot only "connects" when the MCP server is running via Claude |
| `mcp` package not found | Make sure you're using Python 3.10+ (`python3 --version`) |
| Setup wizard doesn't detect Claude | Manually add the config using the [Manual Configuration](#manual-configuration) section |

---

## Project Structure

```
discord-notify-mcp/
├── server.py              # MCP server — handles all Discord API communication
├── setup.py               # Interactive setup wizard
├── requirements.txt       # Python dependencies
├── .env.example           # Template for credentials
├── .gitignore             # Keeps secrets and venv out of git
├── LICENSE                # MIT License
├── README.md              # You are here
└── examples/
    └── USE_CASES.md       # Prompt examples and use case ideas
```

---

## License

[MIT](LICENSE)
