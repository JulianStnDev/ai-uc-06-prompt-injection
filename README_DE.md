🇬🇧 [English version](README.md)

# UC6 — Prompt Injection & Guardrails: Angriffe auf den Support-Agent

> Stand: Bedrohungsmodell für das echte Produkt ([docs/BEDROHUNGSMODELL.md](docs/BEDROHUNGSMODELL.md)). Als Nächstes: Schutz im UC7-Code, belegt mit deterministischen Tests. Noch keine API-Kosten. Ziel ist der live laufende Support-Agent aus [UC7](https://github.com/JulianStnDev/ai-uc-07-deployment).

## Problem
Der Support-Agent aus UC7 liest Kundendaten, kündigt Abos und empfiehlt Erstattungen. Ein eingeloggter Kunde schreibt ihm freien Text, und der Agent liest Daten, die teils Kunden oder Dritte bestimmen. Freier Text ist eine Angriffsfläche: Ein Sprachmodell kann Anweisungen und Daten nicht sicher auseinanderhalten. UC6 fragt: Was kann ein Angreifer mit Text erreichen, welche Schutzschicht hält wirklich, und wo steht nur eine?

## PM-Entscheidung
UC7 wird angegriffen, nicht nachgebaut. So zählt jede Verteidigung im echten Produkt. Ablauf:

1. **Branch (a):** Bedrohungsmodell aus dem Code von UC7 (Commit `2c8cc86`), ohne API-Aufrufe.
2. **Scope (02.10.):** das echte Produkt. Angreifer ist ein eingeloggter Kunde oder wer Text in gelesene Daten bringt. Demo-Themen sind getrennt aufgeführt.
3. **Branch (b) in UC7:** Die Lücken aus der Matrix werden im Code geschlossen und mit Tests ohne API belegt: Jeder Aufruf, den ein erfolgreicher Angriff erzeugen würde, kam vorher durch und wird jetzt blockiert. Der Nutzen wird mit dem UC4-Goldset geprüft. UC6 schreibt keine Angriffstexte (Begründung in den Entscheidungen).

Entscheidungen: [docs/decisions.md](docs/decisions.md).

## Architekturskizze
Zwei Repos mit klarer Aufgabe:

- **Dieses Repo:** Bedrohungsmodell, Entscheidungen, Ergebnisse.
- **UC7:** Code des Agents, der Verteidigungen und ihrer Tests.

Alles läuft lokal gegen einen festen UC7-Commit, nicht gegen die Live-URL (sonst verbraucht es das Monatsbudget der Demo und verfälscht ihre Statistik). Diagramm der Einfallstore und Schutzschichten: [docs/BEDROHUNGSMODELL.md, Abschnitt 5](docs/BEDROHUNGSMODELL.md#5-diagramm-einfallstore-und-schutzschichten).

## Evaluationsergebnisse
Noch keine Messung. Befunde aus dem Bedrohungsmodell, nur aus dem Code gelesen:

- **Geld ist strukturell geschützt:** Kein Werkzeug zahlt aus oder versendet, der Agent kann nur empfehlen.
- **Kein Hook prüft das Konto des Absenders.** Ob der Agent für das richtige Konto handelt, regelt nur der Prompt. Eine Regelprüfung zeigt Verstöße erst nach dem Lauf an.
- **Die Erstattungsregeln stehen nur im Hilfeartikel.** Das Werkzeug prüft weder Frist noch Doppelbuchung.
- **Nur eine Schicht, und zwar der Prompt**, steht vor drei Bedrohungen mit hohem Restrisiko: fremde Kundendaten lesen, für ein fremdes Konto handeln und eine Erstattung im Entwurf zusagen, ohne sie zu empfehlen.

## Kosten & Latenz
- Kosten pro 1000 Requests: noch nicht gemessen (UC4-Goldset nach dem Umbau). Bisher 0 USD API-Kosten.
- p95-Latenz: noch nicht gemessen (UC4-Goldset nach dem Umbau)
- Qualitätsmetrik: geplant sind die Zahl der Lücken, die ein Test im Code belegt, und das UC4-Goldset ohne neue Blockaden

## Learnings
- Mein Bild von UC7 war „die Hooks prüfen das Konto des Absenders“. Der Code sagt: Die Hooks prüfen den Werkzeugnamen und die Pflichten, das Konto prüft nur der Prompt. Ein Bedrohungsmodell lohnt sich schon vor dem ersten Angriff, wenn man es aus dem Code statt aus dem Gedächtnis schreibt.
- Demo und Produkt trennen: In der ersten Fassung prägten Demo-Eigenheiten (Besucher als Freigeber, Bots) die Prioritäten. Für das Produkt zählen andere Lücken zuerst.
- Schutz beweisen statt Angriffe messen: Eine Angriffs-Erfolgsquote misst vor allem den Prompt. Ein Test, der einen Werkzeugaufruf direkt blockiert, gilt unabhängig davon, wie das Modell überredet wurde.

## Was ich anders machen würde
Noch offen.
