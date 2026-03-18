#!/usr/bin/env python3
"""
MCP Server — Discord Notify

Allows Claude to send messages, embeds, and formatted updates to any
channel on your Discord server using a bot token.

Environment Variables (set in .env):
    DISCORD_BOT_TOKEN       - Your bot token from discord.com/developers
    DISCORD_DEFAULT_CHANNEL - Default channel ID to post to (e.g. your #general)
"""

import json
import os
import sys
from typing import Optional

import httpx
from dotenv import load_dotenv
from pydantic import BaseModel, Field, ConfigDict
from mcp.server.fastmcp import FastMCP

# ──────────────────────────────────────────────
# Bootstrap
# ──────────────────────────────────────────────
load_dotenv()

DISCORD_BOT_TOKEN       = os.getenv("DISCORD_BOT_TOKEN", "")
DISCORD_DEFAULT_CHANNEL = os.getenv("DISCORD_DEFAULT_CHANNEL", "")
DISCORD_API_BASE        = "https://discord.com/api/v10"

if not DISCORD_BOT_TOKEN:
    print(
        "ERROR: DISCORD_BOT_TOKEN is not set.\n"
        "  Copy .env.example → .env and fill in your bot token.",
        file=sys.stderr,
    )
    sys.exit(1)

mcp = FastMCP("discord_notify_mcp")


# ──────────────────────────────────────────────
# HTTP helper
# ──────────────────────────────────────────────

def _headers() -> dict:
    return {
        "Authorization": f"Bot {DISCORD_BOT_TOKEN}",
        "Content-Type": "application/json",
    }


async def _request(
    method: str,
    path: str,
    *,
    json_body: Optional[dict] = None,
    expect_json: bool = True,
) -> dict | list | None:
    url = f"{DISCORD_API_BASE}{path}"
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.request(method, url, headers=_headers(), json=json_body)
            resp.raise_for_status()
            if expect_json and resp.content:
                return resp.json()
            return None
    except httpx.HTTPStatusError as e:
        status = e.response.status_code
        try:
            detail = e.response.json()
        except Exception:
            detail = e.response.text
        if status == 401:
            raise RuntimeError("Invalid bot token. Double-check DISCORD_BOT_TOKEN in your .env file.")
        if status == 403:
            raise RuntimeError(
                "Bot doesn't have permission to post in that channel. "
                "Make sure the bot has the 'Send Messages' permission."
            )
        if status == 404:
            raise RuntimeError(
                "Channel not found. Double-check the channel ID. "
                "Make sure Developer Mode is on in Discord settings."
            )
        if status == 429:
            retry_after = e.response.json().get("retry_after", "a few seconds")
            raise RuntimeError(f"Rate limited by Discord. Try again in {retry_after} seconds.")
        raise RuntimeError(f"Discord API error {status}: {detail}")
    except httpx.ConnectError:
        raise RuntimeError("Cannot reach Discord API. Check your internet connection.")
    except httpx.TimeoutException:
        raise RuntimeError("Request to Discord timed out. Please try again.")


def _resolve_channel(channel_id: Optional[str]) -> str:
    """Use provided channel ID, or fall back to the default from .env."""
    cid = channel_id or DISCORD_DEFAULT_CHANNEL
    if not cid:
        raise RuntimeError(
            "No channel ID provided and DISCORD_DEFAULT_CHANNEL is not set in .env. "
            "Pass a channel_id explicitly or set the default in your .env file."
        )
    return cid


def _ok(data, message: str) -> str:
    return json.dumps({"status": "success", "message": message, "data": data}, indent=2)


def _err(message: str) -> str:
    return json.dumps({"status": "error", "message": message}, indent=2)


# ──────────────────────────────────────────────
# Input models
# ──────────────────────────────────────────────

class SendMessageInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    content: str = Field(
        ...,
        description="The text message to post (up to 2000 characters).",
        min_length=1,
        max_length=2000,
    )
    channel_id: Optional[str] = Field(
        default=None,
        description=(
            "Discord channel ID to post to. "
            "Leave blank to use the default channel set in DISCORD_DEFAULT_CHANNEL. "
            "Right-click any channel in Discord → Copy Channel ID."
        ),
    )


class SendEmbedInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    title: str = Field(
        ...,
        description="Bold title shown at the top of the embed card.",
        min_length=1,
        max_length=256,
    )
    description: str = Field(
        ...,
        description="Main body text of the embed (supports markdown). Up to 4096 characters.",
        min_length=1,
        max_length=4096,
    )
    color: Optional[int] = Field(
        default=0x5865F2,
        description=(
            "Sidebar color as a decimal integer. "
            "Examples: 5865202 (Discord blurple), 3066993 (green), 15158332 (red), "
            "16776960 (yellow), 0 (black/no color)."
        ),
    )
    footer: Optional[str] = Field(
        default=None,
        description="Small footer text at the bottom of the embed (e.g. 'Sent by Claude').",
        max_length=2048,
    )
    channel_id: Optional[str] = Field(
        default=None,
        description="Discord channel ID. Leave blank to use the default channel.",
    )


class SendReportInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    headline: str = Field(
        ...,
        description="Short headline for the report (shown as embed title).",
        min_length=1,
        max_length=256,
    )
    summary: str = Field(
        ...,
        description="A brief 1-2 sentence summary shown in the embed description.",
        min_length=1,
        max_length=500,
    )
    body: str = Field(
        ...,
        description="The full report content. Supports Discord markdown (**, *, __, ~~, `, ```).",
        min_length=1,
        max_length=3500,
    )
    color: Optional[int] = Field(
        default=0x57F287,
        description="Sidebar color. Default is green (5764487). Use red (15158332) for alerts.",
    )
    channel_id: Optional[str] = Field(
        default=None,
        description="Discord channel ID. Leave blank to use the default channel.",
    )


class GetChannelInfoInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    channel_id: Optional[str] = Field(
        default=None,
        description="Discord channel ID to look up. Leave blank to check the default channel.",
    )


class ListChannelsInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    server_id: str = Field(
        ...,
        description=(
            "Discord server (guild) ID. Right-click your server icon → Copy Server ID. "
            "Requires Developer Mode to be on in Discord settings."
        ),
        min_length=1,
    )


# ──────────────────────────────────────────────
# Tools
# ──────────────────────────────────────────────

@mcp.tool(
    name="discord_send_message",
    annotations={
        "title": "Send Discord Message",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    },
)
async def discord_send_message(params: SendMessageInput) -> str:
    """
    Post a plain text message to a Discord channel.

    Sends a simple text message to the specified channel (or the default
    channel if none is provided). Great for quick updates, confirmations,
    or short notifications.

    Args:
        params (SendMessageInput):
            - content (str): The message text (up to 2000 characters, markdown supported)
            - channel_id (Optional[str]): Target channel ID (uses default if omitted)

    Returns:
        str: JSON with the sent message ID and channel details.

    Examples:
        - "Send me a message on Discord" → content='Your update is ready.'
        - "Post a quick note to my server" → content='...', channel_id='...'
    """
    try:
        channel = _resolve_channel(params.channel_id)
        result = await _request(
            "POST",
            f"/channels/{channel}/messages",
            json_body={"content": params.content},
        )
        return _ok(result, f"Message posted to channel {channel}. Message ID: {result.get('id')}.")
    except RuntimeError as e:
        return _err(str(e))


@mcp.tool(
    name="discord_send_embed",
    annotations={
        "title": "Send Discord Embed",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    },
)
async def discord_send_embed(params: SendEmbedInput) -> str:
    """
    Post a formatted embed card to a Discord channel.

    Embeds appear as styled cards with a colored sidebar, bold title, and
    body text. Much more readable than plain text for structured information
    like summaries, status updates, or alerts.

    Args:
        params (SendEmbedInput):
            - title (str): Bold title at the top of the card
            - description (str): Main body text (markdown supported)
            - color (Optional[int]): Sidebar color as decimal (default: Discord blurple)
            - footer (Optional[str]): Small text at the bottom
            - channel_id (Optional[str]): Target channel (uses default if omitted)

    Returns:
        str: JSON with the sent message ID.

    Examples:
        - "Send a formatted update to Discord" → title='Update', description='...'
        - "Post an alert card to my server" → title='Alert', color=15158332, description='...'
    """
    try:
        channel = _resolve_channel(params.channel_id)
        embed = {
            "title": params.title,
            "description": params.description,
            "color": params.color or 0x5865F2,
        }
        if params.footer:
            embed["footer"] = {"text": params.footer}

        result = await _request(
            "POST",
            f"/channels/{channel}/messages",
            json_body={"embeds": [embed]},
        )
        return _ok(result, f"Embed posted to channel {channel}. Message ID: {result.get('id')}.")
    except RuntimeError as e:
        return _err(str(e))


@mcp.tool(
    name="discord_send_report",
    annotations={
        "title": "Send Formatted Report to Discord",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    },
)
async def discord_send_report(params: SendReportInput) -> str:
    """
    Post a full structured report to Discord as a rich embed.

    Designed for sending detailed analyses, spending summaries, Gmail digests,
    or any multi-section report. The report is formatted as a Discord embed
    with a headline, summary, and full body content.

    Args:
        params (SendReportInput):
            - headline (str): Report title (e.g. 'Monthly Spending Analysis')
            - summary (str): 1-2 sentence overview shown at the top
            - body (str): Full report body (use **bold**, bullet points, etc.)
            - color (Optional[int]): Sidebar color (default: green for reports)
            - channel_id (Optional[str]): Target channel (uses default if omitted)

    Returns:
        str: JSON with the sent message ID.

    Examples:
        - "Send my spending report to Discord" → headline='Spending Report', body='...'
        - "Post a Gmail summary to my server" → headline='Gmail Digest', body='...'
        - "Send me the PayPal analysis on Discord" → headline='PayPal Analysis', body='...'
    """
    try:
        channel = _resolve_channel(params.channel_id)
        embed = {
            "title": params.headline,
            "description": f"_{params.summary}_\n\n{params.body}",
            "color": params.color or 0x57F287,
            "footer": {"text": "Sent by Claude"},
        }
        result = await _request(
            "POST",
            f"/channels/{channel}/messages",
            json_body={"embeds": [embed]},
        )
        return _ok(result, f"Report '{params.headline}' posted to channel {channel}.")
    except RuntimeError as e:
        return _err(str(e))


@mcp.tool(
    name="discord_get_channel_info",
    annotations={
        "title": "Get Discord Channel Info",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def discord_get_channel_info(params: GetChannelInfoInput) -> str:
    """
    Retrieve information about a Discord channel.

    Returns the channel name, type, server ID, and topic. Useful for
    verifying a channel ID is correct before sending messages to it.

    Args:
        params (GetChannelInfoInput):
            - channel_id (Optional[str]): Channel to look up (uses default if omitted)

    Returns:
        str: JSON with channel name, type, guild ID, and topic.

    Examples:
        - "Is my channel ID correct?" → use this tool to verify
        - "What channel am I posting to?" → use this tool
    """
    try:
        channel = _resolve_channel(params.channel_id)
        result = await _request("GET", f"/channels/{channel}")
        name    = result.get("name", "unknown")
        guild   = result.get("guild_id", "DM")
        topic   = result.get("topic", "No topic set")
        return _ok(result, f"Channel: #{name} | Server ID: {guild} | Topic: {topic}")
    except RuntimeError as e:
        return _err(str(e))


@mcp.tool(
    name="discord_list_channels",
    annotations={
        "title": "List Discord Server Channels",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def discord_list_channels(params: ListChannelsInput) -> str:
    """
    List all channels in a Discord server.

    Returns the name and ID of every channel the bot can see. Useful for
    finding the right channel ID to use when sending messages.

    Args:
        params (ListChannelsInput):
            - server_id (str): Your Discord server (guild) ID.
              Right-click the server icon → Copy Server ID (needs Developer Mode on).

    Returns:
        str: JSON array of channels with their IDs, names, and types.

    Examples:
        - "What channels do I have?" → provide server_id
        - "Find the ID for my #general channel" → use this tool
    """
    try:
        result = await _request("GET", f"/guilds/{params.server_id}/channels")
        channels = [
            {"id": c["id"], "name": c.get("name", "unnamed"), "type": c.get("type", 0)}
            for c in (result or [])
            if c.get("type") in (0, 5, 10, 11, 12)  # text, announcement, thread types
        ]
        channels.sort(key=lambda c: c["name"])
        return _ok(channels, f"Found {len(channels)} text channel(s) in server {params.server_id}.")
    except RuntimeError as e:
        return _err(str(e))


# ──────────────────────────────────────────────
# Entry point
# ──────────────────────────────────────────────

if __name__ == "__main__":
    mcp.run()
