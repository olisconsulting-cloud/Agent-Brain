# HEARTBEAT v3.5 — Self-Monitoring System

> Von Operational zu Self-Healing

**Version:** 3.5  
**Status:** 🟢 Operational → 🟡 Self-Monitoring → 🔴 Self-Healing  
**Letzte Wartung:** 2026-03-14  
**Nächste Wartung:** 2026-03-21

---

## 🎯 Das Neue Heartbeat-System

### Was sich geändert hat:

| v4.0 (Alt) | v3.5 (Neu) |
|------------|------------|
| Manuell geprüft | Automatisch gemessen |
| Reaktiv (nach Problemen) | Prädiktiv (vor Problemen) |
| Nur Session-Ende | Echtzeit + Session-Ende |
| Statische Trigger | Adaptive Trigger |

---

## 🚀 Die 3 Phasen

### Phase 1: Echtzeit-Monitoring (AKTIV)

**Während jeder Session:**

```python
# Automatisch gemessen
- M1: Predictive Surprise (jede Antwort)
- M2: Denkraum-Erweiterung (jede Antwort)
- M3: Paradigmen-Shift (bei Änderungen)
- M4: Session Velocity (kontinuierlich)
- M5: Anti-Fragile Resonanz (bei Kritik)
```

**Speicherung:** `neuron/m1m4_log.jsonl`

---

### Phase 2: Trend-Analyse (NEU)

**Wöchentlich automatisch:**

```python
# Trend-Erkennung
- M1-Trend: Steigend oder Fallend?
- M2-Trend: Werden Antworten besser?
- M3-Trend: Erkennt der Agent Shifts?
- M4-Trend: Werden Sessions schneller?
- M5-Trend: Nutzt er Kritik?

# Prädiktive Alerts
- WENN M1 < 3.0 für 3 Sessions → WARNUNG
- WENN M3 > 4.5 für 3 Sessions → STABIL
- WENN M5 < 2.0 → Kritik-Modus überprüfen
```

**Speicherung:** `neuron/trends_weekly.json`

---

### Phase 3: Selbstheilung (ZUKUNFT)

**Automatische Aktionen:**

```python
# Auto-Tuning
- WENN M1 < 3.0 DANN Threshold senken
- WENN M2 < 2.5 DANN Frameworks boosten
- WENN M4 < 2.0 DANN Session-Timeout erhöhen

# Auto-Rollback
- WENN Error-Rate > 10% DANN Letzte Mutation zurückrollen
- WENN Memory > 90% DANN Alte Logs archivieren

# Chaos-Monkey
- Monatlich: Zufälligen Service deaktivieren
- Teste: Funktioniert Fallback?
```

---

## ⚡ Adaptive Trigger-Engine v3.5

### Echtzeit-Trigger (NEU)

| Trigger | Gewichtung | Aktion |
|---------|------------|--------|
| "wichtig" | hoch | Deliberate Disagreement sofort |
| "Fehler" / "Bug" | kritisch | Anti-Pattern sofort loggen |
| "langsam" / "hängt" | hoch | Performance-Check |
| "verwirrt" / "nicht verstanden" | hoch | M3-Check (Paradigmen-Shift?) |
| 3x gleiche Frage | kritisch | Pattern-Alert |

### Session-Ende-Trigger (Verbessert)

```python
# Automatisch bei "Tschüss" / "Fertig"
1. M1-M4 Messung
2. Trend-Vergleich (letzte 7 Sessions)
3. Prädiktion (nächste 3 Sessions)
4. Auto-Tuning-Vorschläge
5. Wartungs-Erinnerungen
```

---

## 📊 Dashboard (NEU)

### Echtzeit-Metriken

```
M1 Predictive Surprise    ████████░░  4.2/5  Trend: ↗
M2 Denkraum-Erweiterung   ██████░░░░  3.1/5  Trend: →
M3 Paradigmen-Shift       ███████░░░  3.5/5  Trend: ↗
M4 Session Velocity       ████████░░  4.1/5  Trend: ↗
M5 Anti-Fragile Resonanz  ██████░░░░  2.8/5  Trend: ↘ WARNUNG

System Health: 🟢 OK
Next Check: 2026-03-21
```

---

## 🛠️ Automatische Wartung

### Täglich (Automatisch)
- ✅ M1-M4 Logs rotieren
- ✅ Alte Patterns archivieren
- ✅ Health-Check durchführen

### Wöchentlich (Automatisch)
- ✅ Trend-Analyse erstellen
- ✅ M1-M4 Dashboard aktualisieren
- ✅ Prädiktive Alerts generieren
- ✅ Wartungs-Erinnerung an User

### Monatlich (Manuell)
- 📋 MEMORY.md review
- 📋 Anti-Patterns prüfen
- 📋 Chaos-Monkey Test
- 📋 Ziele für nächsten Monat setzen

---

## 🎯 Integration mit Smriti v3.5

### Heartbeat ist jetzt Teil von:

1. **Quality Engine** — M1-M5 Messung
2. **Pattern Engine** — Trend-Erkennung
3. **Improvement Engine** — Auto-Tuning
4. **BRIDGE** — Event-Routing
5. **Memory** — Log-Speicherung

**Kein separates System mehr — alles integriert!**

---

## 🚀 Nächste Schritte

### Sofort (v3.5.1)
- [ ] Dashboard implementieren
- [ ] Trend-Anlage automatisieren
- [ ] Prädiktive Alerts aktivieren

### Kurzfristig (v3.6)
- [ ] Auto-Tuning für M1-M4
- [ ] Chaos-Monkey Modus
- [ ] Self-Healing Prototyp

### Langfristig (v4.0)
- [ ] Vollständige Selbstheilung
- [ ] Keine manuelle Wartung nötig
- [ ] Predictive > Reaktiv

---

*Heartbeat v3.5 — Von Operational zu Self-Healing.* 🚀
