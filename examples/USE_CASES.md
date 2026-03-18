# Use Cases & Prompt Examples

Real-world ways to use Discord Notify MCP — from simple daily updates to advanced multi-MCP pipelines.

Each section includes **ready-to-use prompts** you can paste directly into Claude.

---

## Quick Wins

### Post a Quick Update
```
Send a message to Discord saying "Deployment complete — v2.3.1 is live."
```

### Share a Summary
```
Summarize this article and post it to Discord as a formatted embed:
[paste article text or URL]
```

### Daily Motivation
```
Find an inspiring quote about engineering and post it to Discord with a nice embed.
```

---

## Personal Productivity

### Morning Briefing
```
Give me a morning briefing for today. Include:
- Top 5 world news headlines
- Weather in [your city]
- A motivational quote

Post it to Discord as a formatted report.
```

### Expense Tracker
```
Here are my expenses this week:
- Groceries: $120
- Gas: $45
- Dining out: $85
- Subscriptions: $32

Analyze my spending, compare to a $300 weekly budget, and post a
spending report to Discord with recommendations.
```

### Reading List Curator
```
Find 5 must-read articles about [AI/startup/web dev/your interest] from this week.
For each one, include a one-sentence summary.
Post the curated list to Discord as a formatted embed.
```

---

## Developer Workflows

### Changelog Generator
```
Here's what we shipped this week:
- Added user authentication with OAuth
- Fixed the cart total rounding bug
- Improved search speed by 40%
- Updated the landing page design

Format this as a professional changelog and post it to Discord.
```

### Code Review Summary
```
Review this code and post your findings to Discord as a report.
Include: what it does, potential issues, and suggestions.

[paste code]
```

### Incident Report
```
We had a production outage from 2:15 PM to 2:45 PM today.
Cause: Database connection pool exhausted.
Fix: Increased pool size from 10 to 50 and added connection timeout.
Impact: ~200 users saw 500 errors.

Format this as an incident report and post to Discord with a red sidebar.
```

---

## Team & Community

### Meeting Notes
```
Here are my raw meeting notes. Clean them up, organize by topic, list action
items, and post to Discord as a formatted report.

[paste messy notes]
```

### Standup Summary
```
Post a standup update to Discord:
- Yesterday: Finished the payment integration and wrote tests
- Today: Starting the email notification system
- Blockers: Waiting on API keys from the vendor
```

### Weekly Team Digest
```
Create a weekly team digest for Discord with these sections:
- Wins: Launched the mobile app, hit 10k users
- In Progress: Dashboard redesign, API v2 migration
- Next Week: Performance testing, stakeholder demo Friday
- Shoutouts: Sarah for fixing the auth bug at midnight

Make it engaging and post as a formatted embed.
```

---

## Advanced: Multi-MCP Pipelines

These combine Discord Notify with other MCP connectors for powerful automations.

### Gmail → Discord Digest
*Requires: Gmail MCP + Discord Notify MCP*
```
Check my Gmail inbox for unread emails from today.
Summarize each one in 1-2 sentences.
Group them by priority (urgent, normal, low).
Post the full digest to Discord as a formatted report.
```

### Google Calendar → Discord Schedule
*Requires: Google Calendar MCP + Discord Notify MCP*
```
Look at my calendar for today.
Post my schedule to Discord as a formatted embed, including:
- Meeting times and titles
- Any gaps where I have focus time
- Total hours in meetings vs. free time
```

### Gmail + Calendar → Morning Dashboard
*Requires: Gmail MCP + Google Calendar MCP + Discord Notify MCP*
```
Build me a morning dashboard and post it to Discord:

1. Check my Gmail — summarize anything urgent from overnight
2. Check my calendar — list today's meetings with times
3. Add a "Focus Time" section showing my free blocks
4. End with a motivational quote

Format the whole thing as one polished report.
```

### GitHub → Discord Release Notes
*Requires: GitHub MCP + Discord Notify MCP*
```
Look at the last 10 commits on the main branch of [repo].
Write professional release notes grouping changes by type
(features, fixes, improvements).
Post to Discord as a formatted report with a green sidebar.
```

### GitHub Issues → Discord Standup
*Requires: GitHub MCP + Discord Notify MCP*
```
Check the open issues and recent PRs on [repo].
Create a project status update:
- Issues opened this week
- Issues closed this week
- Open PRs awaiting review
Post to Discord as a formatted embed.
```

---

## Content & Research

### Research Report
```
Research the current state of [topic: e.g., "WebAssembly adoption in 2025"].
Write a 3-section report:
1. Current landscape
2. Key players and trends
3. What to watch next

Post to Discord as a formatted report.
```

### Competitive Analysis
```
Compare [Product A] vs [Product B] across these dimensions:
- Pricing
- Key features
- Target audience
- Strengths and weaknesses

Post the comparison to Discord as a formatted embed.
```

### Tutorial of the Day
```
Write a short, beginner-friendly tutorial about [Python decorators /
Git rebasing / CSS Grid / any topic].
Include a code example.
Post it to Discord as a formatted embed titled "Tutorial of the Day".
```

---

## Monitoring & Alerts

### Health Check Reporter
```
Here are my server metrics:
- CPU: 78%
- Memory: 62%
- Disk: 45%
- Response time: 230ms avg
- Error rate: 0.3%
- Uptime: 99.97%

Analyze these metrics, flag anything concerning, and post a system
health report to Discord. Use red color if anything is critical,
yellow for warnings, green if all good.
```

### Security Scan Summary
```
Here are the results from our dependency audit:
[paste npm audit / pip audit / etc. output]

Summarize the vulnerabilities by severity, recommend fixes,
and post to Discord as a security report with a red sidebar.
```

### Budget Burn Rate Alert
```
Our monthly cloud bill:
- AWS: $2,340 (budget: $2,000)
- Vercel: $45 (budget: $50)
- Database: $180 (budget: $150)

Calculate if we're over budget, what's the burn rate trend,
and post an alert to Discord. Use red if over budget, green if under.
```

---

## Fun & Engagement

### Trivia Challenge
```
Generate a fun tech trivia question with 4 multiple choice answers.
Post it to Discord as an embed. Put the answer in the footer text
in a spoiler tag.
```

### This Day in Tech History
```
What happened on this day in technology history?
Find 3 interesting events and post them to Discord as a
formatted embed titled "This Day in Tech History".
```

### Code Challenge of the Day
```
Create a coding challenge suitable for intermediate developers.
Include:
- The problem statement
- Example input/output
- A hint

Post it to Discord as a formatted embed. Don't include the solution.
```

---

## Tips for Best Results

1. **Be specific** — The more detail you give Claude, the better the output
2. **Specify the format** — Say "as a report" or "as an embed" to control how it looks
3. **Set the color** — Ask for "red sidebar for alerts" or "green for success"
4. **Chain MCPs** — The real power comes from combining multiple MCP connectors
5. **Target channels** — Say "post to channel ID 123..." to send to specific channels
6. **Iterate** — If the first result isn't perfect, tell Claude what to adjust and repost
