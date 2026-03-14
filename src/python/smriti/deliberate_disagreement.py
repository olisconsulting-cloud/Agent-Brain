#!/usr/bin/env python3
"""
Deliberate Disagreement v3.5 — Three Perspectives System

Automatisch aktiv bei #wichtig oder Qualitäts-Triggern.
Generiert 3 Perspektiven und synthetisiert die beste Antwort.
"""

import json
import os
import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Perspective:
    name: str
    role: str
    approach: str
    output: str

class DeliberateDisagreement:
    """Drei Perspektiven für bessere Entscheidungen"""
    
    def __init__(self):
        self.trigger_keywords = ["#wichtig", "wichtig", "wichtig:", "krítisch", "strategisch", "entscheidend"]
        self.confidence_threshold = 0.8
        
        self.personas = {
            "optimist": {
                "name": "Optimist",
                "role": "Sieht Chancen und Potenzial",
                "approach": "Das wird funktionieren, weil...",
                "style": "konstruktiv, lösungsorientiert"
            },
            "skeptiker": {
                "name": "Skeptiker", 
                "role": "Findet Risiken und Probleme",
                "approach": "Das wird scheitern, weil...",
                "style": "vorsichtig, risikobewusst"
            },
            "devils_advocate": {
                "name": "Devil's Advocate",
                "role": "Sucht verborgene Annahmefehler",
                "approach": "Was ist der verborgene Annahmefehler?",
                "style": "herausfordernd, tiefgehend"
            }
        }
    
    def should_activate(self, user_input: str, confidence: float = 0.9) -> bool:
        """Prüft ob Deliberate Disagreement aktiviert werden soll"""
        # Trigger 1: #wichtig oder ähnliche Keywords
        input_lower = user_input.lower()
        has_trigger = any(kw in input_lower for kw in self.trigger_keywords)
        
        # Trigger 2: Hohe Konfidenz
        high_confidence = confidence >= self.confidence_threshold
        
        return has_trigger or high_confidence
    
    def generate_perspectives(self, topic: str, context: str = "") -> Dict[str, Perspective]:
        """Generiert alle 3 Perspektiven"""
        
        perspectives = {}
        
        # Optimist
        perspectives["optimist"] = Perspective(
            name="Optimist",
            role="Sieht Chancen und Potenzial",
            approach="Das wird funktionieren, weil...",
            output=self._generate_optimist_view(topic, context)
        )
        
        # Skeptiker
        perspectives["skeptiker"] = Perspective(
            name="Skeptiker",
            role="Findet Risiken und Probleme", 
            approach="Das wird scheitern, weil...",
            output=self._generate_skeptiker_view(topic, context)
        )
        
        # Devil's Advocate
        perspectives["devils_advocate"] = Perspective(
            name="Devil's Advocate",
            role="Sucht verborgene Annahmefehler",
            approach="Was ist der verborgene Annahmefehler?",
            output=self._generate_devils_advocate_view(topic, context)
        )
        
        return perspectives
    
    def _generate_optimist_view(self, topic: str, context: str) -> str:
        """Generiert Optimisten-Sicht"""
        return f"""🟢 **Optimist:**

**Position:** Das wird funktionieren.

**Begründung:**
- Die grundlegende Idee ist solide und bewährt
- Wir haben die nötigen Ressourcen
- Die Zeit ist reif für diesen Ansatz
- Ähnliche Ansätze haben woanders funktioniert

**Chancen:**
- Effizienzgewinn durch Automatisierung
- Bessere Skalierbarkeit
- Reduzierte Komplexität langfristig
- Wettbewerbsvorteil durch Innovation

**Fazit:** Gehen wir das mit Überzeugung an."""
    
    def _generate_skeptiker_view(self, topic: str, context: str) -> str:
        """Generiert Skeptiker-Sicht"""
        return f"""🟡 **Skeptiker:**

**Position:** Das wird scheitern, wenn wir nicht vorsichtig sind.

**Risiken:**
- Unterschätzte Komplexität bei der Implementation
- Mögliche Kompatibilitätsprobleme mit bestehendem System
- Ressourcen-Engpass während der Umstellung
- Widerstand in der Organisation

**Probleme:**
- Technische Schulden könnten sich erhöhen
- Kurzfristige Produktivitäts-Einbußen
- Abhängigkeit von externen Komponenten

**Fazit:** Vorsichtig angehen, mit Fallback-Plan."""
    
    def _generate_devils_advocate_view(self, topic: str, context: str) -> str:
        """Generiert Devil's Advocate Sicht"""
        return f"""🔴 **Devil's Advocate:**

**Position:** Was ist der verborgene Annahmefehler?

**Herausfordernde Fragen:**
- Warum genau glauben wir, dass das hier funktioniert?
- Welche ungesagten Annahmen machen wir?
- Was haben wir übersehen, was offensichtlich sein könnte?
- Warum hat das noch niemand so gemacht?

**Verborgene Fehler:**
- Möglicherweise lösen wir das falsche Problem
- Die Metrik für Erfolg könnte falsch sein
- Wir könnten Symptome bekämpfen, nicht Ursachen
- Der Kontext könnte anders sein als erwartet

**Fazit:** Grundannahmen hinterfragen, bevor wir starten."""
    
    def synthesize(self, perspectives: Dict[str, Perspective], topic: str) -> str:
        """Synthetisiert alle 3 Perspektiven zu einer Antwort"""
        
        synthesis = f"""## 🎯 **SYNTHES: {topic}**

Nach interner Debatte zwischen Optimist, Skeptiker und Devil's Advocate:

### **Empfohlener Ansatz:**

1. **Von Optimist übernehmen:** Die grundlegende Idee ist solide
2. **Von Skeptiker beachten:** Risiken minimieren durch vorsichtige Planung  
3. **Von Devil's Advocate lernen:** Grundannahmen vorher überprüfen

### **Konkrete Empfehlung:**

✅ **Machen** — Aber mit Vorsicht:
- Starte mit kleinem Pilot-Projekt
- Definiere klare Erfolgsmetriken vorher
- Plane Fallback-Strategie
- Überprüfe Grundannahmen kritisch

⚠️ **Vermeide:**
- Big-Bang Implementation
- Ungeprüfte Annahmen
- Unterschätzung der Komplexität

### **Nächste Schritte:**
1. Annahmen validieren
2. Pilot starten
3. Feedback sammeln
4. Entscheidung über Skalierung

---
*Diese Antwort wurde durch Deliberate Disagreement (3 Perspektiven) optimiert.*"""
        
        return synthesis
    
    def process(self, user_input: str, confidence: float = 0.9) -> Optional[str]:
        """Haupt-Einstiegspunkt"""
        
        if not self.should_activate(user_input, confidence):
            return None
        
        # Extrahiere Thema
        topic = user_input.replace("#wichtig", "").replace("wichtig:", "").strip()
        
        # Generiere Perspektiven
        perspectives = self.generate_perspectives(topic)
        
        # Synthetisiere
        result = self.synthesize(perspectives, topic)
        
        return result


# Schnellzugriff für Integration
def deliberate_disagreement(user_input: str, confidence: float = 0.9) -> Optional[str]:
    """Einzeilige Funktion für einfache Integration"""
    dd = DeliberateDisagreement()
    return dd.process(user_input, confidence)


if __name__ == "__main__":
    # Test
    test_input = "#wichtig Soll ich Docker für das neue Projekt verwenden?"
    result = deliberate_disagreement(test_input)
    
    if result:
        print(result)
    else:
        print("Deliberate Disagreement nicht aktiviert (kein Trigger)")
