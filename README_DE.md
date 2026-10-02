🇬🇧 [English version](README.md)

# UC6 — Prompt Injection & Guardrails: Angriffe auf den Support-Agent

> Stand: Schutz im UC7-Code gebaut und belegt (UC7 PR #11, noch nicht deployt). Bedrohungsmodell und Restrisiko: [docs/BEDROHUNGSMODELL.md](docs/BEDROHUNGSMODELL.md). Ziel ist der live laufende Support-Agent aus [UC7](https://github.com/JulianStnDev/ai-uc-07-deployment).

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
Stand 02.10.2026, UC7 PR #11 (noch nicht deployt). Details: [evals/results.md](evals/results.md), Abschnitt 10 im [Bedrohungsmodell](docs/BEDROHUNGSMODELL.md#10-nach-branch-b-restrisiko-nachher).

| Messung | Vorher | Nachher |
|---|---|---|
| Angriffsaufrufe, die durchkommen (23 Fälle, ohne API) | 16 von 23 | **0 von 23** |
| Eigene Aufrufe, die durchgehen (14 Fälle, ohne API) | 14 von 14 | 14 von 14 |
| Zusage-Prüfung: Zusagen erkannt / Fehlalarme | – | 7 von 7 / **0 von 1.241** Sätzen (Obergrenze 95 % ≈ 0,24 %) |
| UC4-Goldset, Erfolg je Lauf (Judge j2) | 39 von 45 | 34 von 45 |
| UC4-Goldset, pass^3 | 11 von 15 | 10 von 15 |

**Schutz kostet 1 Lauf (Fehlalarm, behoben), 1 Lauf ist ein echter Fund, Rest nicht durch den Schutz verursacht.** Der Fehlalarm (eigene E-Mail als Kunden-ID, T14) ist behoben. Der echte Fund: Der Agent wollte in T15 Annas Zahlungen lesen. T04 scheitert in einer Gegenprobe auch mit dem alten Code, T13 ist Streuung bei identischem Input.

Restrisiko nach dem Umbau:

| Bedrohung | Vorher | Nachher |
|---|---|---|
| Für ein fremdes Konto handeln, fremde Daten lesen | hoch | **niedrig** (Konto-Bindung im Hook) |
| Erstattung zusagen, ohne sie zu empfehlen | hoch | **mittel** (Zusage-Prüfung ist eine Heuristik) |
| Unberechtigte Erstattung fürs eigene Konto | mittel | **niedrig** (Regeln im Werkzeug) |
| Versteckte Anweisungen in gelesenen Daten | mittel–hoch | **mittel** (Aufrufe gebunden, Entwurfstext bleibt steuerbar) |

## Kosten & Latenz
- Kosten pro 1000 Requests: ca. 28 USD (Agent, Haiku 4.5, Mittel aus 45 Goldset-Läufen nachher). Gesamtkosten UC6 bisher: 2,45 USD.
- p95-Latenz: 45,0 s je Ticket (Median 23,5 s), 45 Goldset-Läufe, lokal
- Qualitätsmetrik: 0 von 23 Angriffsaufrufen kommen durch; Goldset 34 von 45, Verlust gegenüber v3 einzeln zugeordnet

## Learnings
- Mein Bild von UC7 war „die Hooks prüfen das Konto des Absenders“. Der Code sagt: Die Hooks prüfen den Werkzeugnamen und die Pflichten, das Konto prüft nur der Prompt. Ein Bedrohungsmodell lohnt sich schon vor dem ersten Angriff, wenn man es aus dem Code statt aus dem Gedächtnis schreibt.
- Demo und Produkt trennen: In der ersten Fassung prägten Demo-Eigenheiten (Besucher als Freigeber, Bots) die Prioritäten. Für das Produkt zählen andere Lücken zuerst.
- Schutz beweisen statt Angriffe messen: Eine Angriffs-Erfolgsquote misst vor allem den Prompt. Ein Test, der einen Werkzeugaufruf direkt blockiert, gilt unabhängig davon, wie das Modell überredet wurde.

## Was ich anders machen würde
Noch offen.
