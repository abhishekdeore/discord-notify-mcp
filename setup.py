#!/usr/bin/env python3
"""
One-click setup for the Discord Notify MCP connector.

Run this once and it handles everything:
  1. Collects your Discord bot token and channel ID
  2. Creates your .env file
  3. Installs Python dependencies
  4. Registers the MCP connector with Claude
  5. Tells you to restart Claude

Usage:
    python setup.py
"""

import json
import os
import platform
import subprocess
import sys
from pathlib import Path

SERVER_NAME = "discord-notify"


def print_step(n, msg):
    print(f"\n[{n}] {msg}")

def print_ok(msg):
    print(f"    ✅ {msg}")

def print_err(msg):
    print(f"    ❌ {msg}")

def print_info(msg):
    print(f"    ℹ  {msg}")


# ── Step 1: Find server.py ────────────────────────────────────
print_step(1, "Locating server.py...")
script_dir  = Path(__file__).parent.resolve()
server_path = script_dir / "server.py"

if not server_path.exists():
    print_err(f"server.py not found at {server_path}")
    print_info("Make sure setup.py is inside the discord-notify-mcp folder.")
    sys.exit(1)

print_ok(f"Found: {server_path}")


# ── Step 2: Collect credentials ───────────────────────────────
print_step(2, "Collecting your Discord credentials...")
print()
print("    If you don't have these yet, follow the README:")
print("    https://github.com/abhishekdeore/discord-notify-mcp#readme")
print()

bot_token = input("    Enter your Discord Bot Token: ").strip()
if not bot_token:
    print_err("Bot token is required. See the README for how to get one.")
    sys.exit(1)

channel_id = input("    Enter your default Channel ID: ").strip()
if not channel_id:
    print_err("Channel ID is required. See the README for how to get one.")
    sys.exit(1)

print_ok("Credentials collected.")


# ── Step 3: Create .env file ─────────────────────────────────
print_step(3, "Creating .env file...")
env_path = script_dir / ".env"

if env_path.exists():
    overwrite = input("    .env already exists. Overwrite? (y/N): ").strip().lower()
    if overwrite != "y":
        print_info("Keeping existing .env file.")
    else:
        env_path.write_text(
            f"DISCORD_BOT_TOKEN={bot_token}\n"
            f"DISCORD_DEFAULT_CHANNEL={channel_id}\n"
        )
        print_ok(f"Updated: {env_path}")
else:
    env_path.write_text(
        f"DISCORD_BOT_TOKEN={bot_token}\n"
        f"DISCORD_DEFAULT_CHANNEL={channel_id}\n"
    )
    print_ok(f"Created: {env_path}")


# ── Step 4: Install dependencies ─────────────────────────────
print_step(4, "Installing Python dependencies...")
packages = ["mcp[cli]", "httpx", "pydantic", "python-dotenv"]

try:
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "--quiet"] + packages
    )
    print_ok("Dependencies installed: " + ", ".join(packages))
except subprocess.CalledProcessError:
    print_err("pip install failed. Try running manually:")
    print_info(f"  pip install {' '.join(packages)}")
    sys.exit(1)


# ── Step 5: Find Claude config file ──────────────────────────
print_step(5, "Finding Claude config file...")
system = platform.system()

if system == "Darwin":  # macOS
    config_paths = [
        Path.home() / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json",
        Path.home() / ".claude" / "claude_desktop_config.json",
    ]
elif system == "Windows":
    appdata = Path(os.environ.get("APPDATA", ""))
    config_paths = [
        appdata / "Claude" / "claude_desktop_config.json",
        Path.home() / ".claude" / "claude_desktop_config.json",
    ]
else:  # Linux
    config_paths = [
        Path.home() / ".claude" / "claude_desktop_config.json",
        Path.home() / ".config" / "Claude" / "claude_desktop_config.json",
    ]

config_path = None
for path in config_paths:
    if path.exists():
        config_path = path
        print_ok(f"Found existing config: {config_path}")
        break

if config_path is None:
    config_path = config_paths[0]
    config_path.parent.mkdir(parents=True, exist_ok=True)
    print_info(f"No config found. Creating new one at: {config_path}")


# ── Step 6: Read existing config ─────────────────────────────
print_step(6, "Reading existing Claude config...")
if config_path.exists():
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        print_ok("Existing config loaded.")
    except json.JSONDecodeError:
        print_err("Config file has invalid JSON. Backing it up and starting fresh.")
        backup = config_path.with_suffix(".json.bak")
        config_path.rename(backup)
        print_info(f"Backup saved to: {backup}")
        config = {}
else:
    config = {}
    print_info("Starting with a fresh config.")


# ── Step 7: Add/update the MCP server entry ───────────────────
print_step(7, "Registering Discord Notify MCP connector...")

if "mcpServers" not in config:
    config["mcpServers"] = {}

config["mcpServers"][SERVER_NAME] = {
    "command": sys.executable,
    "args": [str(server_path)],
    "env": {
        "DISCORD_BOT_TOKEN": bot_token,
        "DISCORD_DEFAULT_CHANNEL": channel_id,
    }
}

with open(config_path, "w", encoding="utf-8") as f:
    json.dump(config, f, indent=2)

print_ok(f"Connector '{SERVER_NAME}' registered in: {config_path}")
print_info(f"Python:    {sys.executable}")
print_info(f"Server:    {server_path}")
print_info(f"Channel:   {channel_id}")


# ── Done ──────────────────────────────────────────────────────
print("\n" + "─" * 55)
print("  Setup complete!")
print("─" * 55)
print("\n  Next steps:")
print("    1. Fully quit and reopen Claude Desktop")
print("    2. Ask Claude to post something to Discord")
print()
