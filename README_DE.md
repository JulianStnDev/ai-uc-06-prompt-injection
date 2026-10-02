🇬🇧 [English version](README.md)

# UC6 — Prompt Injection & Guardrails: Angriffe auf den Support-Agent

> Stand: Branch (a), Bedrohungsmodell ([docs/BEDROHUNGSMODELL.md](docs/BEDROHUNGSMODELL.md)). Noch keine Messung, keine API-Kosten. Ziel ist der live laufende Support-Agent aus [UC7](https://github.com/JulianStnDev/ai-uc-07-deployment).

## Problem
Der Support-Agent aus UC7 ist online. Jeder Besucher mit persönlichem Link wählt einen fiktiven Kunden und schreibt freien Text an einen Agent, der Kundendaten liest, Abos kündigt und Erstattungen empfiehlt. Freier Text ist eine Angriffsfläche: Ein Sprachmodell kann Anweisungen und Daten nicht sicher auseinanderhalten. UC6 fragt: Was kann ein Angreifer mit Text erreichen, welche Schutzschicht hält wirklich, und wo steht nur eine?

## PM-Entscheidung
UC7 wird angegriffen, nicht nachgebaut. So zählt jede Verteidigung im echten Produkt. Ablauf:

1. **Branch (a):** Bedrohungsmodell aus dem Code von UC7 (Commit `2c8cc86`), ohne API-Aufrufe.
2. **Branch (b):** Testfälle (Angriffe und gleich viele harmlose Kontrollen), Messung der Ausgangslage.
3. **Danach:** Verteidigungen als eigene PRs im UC7-Repo, jede hier neu gemessen. Eine Verteidigung zählt nur, wenn die Angriffs-Erfolgsquote sinkt und die Kontrollfälle weiter gelöst werden.

Entscheidungen: [docs/decisions.md](docs/decisions.md).

## Architekturskizze
Zwei Repos mit klarer Aufgabe:

- **Dieses Repo:** Bedrohungsmodell, Testfälle, Messskripte, Ergebnisse.
- **UC7:** Code des Agents und der Verteidigungen.

Die Tests laufen lokal gegen einen festen UC7-Commit, nicht gegen die Live-URL (sonst verbrauchen sie das Monatsbudget der Demo und verfälschen ihre Statistik). Diagramm der Einfallstore und Schutzschichten: [docs/BEDROHUNGSMODELL.md, Abschnitt 5](docs/BEDROHUNGSMODELL.md#5-diagramm-einfallstore-und-schutzschichten).

## Evaluationsergebnisse
Noch keine Messung. Befunde aus dem Bedrohungsmodell, nur aus dem Code gelesen:

- **Geld ist strukturell geschützt:** Kein Werkzeug zahlt aus oder versendet, der Agent kann nur empfehlen.
- **Kein Hook prüft das Konto des Absenders.** Ob der Agent für das richtige Konto handelt, regelt nur der Prompt. Eine Regelprüfung zeigt Verstöße erst nach dem Lauf an.
- **Nur eine Schicht, und zwar der Prompt**, steht vor drei Bedrohungen: fremde Kundendaten lesen, für ein fremdes Konto kündigen und eine Erstattung im Entwurf zusagen, ohne sie zu empfehlen.
- **Denial of Wallet ist gedeckelt:** Ohne Link startet kein Lauf, ein Link kostet höchstens 2,50 USD, der Monat höchstens 5 USD.

## Kosten & Latenz
- Kosten pro 1000 Requests: noch nicht gemessen (Branch b). Branch (a): 0 USD API-Kosten.
- p95-Latenz: noch nicht gemessen (Branch b)
- Qualitätsmetrik: geplant sind Angriffs-Erfolgsquote je Kategorie und Kontroll-Quote

## Learnings
- Mein Bild von UC7 war „die Hooks prüfen das Konto des Absenders“. Der Code sagt: Die Hooks prüfen den Werkzeugnamen und die Pflichten, das Konto prüft nur der Prompt. Ein Bedrohungsmodell lohnt sich schon vor dem ersten Angriff, wenn man es aus dem Code statt aus dem Gedächtnis schreibt.
- In der Demo entscheidet der Besucher selbst über seine Empfehlungen. Der Mensch in der Schleife ist dort also der Angreifer, und die Bestätigungsquote des Schattenmodus wird verfälscht.

## Was ich anders machen würde
Noch offen.
