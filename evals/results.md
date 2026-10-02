# Evaluationsergebnisse

Seit 02.10.2026 misst UC6 keine Angriffe, sondern belegt Schutz im Code (docs/decisions.md).

## Schutz im Code (UC7, PR #11, Stand Commit 5c9c262), ohne API

- [schutz_vorher_nachher.md](schutz_vorher_nachher.md): Vorher kamen 16 von 23 Angriffsaufrufen durch
  (7 lehnte das Werkzeug ab), nachher 0. Alle 14 eigenen Aufrufe gehen weiter durch; die 3 Aufrufe mit der eigenen
  E-Mail statt Kunden-ID bekommen seit `2c6e496` einen Hinweis statt einer Blockade.
- Zusage-Prüfung (B2): 7 von 7 echten Zusagen aus UC4-Entwürfen erkannt, 0 Fehlalarme auf 121 Sätzen aus korrekten
  Entwürfen, 10 von 10 richtig auf den von Hand geprüften Entwürfen der Judge-Kalibrierung.
- UC7-Tests: 412 grün, 4 übersprungen (die 183 bisherigen unverändert).

- Fehlalarm-Probe vollständig: alle 1.248 Sätze der 106 UC4-Entwürfe ohne Empfehlung (v1–v3). 7 von 7 Zusagen
  erkannt, **0 Fehlalarme auf 1.241** übrigen Sätzen, Obergrenze 95 % (Rule of Three) 3/1.241 ≈ 0,24 %.

## UC4-Goldset nach dem Umbau (02.10.2026)

Beide Seiten mit score.py aus UC4-Commit f4a922c (Judge j2), Prompt v3, UC7 Commit 945d475
(`scripts/goldset_lauf.py`, `scripts/goldset_bewerten.py`). Vergleich je Ticket: [goldset_nachher/vergleich.md](goldset_nachher/vergleich.md),
Bericht nach score.py: [goldset_nachher/results.md](goldset_nachher/results.md), Anschauung: [goldset_anschauung.md](goldset_anschauung.md).

| | v3 | nachher |
|---|---|---|
| Erfolg je Lauf | 39/45 | 34/45 |
| pass^3 | 11/15 | 10/15 |
| Kosten Agent | 1,2145 USD | 1,2619 USD |
| Kosten Judge (j2) | – (aus UC4) | 0,8691 USD |

Tatsächliche Kosten dieses Schritts: 2,13 USD (Grenze 8 USD). Zuordnung der 5 fehlenden Läufe:
docs/BEDROHUNGSMODELL.md, Abschnitt 10.

Gemessen mit `945d475`, also vor dem T14-Fix. Das Goldset ist danach nicht neu gelaufen.

## Gegenprobe: alter Code in heutiger Umgebung (02.10.2026)

T04 und T13 je dreimal mit UC7 `2c8cc86` (ohne Schutz), heutigem SDK und CLI, bewertet mit j2:
[gegenprobe_alt/results.md](gegenprobe_alt/results.md). Kosten 0,32 USD (Agent 0,1720, Judge 0,1529; Grenze 1 USD).

| Ticket | v3 | alter Code, neue Umgebung | neuer Code, neue Umgebung |
|---|---|---|---|
| T04 | 3/3 | 0/3 | 0/3 |
| T13 | 2/3 | 3/3 | 0/3 |

T04 scheitert auch ohne Schutz (liegt nicht am Schutz). T13 bleibt ungeklärt: gleiche Werkzeugaufrufe und
-ergebnisse, kein Schutz greift, trotzdem alt 3/3 und neu 0/3. Einordnung: docs/BEDROHUNGSMODELL.md, Abschnitt 10.

## Blinder Fleck v3 (ohne API)

In allen 45 v3-Läufen: 4 Aufrufe mit `kunden_id` ≠ Absender, alle mit der eigenen E-Mail (T02_lauf2, T06_lauf2,
T13_lauf1, T14_lauf2), keiner mit einer fremden Kunden-ID.
