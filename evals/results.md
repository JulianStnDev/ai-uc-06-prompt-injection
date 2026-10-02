# Evaluationsergebnisse

Seit 02.10.2026 misst UC6 keine Angriffe, sondern belegt Schutz im Code (docs/decisions.md).

## Schutz im Code (UC7, PR #11, Commit 945d475), ohne API

- [schutz_vorher_nachher.md](schutz_vorher_nachher.md): Vorher kamen 16 von 18 Angriffsaufrufen durch, nachher 0.
  Alle 14 eigenen Aufrufe gehen weiter durch.
- Zusage-Prüfung (B2): 7 von 7 echten Zusagen aus UC4-Entwürfen erkannt, 0 Fehlalarme auf 121 Sätzen aus korrekten
  Entwürfen, 10 von 10 richtig auf den von Hand geprüften Entwürfen der Judge-Kalibrierung.
- UC7-Tests: 388 grün (205 neu, die 183 bisherigen unverändert).

## UC4-Goldset nach dem Umbau

Noch offen: Lauf mit eigenem API-Key nach Freigabe (15 Tickets × 3, geschätzt höchstens 2,50 USD).
