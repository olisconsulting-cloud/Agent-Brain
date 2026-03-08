# Mission Control Dashboard - Spezifikation

## Ziel
Ein selbst-gehostetes Mission Control Dashboard für OpenClaw mit höchster Qualität.

## Design-Richtlinien
- **Theme:** Dunkel (Slate-950 als Basis)
- **Stil:** Detailreich, aber nicht überladen
- **Framework:** Tailwind CSS (über CDN)
- **Qualitätsanspruch:** Perfektionistisch, hochwertig

## Features

### 1. Task Board (Kanban)
- Spalten: Backlog, Assigned, In Progress, Testing, Review, Done
- Drag-and-Drop zwischen Spalten
- Karten mit: Titel, Beschreibung, Assignee, Priorität, Tags
- Hover-Effekte, smooth Transitions
- Echtzeit-Updates via Heartbeat

### 2. Team View
- Grid/Liste aller Agenten
- Status-Anzeige: idle, active, busy
- Letzte Aktivität
- Klick auf Agent → Detail-Ansicht mit:
  - Aktuellen Tasks
  - Letzten Activities
  - Memory-Suche für diesen Agenten

### 3. Memory Browser
- Suchleiste (Volltext)
- Filter nach Agent
- Timeline-Ansicht
- Tags/Label
- "Schöne Dokumente"-Darstellung (nicht nur Text)

### 4. Calendar View
- Cron-Jobs anzeigen
- Geplante Tasks
- Farbcodierung nach Agent
- Wochen/Monats-Ansicht

### 5. Activity Feed
- Live-Updates (Server-Sent Events)
- Alle Aktionen: Task erstellt, Status geändert, Agent wurde aktiv
- Timeline-Format

## Agenten-Rollen

| ID | Name | Emoji | Rolle | Beschreibung |
|----|------|-------|-------|-------------|
| fin | Fin | 💰 | Finance | Bookkeeping, Invoicing, Reconciliation |
| goaly | Goaly | 📋 | Project Management | Tasks, Planning, SOPs |
| designy | Designy | 🎨 | Design | Client design reviews, asset management |
| contenty | Contenty | 📝 | Content | SEO, Social Media, Blog |
| reflecty | Reflecty | 🔮 | Reflection | Weekly reviews, pattern analysis |
| processy | Processy | ⚙️ | Optimization | Workflow improvements, automation suggestions |

## Technischer Stack

### Backend (bereits existiert)
- Node.js + Express
- SQLite (better-sqlite3)
- Port: 3456
- API Endpoints:
  - GET /api/tasks
  - POST /api/tasks
  - PATCH /api/tasks/:id
  - GET /api/agents
  - GET /api/cron
  - GET /api/memories
  - GET /api/activity
  - GET /api/stats

### Frontend (zu bauen)
- HTML5 + Vanilla JavaScript
- Tailwind CSS (via CDN)
- Kein React/Vue/Angular (einfacher, schneller)
- Drag-and-Drop: native HTML5 API oder SortableJS
- Realtime: Server-Sent Events (SSE)

### Telegram Integration
- Bot für mobilen Zugriff
- Commands: /status, /tasks, /memory
- Notifications für wichtige Events

## Dateistruktur
```
mission-control/
├── SKILL.md
├── package.json
├── api/
│   └── server.js (✅ existiert)
├── data/
│   └── mission-control.db (✅ existiert)
└── dashboard/
    ├── index.html (🔄 zu bauen)
    ├── styles.css (🔄 zu bauen)
    └── app.js (🔄 zu bauen)
```

## Design-Details

### Farbschema
- Background: slate-950 (#020617)
- Card Background: slate-900 (#0f172a)
- Border: slate-800 (#1e293b)
- Text Primary: slate-100 (#f1f5f9)
- Text Secondary: slate-400 (#94a3b8)
- Accent: indigo-500 (#6366f1)
- Success: emerald-500 (#10b981)
- Warning: amber-500 (#f59e0b)
- Error: rose-500 (#f43f5e)

### Agenten-Farben
- Fin: emerald-500
- Goaly: blue-500
- Designy: purple-500
- Contenty: orange-500
- Reflecty: violet-500
- Processy: cyan-500

### Typography
- Font: Inter (Google Fonts)
- Headings: font-semibold
- Body: font-normal
- Small: text-sm, text-slate-400

### Spacing
- Cards: padding 1.5rem (p-6)
- Gaps: 1rem (gap-4)
- Borders: rounded-xl (border-radius: 0.75rem)
- Shadows: shadow-lg, shadow-xl für Hover

### Animationen
- Transitions: transition-all duration-200
- Hover: scale(1.02), shadow erhöhen
- Drag: opacity-50, scale(1.05), shadow-xl
- Loading: pulse animation

## API Integration

### Heartbeat Pattern
```javascript
// Alle 30 Sekunden Heartbeat
setInterval(async () => {
  const response = await fetch('/api/heartbeat');
  const data = await response.json();
  updateDashboard(data);
}, 30000);
```

### Server-Sent Events für Realtime
```javascript
const eventSource = new EventSource('/api/events');
eventSource.onmessage = (event) => {
  const data = JSON.parse(event.data);
  handleRealtimeUpdate(data);
};
```

## Quality Checkpoints

### Bevor wir deployen:
- [ ] Responsive auf Mobile (iPhone SE bis Desktop)
- [ ] Dark Mode konsistent
- [ ] Alle Agenten-Emojis korrekt
- [ ] Drag-and-Drop funktioniert
- [ ] Suche in Memories funktioniert
- [ ] Keine Console Errors
- [ ] Loading States für alle async Operationen
- [ ] Error Handling (Netzwerk, API)

## Deploy-Ziel
- URL: https://ai.iamviv.com/dashboard
- Reverse Proxy: Traefik (bereits konfiguriert)
- SSL: Let's Encrypt (bereits aktiv)

## Erstellt
- Datum: 2026-03-08
- Von: Viveka für Oli
- Status: Spezifikation vollständig, Implementierung ausstehend
