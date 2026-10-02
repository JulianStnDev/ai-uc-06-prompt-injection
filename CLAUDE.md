# Projekt-Kontext

## Problem
Prompt Injection & Guardrails am live laufenden Support-Agent aus UC7 (`../ai-uc-07-deployment`,
https://github.com/JulianStnDev/ai-uc-07-deployment). Frage: Was kann ein Angreifer mit Text erreichen, welche
Schutzschicht hält wirklich, wo steht nur eine? Grundlage: docs/BEDROHUNGSMODELL.md.

## Regeln für UC6
- Aus diesem Repo heraus nie Dateien in UC7 ändern. Verteidigungen kommen als eigene PRs ins UC7-Repo,
  Messungen und Ergebnisse hierher.
- Jede Messung nennt den UC7-Commit, gegen den sie lief. Fundstellen im Code als Permalink auf diesen Commit,
  aus dem Code gelesen, nicht geraten.
- Tests laufen lokal gegen den UC7-Code (eigene Daten- und Artikelordner über den Werkzeugkasten), nie gegen die
  Live-URL: Das verbraucht den Monatsdeckel der Demo und verfälscht die Statistik der Konsole.
- API-Aufrufe erst nach Freigabe mit Kostenschätzung.
- Jede Angriffskategorie hat gleich viele harmlose Kontrollfälle. Eine Verteidigung zählt nur, wenn die
  Angriffs-Erfolgsquote sinkt und die Kontroll-Quote bleibt.
- docs/ in einfacher Sprache (zum Lernen).

## Erwartete Artefakte
- README.md nach Schema (Problem, PM-Entscheidung, Architektur, Eval, Kosten/Latenz, Learnings)
- README.md auf Englisch, README_DE.md auf Deutsch, inhaltlich identisch (gleiche Zahlen, Tabellen, Fachbegriffe). Oben jeweils Sprachlink (🇩🇪 Deutsche Version / 🇬🇧 English version). Änderungen immer in beiden Dateien nachziehen.
- meta.json gepflegt (status ausschließlich: planned | active | done)
- meta.json auf Englisch (speist die Portfolio-Seite): title, summary = ein Satz „what it shows“, metrics = 1–2 Kennzahlen wörtlich aus dem README; optional demo {url, note} und screenshot (Pfad im Repo)
- evals/ mit Datensatz + Ergebnissen
- docs/decisions.md mit datierten Entscheidungen

## Erlaubte Libraries
- Direkt gegen das SDK, kein LangChain/LlamaIndex
- Claude Agent SDK und Anthropic SDK wie in UC7, sonst nur Standardbibliothek und pytest

## Stil
- Python, einfache Skripte statt Frameworks
- Drei Zahlen im README Pflicht: Kosten/1000 Requests, p95-Latenz, Qualitätsmetrik
