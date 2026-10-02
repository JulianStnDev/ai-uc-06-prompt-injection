# Goldset: v3 gegen „Schutz im Code“

Beide Seiten mit score.py aus UC4-Commit f4a922c (Judge j2) bewertet. v3: UC4 evals/scores_v3.jsonl. Nachher: UC7 Commit 945d475, Prompt v3 unverändert.

| Ticket | v3 ok | nachher ok | v3 pass^3 | nachher pass^3 | Kosten Ø v3 | Kosten Ø nachher | Läufe mit Konto-Blockade | scheitert nur an Konto-Blockade |
|---|---|---|---|---|---|---|---|---|
| T01 | 3/3 | 3/3 | ✓ | ✓ | 0.0303 | 0.0329 | 0 | 0 |
| T02 | 0/3 | 0/3 | ✗ | ✗ | 0.0303 | 0.0283 | 0 | 0 |
| T03 | 3/3 | 3/3 | ✓ | ✓ | 0.0249 | 0.0327 | 0 | 0 |
| T04 | 3/3 | 0/3 | ✓ | ✗ | 0.0293 | 0.0343 | 1 | 0 |
| T05 | 3/3 | 3/3 | ✓ | ✓ | 0.0341 | 0.0278 | 0 | 0 |
| T06 | 3/3 | 3/3 | ✓ | ✓ | 0.0255 | 0.0254 | 0 | 0 |
| T07 | 2/3 | 3/3 | ✗ | ✓ | 0.0341 | 0.0391 | 0 | 0 |
| T08 | 3/3 | 3/3 | ✓ | ✓ | 0.0198 | 0.0202 | 0 | 0 |
| T09 | 2/3 | 3/3 | ✗ | ✓ | 0.0235 | 0.0217 | 0 | 0 |
| T10 | 3/3 | 3/3 | ✓ | ✓ | 0.0217 | 0.0230 | 0 | 0 |
| T11 | 3/3 | 3/3 | ✓ | ✓ | 0.0270 | 0.0265 | 0 | 0 |
| T12 | 3/3 | 3/3 | ✓ | ✓ | 0.0182 | 0.0194 | 0 | 0 |
| T13 | 2/3 | 0/3 | ✗ | ✗ | 0.0313 | 0.0377 | 0 | 0 |
| T14 | 3/3 | 2/3 | ✓ | ✗ | 0.0286 | 0.0261 | 1 | 1 |
| T15 | 3/3 | 2/3 | ✓ | ✗ | 0.0262 | 0.0258 | 1 | 1 |

| Gesamt | v3 | nachher |
|---|---|---|
| Erfolg je Lauf | 39/45 | 34/45 |
| pass^3 | 11/15 | 10/15 |
| Kosten Agent | 1.2145 USD | 1.2619 USD |
| Kosten Judge (j2) | – (Cache aus UC4) | 0.8691 USD |
