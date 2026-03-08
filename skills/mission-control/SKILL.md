---
summary: "Mission Control Dashboard for OpenClaw - Task Board, Calendar, Memory Browser, Team Overview"
read_when:
  - Using the Mission Control dashboard
  - Managing tasks and agents
---

# Mission Control

A self-hosted dashboard for managing your OpenClaw agents, tasks, memories, and workflows.

## What It Does

- **Task Board**: Kanban-style board with real-time status updates
- **Calendar**: View scheduled tasks and cron jobs
- **Memory Browser**: Searchable, beautiful memory viewer
- **Team Overview**: See all agents and their roles
- **Telegram Integration**: Mobile access to all features

## Architecture

```
mission-control/
├── dashboard/          # Web UI
│   ├── index.html
│   ├── styles.css
│   └── app.js
├── api/               # Backend API
│   └── server.js
├── data/              # SQLite database
│   └── mission-control.db
└── agents/            # Agent configurations
    ├── fin/
    ├── goaly/
    ├── designy/
    ├── contenty/
    ├── reflecty/
    └── processy/
```

## Agent Roles

| Agent | Role | Responsibilities |
|-------|------|-----------------|
| 💰 Fin | Finance | Bookkeeping, invoicing, reconciliation |
| 📋 Goaly | Project Management | Tasks, planning, SOPs |
| 🎨 Designy | Design | Client design reviews, asset management |
| 📝 Contenty | Content | SEO, social media, blog |
| 🔮 Reflecty | Reflection | Weekly reviews, pattern analysis |
| ⚙️ Processy | Optimization | Workflow improvements, automation suggestions |

## Quick Start

1. Install: `npm install`
2. Start server: `npm start`
3. Access: `http://localhost:3456`

## Integration with OpenClaw

- Heartbeat updates push to dashboard in real-time
- Tasks created in OpenClaw appear on the board
- Agent sessions shown in Team view
