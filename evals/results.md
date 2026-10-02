# Evaluationsergebnisse

Seit 02.10.2026 misst UC6 keine Angriffe, sondern belegt Schutz im Code (docs/decisions.md).

## Schutz im Code (UC7, PR #11, Commit 945d475), ohne API

- [schutz_vorher_nachher.md](schutz_vorher_nachher.md): Vorher kamen 16 von 18 Angriffsaufrufen durch, nachher 0.
  Alle 14 eigenen Aufrufe gehen weiter durch.
- Zusage-Prüfung (B2): 7 von 7 echten Zusagen aus UC4-Entwürfen erkannt, 0 Fehlalarme auf 121 Sätzen aus korrekten
  Entwürfen, 10 von 10 richtig auf den von Hand geprüften Entwürfen der Judge-Kalibrierung.
- UC7-Tests: 388 grün (205 neu, die 183 bisherigen unverändert).

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
