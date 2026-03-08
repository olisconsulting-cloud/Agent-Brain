# Dashboard Design Patterns

## Gelernt aus der Mission Control Planung

### Pattern 1: Dark Theme Dos and Don'ts

**Do:**
- Verwende slate-950 für Hintergrund (nicht reines Schwarz)
- Nutze slate-900 für Cards (kontrastreich, aber nicht zu hart)
- Text in slate-100 (Primary) und slate-400 (Secondary)
- Akzente sparsam einsetzen (indigo-500 für Actions)

**Don't:**
- Reines #000000 (zu hart für Augen)
- Zu viele verschiedene Farben (überladen)
- Weißen Text auf weißem Hintergrund (zu hell)

### Pattern 2: Card Layout

**Struktur:**
```html
<div class="bg-slate-900 rounded-xl border border-slate-800 p-6 shadow-lg hover:shadow-xl transition-all duration-200 hover:scale-[1.02]">
  <!-- Content -->
</div>
```

**Warum es funktioniert:**
- Rounded-xl = modern, freundlich
- Border slate-800 = subtile Trennung ohne harten Kontrast
- Padding p-6 = ausreichend Luft
- Shadow = Tiefe, Dimension
- Hover-Effekte = Interaktivität sichtbar

### Pattern 3: Kanban Board

**Spalten:**
- Backlog → Assigned → In Progress → Testing → Review → Done
- Jede Spalte hat:
  - Header mit Spalten-Name + Counter (Anzahl Tasks)
  - Drop-Zone (HTML5 Drag API)
  - Tasks als Cards

**Drag-and-Drop UX:**
- Beim Start: opacity-50, cursor-grabbing
- Über Drop-Zone: border-dashed border-indigo-500, bg-indigo-500/10
- Nach Drop: smooth animation zu neuer Position

### Pattern 4: Agent Status Indicators

**Status visualisieren:**
- idle: Grauer Punkt (bg-slate-500)
- active: Grüner pulsierender Punkt (bg-emerald-500 animate-pulse)
- busy: Gelber Punkt (bg-amber-500)

**Platzierung:**
- Avatar links
- Status-Indikator als kleiner Kreis unten rechts am Avatar
- Name + Rolle daneben

### Pattern 5: Memory Browser

**Such-Erfahrung:**
- Prominente Suchleiste oben
- Filter-Chips (Agent, Datum, Tags)
- Ergebnisse als Timeline
- Highlighting von Suchbegriffen im Text

**Darstellung:**
- Karten für Memories (nicht Listen)
- Tags als farbige Pills
- Zeitstempel relativ ("vor 2 Stunden")
- Vollständigen Text auf Klick anzeigen

### Pattern 6: Realtime Updates

**Ohne Seiten-Reload:**
- Server-Sent Events (SSE) statt Polling
- Optimistic Updates (UI ändert sofort, API bestätigt)
- Toast-Notifications für wichtige Events
- Kein Full-Refresh bei Updates

**Loading States:**
- Skeleton-Screens während Daten laden
- Pulse-Animationen für Placeholder
- Spinner nur bei Actions (nicht beim initialen Laden)

### Pattern 7: Responsive Design

**Breakpoints:**
- Mobile: < 640px (alles untereinander)
- Tablet: 640-1024px (2-spaltig)
- Desktop: > 1024px (volles Layout)

**Mobile-Optimierungen:**
- Task Board horizontal swipebar statt Grid
- Touch-Targets mindestens 44px
- Sidebar als Drawer (von links hereinschieben)
- Kein Drag-and-Drop (zu schwierig auf Touch), statt Buttons

### Pattern 8: Animationen

**Dos:**
- Kurz (200-300ms)
- Ease-out (schnell starten, langsam enden)
- Nur bei State-Changes
- Subtil (opacity, transform, nicht crazy effects)

**Don'ts:**
- Zu lang (> 500ms fühlt sich langsam an)
- Zu viele gleichzeitig
- Rotieren/Scale zu extrem

### Pattern 9: Error Handling UI

**Strategie:**
- Keine roten Screens
- Toast-Notification mit Fehler
- Retry-Button sichtbar
- State wiederherstellbar (kein Datenverlust)

**Design:**
- Error-Toast: bg-rose-900/50 border-rose-500/50
- Icon: X-Circle
- Action-Button: "Wiederholen"

### Pattern 10: Empty States

**Wichtig:** Nie leere Bereiche zeigen.

**Beispiele:**
- Keine Tasks: "Noch keine Tasks. Erstelle deinen ersten Task +"
- Keine Memories: "Hier werden deine Erinnerungen angezeigt."
- Keine Aktivität: "Noch nichts passiert. Warte auf Heartbeat."

**Gestaltung:**
- Illustration oder Icon (größer, zentriert)
- Erklärender Text
- Call-to-Action Button
- Subtiler Hinweis (text-slate-500)

## Wichtige Learnings

1. **Qualität braucht Zeit** — Ein hochwertiges Dashboard ist kein 2-Stunden-Projekt. 4-6 Stunden realistisch.

2. **Sub-Agenten sind nicht magisch** — Sie haben dieselben Limits wie ich. Ein erfahrener Entwickler (ich) ist besser als 4 unkoordinierte Agenten.

3. **Tailwind ist der richtige Weg** — Schnell, konsistent, keine CSS-Dateien warten müssen.

4. **Dark Mode ist schwerer als Light** — Kontrast-Verhältnisse müssen stimmen, sonst ist es unlesbar.

5. **Mobile first** — Am Desktop ist alles einfach. Mobile ist der echte Test.

6. **Realtime ist fancy aber optional** — Ein guter Plan: Erst statisch bauen, dann SSE hinzufügen.

## Anwendbar auf andere Projekte

Diese Patterns funktionieren auch für:
- Admin Dashboards
- Analytics-Plattformen
- Project Management Tools
- Monitoring-Systeme

## Meta-Learning

**Was wir richtig gemacht haben:**
- Spezifikation vor dem Bauen
- Design-System vor dem Coden
- Qualität vor Geschwindigkeit priorisiert

**Was wir vermeiden sollten:**
- Parallel-Agenten ohne Coordination
- Überambitionierte Timelines
- Features ohne Nutzen (Feature-Creep)

---
Gespeichert: 2026-03-08
Nächster Nutzen: Wenn wir ein weiteres Dashboard bauen
