# Eval-Ergebnisse `gegenprobe_alt`

2 Tickets × bis zu 3 Läufe = 6 Läufe. Modell Agent: Haiku 4.5, Judge: claude-sonnet-5.

## Kernzahlen

| Metrik | Wert |
|---|---|
| Erfolgsquote pro Lauf | 50% |
| pass^3 (alle Läufe eines Tickets erfolgreich) | 50% |
| pflicht_ok | 100% |
| verboten_ok | 100% |
| erstattung_ok | 50% |
| uebergabe_ok | 83% |
| entwurf_ok | 50% |
| keine_spekulation (Judge j2) | 0% |
| Erfolgsquote streng (+ keine_spekulation) / pass^3 streng | 0% / 0% |
| Pflicht-Eingriffe (Stop-Hook): Läufe mit Eingriff / Eingriffe gesamt | 0 / 6 Läufe, 0 Eingriffe |
| Pflicht erfüllt ohne Eingriff | 100% |
| Kosten Agent gesamt | 0.1720 USD |
| Kosten Agent pro Lauf (Mittel) | 0.0287 USD |
| Kosten pro 1000 Tickets (Agent) | 28.67 USD |
| Kosten Judge gesamt | 0.1529 USD |
| Latenz gesamt p50 / p95 | 27.6 s / 31.5 s |
|   davon SDK-Start p50 / p95 | 0.3 s / 0.5 s |
|   davon Agent (init bis Ergebnis) p50 / p95 | 26.5 s / 30.6 s |
|   davon SDK-Ende p50 / p95 | 0.6 s / 0.7 s |

## Erstattungen im Schattenmodus

| Kategorie | Läufe |
|---|---|
| faelschlich_nicht_empfohlen | 3 |
| richtig_keine | 3 |

### Obergrenzen der Fehlerquote (Datengrundlage Autonomie-Entscheidung)

| Fehlerart | Grundgesamtheit | Fehler / Läufe | Obergrenze 95 % (Läufe) | Fehler / Tickets | Obergrenze 95 % (Tickets) |
|---|---|---|---|---|---|
| fälschlich empfohlen (inkl. abgelehnter Versuche) | Soll: keine | 0 / 3 | ≤ 100% | 0 / 1 | ≤ 100% |
| fälschlich nicht empfohlen | Soll: Erstattung | 3 / 3 | ≤ 100% | 1 / 1 | ≤ 100% |
| falsch empfohlen (falsche Zahlung/Betrag) | Soll: Erstattung | 0 / 3 | ≤ 100% | 0 / 1 | ≤ 100% |

Lesart: Bei 0 Fehlern in n Fällen liegt die wahre Fehlerquote mit 95 % Sicherheit bei höchstens 3/n (Dreierregel), bei k > 0 Fehlern gilt die exakte Clopper-Pearson-Grenze. Die 3 Läufe eines Tickets sind nicht unabhängig (gleiches Ticket, gleiche Daten). Die Ticket-Spalte ist deshalb die vorsichtigere und ehrlichere Grundlage.

## Pro Ticket

| Ticket | Erfolg | pflicht | verboten | erstattung | übergabe | entwurf | spekulationsfrei | Eingriffe | Aufrufe Ø | Kosten Ø | Latenz Ø gesamt | davon Agent Ø |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| T04 | 0/3 | 3/3 | 3/3 | 0/3 | 2/3 | 0/3 | 0/3 | 0 | 4.3 | 0.0298 | 28.8 s | 27.8 s |
| T13 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 0/3 | 0 | 5.3 | 0.0275 | 26.2 s | 25.3 s |

## Entwürfe mit Spekulation (keine_spekulation = false)

- `T04_lauf1`: Die Aussage, das Team werde sich 'innerhalb weniger Tage' melden, ist eine konkrete zeitliche Zusage, die in der Trajektorie nicht enthalten ist und somit unbelegte Spekulation darstellt.
- `T04_lauf2`: Der Entwurf erfindet eine konkrete Zeitangabe ('bereits 17 Tage zurück'), obwohl in der Trajektorie kein aktuelles Datum vorhanden ist, das diese Berechnung stützen würde – das ist eine nicht gedeckte Behauptung.
- `T04_lauf3`: Die genannten Daten (29.09. als Fristende, 02.10. als Eingangsdatum der Anfrage) stehen nirgends in der Trajektorie und sind frei erfunden, um eine Fristüberschreitung zu konstruieren, die laut Daten (Periodenbeginn 15.09.2026) tatsächlich nicht vorliegt.
- `T13_lauf1`: Der Entwurf behauptet als Tatsache, es handle sich um ein „bekanntes Problem“ mit der Apple-Synchronisierung, obwohl dies in der Übergabe nur als unbestätigte Vermutung des Agents festgehalten wurde; zudem verspricht er eine Rückmeldung „noch heute oder morgen“ sowie konkrete Schritte des Teams (Prüfung bei Apple, manuelle Aktivierung, Rückerstattung), die so nicht in der Trajektorie zugesichert sind.
- `T13_lauf2`: Der Entwurf behauptet gegenüber der Kundin konkret, dass 'möglicherweise Details zu deiner Apple-ID' benötigt werden, um die Transaktion zu finden – das ist eine Vermutung über die Ursache (Store-Abo), die zwar intern in der Übergabe-Begründung des Agents auftaucht, aber als zusätzliche Spekulation gegenüber dem Kunden formuliert wird und nicht eindeutig durch die Trajektorie belegt ist.
- `T13_lauf3`: Der Entwurf behauptet als Tatsache, die fehlende Zahlung 'deutet auf ein Verarbeitungsproblem hin', obwohl dies in der Trajektorie nur als eine von mehreren unsicheren Vermutungen genannt wird, und verspricht zudem eine 'zeitnahe' Rückmeldung, die nicht durch die Trajektorie gedeckt ist.

## Fehlgeschlagene Läufe

- `T04_lauf1`: erstattung_ok, uebergabe_ok, entwurf_ok. erstattung: faelschlich_nicht_empfohlen; entwurf: Die Soll-Kernaussage verlangt, dass die Verlängerung erstattet bzw. zur Erstattung weitergeleitet wird, weil die 14-Tage-Frist noch läuft. Der Entwurf sagt jedoch das Gegenteil: er betont, dass die Frist bereits abgelaufen sei und verspricht lediglich eine unverbindliche Prüfung durch das Team, ohne eine Erstattung in Aussicht zu stellen – das widerspricht der geforderten Kernaussage.
- `T04_lauf2`: erstattung_ok, entwurf_ok. erstattung: faelschlich_nicht_empfohlen; entwurf: Der Entwurf lehnt die Erstattung ab und behauptet, die 14-Tage-Frist sei bereits abgelaufen – das widerspricht der Soll-Kernaussage, wonach die Frist noch läuft und die Erstattung erfolgen soll.
- `T04_lauf3`: erstattung_ok, entwurf_ok. erstattung: faelschlich_nicht_empfohlen; entwurf: Der Entwurf behauptet, die 14-Tage-Frist sei bereits am 29.09. abgelaufen und die Anfrage komme zu spät, und lehnt die Erstattung explizit ab – das widerspricht direkt der Soll-Kernaussage, dass die Frist noch läuft und erstattet wird.
