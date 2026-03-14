#!/usr/bin/env python3
"""
Deliberate Disagreement v2.0 — DYNAMIC Three Perspectives System

Automatisch aktiv bei 'wichtig' in JEDEM Kontext.
Generiert dynamische, kontext-spezifische Perspektiven.
"""

import json
import os
import re
from typing import Dict, List, Optional
from dataclasses import dataclass
from pathlib import Path

@dataclass
class Perspective:
    name: str
    role: str
    analysis: str
    arguments: List[str]
    conclusion: str

class DeliberateDisagreementV2:
    """Dynamische Drei-Perspektiven-Analyse"""
    
    def __init__(self):
        # Trigger: "wichtig" in JEDEM Kontext
        self.trigger_pattern = re.compile(r'\bwichtig\b', re.IGNORECASE)
        
        self.workspace = Path(os.environ.get('SMRITI_WORKSPACE', '/data/.openclaw/workspace'))
        self.memory_file = self.workspace / 'data' / 'memory' / 'dd_history.jsonl'
        
        # Stelle sicher, dass das Verzeichnis existiert
        self.memory_file.parent.mkdir(parents=True, exist_ok=True)
    
    def should_activate(self, user_input: str) -> bool:
        """Prüft ob 'wichtig' irgendwo im Text vorkommt"""
        return bool(self.trigger_pattern.search(user_input))
    
    def extract_topic(self, user_input: str) -> str:
        """Extrahiert das Thema aus dem Input"""
        # Entferne "wichtig" und Satzzeichen am Anfang
        topic = re.sub(r'^.*?\bwichtig\b[\s:!.,]*', '', user_input, flags=re.IGNORECASE).strip()
        
        # Entferne Frage-Wörter am Anfang
        topic = re.sub(r'^(soll ich|sollten wir|müssen wir|kann ich|will ich)\s+', '', topic, flags=re.IGNORECASE)
        
        # Entferne Satzzeichen am Ende
        topic = re.sub(r'[?.!]+$', '', topic).strip()
        
        return topic if topic else "Das vorgeschlagene Vorhaben"
    
    def analyze_topic(self, topic: str) -> Dict:
        """Analysiert das Thema für dynamische Perspektiven"""
        
        # Keywords für verschiedene Bereiche
        tech_keywords = ['docker', 'kubernetes', 'cloud', 'server', 'api', 'code', 'software', 'system']
        business_keywords = ['kunde', 'umsatz', 'marketing', 'verkauf', 'strategie', 'business']
        personal_keywords = ['lernen', 'karriere', 'job', 'beziehung', 'gesundheit', 'wohnung', 'haus']
        
        topic_lower = topic.lower()
        
        # Bestimme den Bereich
        if any(kw in topic_lower for kw in tech_keywords):
            domain = "technisch"
            context = "Technologie-Entscheidung"
        elif any(kw in topic_lower for kw in business_keywords):
            domain = "geschäftlich"
            context = "Business-Entscheidung"
        elif any(kw in topic_lower for kw in personal_keywords):
            domain = "persönlich"
            context = "Persönliche Entscheidung"
        else:
            domain = "allgemein"
            context = "Strategische Entscheidung"
        
        return {
            "topic": topic,
            "domain": domain,
            "context": context
        }
    
    def generate_optimist(self, analysis: Dict) -> Perspective:
        """Generiert dynamischen Optimisten"""
        topic = analysis["topic"]
        domain = analysis["domain"]
        
        if domain == "technisch":
            arguments = [
                f"{topic} ist industriestandard und bewährt",
                "Skalierbarkeit und Wartbarkeit werden deutlich verbessert",
                "Langfristige Kosteneinsparungen durch Effizienz",
                "Große Community und Support verfügbar"
            ]
            conclusion = f"Die technischen Vorteile von {topic} überwiegen die Risiken."
            
        elif domain == "geschäftlich":
            arguments = [
                f"{topic} öffnet neue Marktchancen",
                "Wettbewerbsvorteil durch frühen Einstieg",
                "ROI ist in ähnlichen Fällen nachweisbar",
                "Kundenfeedback unterstützt diese Richtung"
            ]
            conclusion = f"{topic} ist eine strategisch kluge Entscheidung."
            
        elif domain == "persönlich":
            arguments = [
                f"{topic} fördert persönliches Wachstum",
                "Die Zeit ist reif für diesen Schritt",
                "Langfristige Vorteile überwiegen kurzfristige Unannehmlichkeiten",
                "Du hast die nötigen Ressourcen"
            ]
            conclusion = f"{topic} wird deine Situation verbessern."
        else:
            arguments = [
                f"Die grundlegende Idee von {topic} ist solide",
                "Chancen überwiegen die Risiken",
                "Timing und Kontext sind günstig",
                "Vergleichbare Ansätze waren erfolgreich"
            ]
            conclusion = f"{topic} ist eine gute Entscheidung."
        
        return Perspective(
            name="Optimist",
            role="Sieht Chancen und Potenzial",
            analysis=f"Ich analysiere {topic} aus der Perspektive des Optimisten...",
            arguments=arguments,
            conclusion=conclusion
        )
    
    def generate_skeptiker(self, analysis: Dict) -> Perspective:
        """Generiert dynamischen Skeptiker"""
        topic = analysis["topic"]
        domain = analysis["domain"]
        
        if domain == "technisch":
            arguments = [
                f"{topic} hat eine Lernkurve die unterschätzt wird",
                "Migrationskosten und Komplexität werden oft vernachlässigt",
                "Abhängigkeit von externen Komponenten erhöht Risiko",
                "Team-Widerstand und Schulungsaufwand sind real"
            ]
            conclusion = f"Die technischen Risiken von {topic} erfordern vorsichtige Planung."
            
        elif domain == "geschäftlich":
            arguments = [
                f"{topic} erfordert erhebliche Investition ohne garantierten Erfolg",
                "Markt könnte sich anders entwickeln als erwartet",
                "Konkurrenz könnte schneller reagieren",
                "Interne Ressourcen sind möglicherweise unzureichend"
            ]
            conclusion = f"{topic} birgt erhebliche geschäftliche Risiken."
            
        elif domain == "persönlich":
            arguments = [
                f"{topic} erfordert Opfer die möglicherweise zu hoch sind",
                "Zeitpunkt könnte besser gewählt werden",
                "Unvorhergesehene Konsequenzen sind wahrscheinlich",
                "Alternative Optionen sollten geprüft werden"
            ]
            conclusion = f"{topic} sollte nicht übereilt werden."
        else:
            arguments = [
                f"Die Komplexität von {topic} wird unterschätzt",
                "Ressourcen-Engpässe sind wahrscheinlich",
                "Zeitplan ist unrealistisch",
                "Fallback-Option fehlt"
            ]
            conclusion = f"{topic} erfordert mehr Vorbereitung."
        
        return Perspective(
            name="Skeptiker",
            role="Findet Risiken und Probleme",
            analysis=f"Ich analysiere {topic} aus der Perspektive des Skeptikers...",
            arguments=arguments,
            conclusion=conclusion
        )
    
    def generate_devils_advocate(self, analysis: Dict) -> Perspective:
        """Generiert dynamischen Devil's Advocate"""
        topic = analysis["topic"]
        
        # Generiere herausfordernde Fragen basierend auf dem Thema
        questions = [
            f"Warum genau glauben wir, dass {topic} hier funktioniert?",
            f"Welche ungesagten Annahmen machen wir über {topic}?",
            "Was haben wir übersehen, was offensichtlich sein könnte?",
            "Warum hat das noch niemand so gemacht?",
            "Was ist der wahre Grund für diesen Vorschlag?",
            "Welches Problem lösen wir eigentlich wirklich?"
        ]
        
        return Perspective(
            name="Devil's Advocate",
            role="Sucht verborgene Annahmefehler",
            analysis=f"Ich hinterfrage die Grundannahmen zu {topic}...",
            arguments=questions,
            conclusion=f"Die Annahmen hinter {topic} müssen validiert werden, bevor wir fortfahren."
        )
    
    def synthesize(self, perspectives: Dict[str, Perspective], analysis: Dict) -> str:
        """Synthetisiert alle Perspektiven zu einer dynamischen Empfehlung"""
        topic = analysis["topic"]
        domain = analysis["domain"]
        
        # Speichere in Memory für Lernen
        self._save_to_memory(topic, perspectives)
        
        # Domain-spezifische Empfehlung
        if domain == "technisch":
            recommendation = f"**Empfohlener Ansatz für {topic}:**\n\n1. **Proof of Concept** — Kleines Testprojekt starten\n2. **Team-Evaluation** — Technisches Team befragen\n3. **Kosten-Nutzen-Analyse** — Konkrete Zahlen ermitteln\n4. **Fallback-Plan** — Wie kommen wir zurück wenn es nicht funktioniert?"
            
        elif domain == "geschäftlich":
            recommendation = f"**Empfohlener Ansatz für {topic}:**\n\n1. **Markt-Validierung** — Kunden befragen bevor wir investieren\n2. **Pilot-Programm** — Mit kleiner Gruppe testen\n3. **Konkurrenz-Analyse** — Was machen andere?\n4. **Exit-Strategie** — Wann steigen wir aus wenn es nicht funktioniert?"
            
        elif domain == "persönlich":
            recommendation = f"**Empfohlener Ansatz für {topic}:**\n\n1. **Zeit-Check** — Ist jetzt der richtige Zeitpunkt?\n2. **Ressourcen-Check** — Haben ich wirklich alles was nötig ist?\n3. **Alternativen-Check** — Gibt es bessere Optionen?\n4. **Beratung** — Was sagen vertraute Personen dazu?"
        else:
            recommendation = f"**Empfohlener Ansatz für {topic}:**\n\n1. **Annahmen validieren** — Sind unsere Grundannahmen korrekt?\n2. **Risiken minimieren** — Was kann schiefgehen und wie verhindern wir es?\n3. **Kleiner Schritt** — Können wir es testen bevor wir voll commiten?\n4. **Review-Punkt** — Wann evaluieren wir ob es funktioniert?"
        
        return f"""## 🎭 **DELIBERATE DISAGREEMENT — 3 Perspektiven**
### Thema: {topic}

---

### 🟢 **{perspectives['optimist'].name}** — {perspectives['optimist'].role}

**Position:** {perspectives['optimist'].conclusion}

**Argumente:**
{chr(10).join(f"• {arg}" for arg in perspectives['optimist'].arguments)}

---

### 🟡 **{perspectives['skeptiker'].name}** — {perspectives['skeptiker'].role}

**Position:** {perspectives['skeptiker'].conclusion}

**Risiken:**
{chr(10).join(f"• {arg}" for arg in perspectives['skeptiker'].arguments)}

---

### 🔴 **{perspectives['devils_advocate'].name}** — {perspectives['devils_advocate'].role}

**Herausfordernde Fragen:**
{chr(10).join(f"• {arg}" for arg in perspectives['devils_advocate'].arguments)}

**Position:** {perspectives['devils_advocate'].conclusion}

---

## 🎯 **SYNTHES**

{recommendation}

---
*Analyse basiert auf {analysis['context']} | Domain: {domain}*"""
    
    def _save_to_memory(self, topic: str, perspectives: Dict):
        """Speichert für kontinuierliches Lernen"""
        try:
            entry = {
                "timestamp": str(Path().stat().st_mtime),
                "topic": topic,
                "perspectives": {k: v.__dict__ for k, v in perspectives.items()},
                "domain": self.analyze_topic(topic)["domain"]
            }
            with open(self.memory_file, 'a') as f:
                f.write(json.dumps(entry) + '\n')
        except Exception:
            pass  # Silent fail für Memory
    
    def process(self, user_input: str) -> Optional[str]:
        """Haupt-Einstiegspunkt — automatisch bei 'wichtig'"""
        
        if not self.should_activate(user_input):
            return None
        
        # Extrahiere und analysiere Thema
        topic = self.extract_topic(user_input)
        analysis = self.analyze_topic(topic)
        
        # Generiere alle 3 Perspektiven (dynamisch!)
        perspectives = {
            "optimist": self.generate_optimist(analysis),
            "skeptiker": self.generate_skeptiker(analysis),
            "devils_advocate": self.generate_devils_advocate(analysis)
        }
        
        # Synthetisiere
        return self.synthesize(perspectives, analysis)


# Schnellzugriff für Integration
def deliberate_disagreement_v2(user_input: str) -> Optional[str]:
    """Einzeilige Funktion für einfache Integration"""
    dd = DeliberateDisagreementV2()
    return dd.process(user_input)


if __name__ == "__main__":
    # Test
    test_inputs = [
        "wichtig Soll ich Docker verwenden?",
        "wichtig Soll ich den Job wechseln?",
        "Das ist wichtig: Neue Marketing-Strategie!"
    ]
    
    for test in test_inputs:
        print(f"\n{'='*60}")
        print(f"Input: {test}")
        print('='*60)
        result = deliberate_disagreement_v2(test)
        if result:
            print(result[:800] + "..." if len(result) > 800 else result)
        else:
            print("Nicht aktiviert")
