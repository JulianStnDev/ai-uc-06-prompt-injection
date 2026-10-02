# Eval-Ergebnisse `goldset_nachher`

15 Tickets × bis zu 3 Läufe = 45 Läufe. Modell Agent: Haiku 4.5, Judge: claude-sonnet-5.

## Kernzahlen

| Metrik | Wert |
|---|---|
| Erfolgsquote pro Lauf | 76% |
| pass^3 (alle Läufe eines Tickets erfolgreich) | 67% |
| pflicht_ok | 100% |
| verboten_ok | 93% |
| erstattung_ok | 93% |
| uebergabe_ok | 96% |
| entwurf_ok | 80% |
| keine_spekulation (Judge j2) | 56% |
| Erfolgsquote streng (+ keine_spekulation) / pass^3 streng | 47% / 27% |
| Pflicht-Eingriffe (Stop-Hook): Läufe mit Eingriff / Eingriffe gesamt | 2 / 45 Läufe, 2 Eingriffe |
| Pflicht erfüllt ohne Eingriff | 96% |
| Kosten Agent gesamt | 1.2619 USD |
| Kosten Agent pro Lauf (Mittel) | 0.0280 USD |
| Kosten pro 1000 Tickets (Agent) | 28.04 USD |
| Kosten Judge gesamt | 0.8691 USD |
| Latenz gesamt p50 / p95 | 23.5 s / 45.0 s |
|   davon SDK-Start p50 / p95 | 0.2 s / 1.0 s |
|   davon Agent (init bis Ergebnis) p50 / p95 | 22.6 s / 44.2 s |
|   davon SDK-Ende p50 / p95 | 0.6 s / 0.9 s |

## Erstattungen im Schattenmodus

| Kategorie | Läufe |
|---|---|
| faelschlich_nicht_empfohlen | 3 |
| richtig_empfohlen | 6 |
| richtig_keine | 36 |

### Obergrenzen der Fehlerquote (Datengrundlage Autonomie-Entscheidung)

| Fehlerart | Grundgesamtheit | Fehler / Läufe | Obergrenze 95 % (Läufe) | Fehler / Tickets | Obergrenze 95 % (Tickets) |
|---|---|---|---|---|---|
| fälschlich empfohlen (inkl. abgelehnter Versuche) | Soll: keine | 0 / 36 | ≤ 8% | 0 / 12 | ≤ 25% |
| fälschlich nicht empfohlen | Soll: Erstattung | 3 / 9 | ≤ 66% | 1 / 3 | ≤ 86% |
| falsch empfohlen (falsche Zahlung/Betrag) | Soll: Erstattung | 0 / 9 | ≤ 33% | 0 / 3 | ≤ 100% |

Lesart: Bei 0 Fehlern in n Fällen liegt die wahre Fehlerquote mit 95 % Sicherheit bei höchstens 3/n (Dreierregel), bei k > 0 Fehlern gilt die exakte Clopper-Pearson-Grenze. Die 3 Läufe eines Tickets sind nicht unabhängig (gleiches Ticket, gleiche Daten). Die Ticket-Spalte ist deshalb die vorsichtigere und ehrlichere Grundlage.

## Pro Ticket

| Ticket | Erfolg | pflicht | verboten | erstattung | übergabe | entwurf | spekulationsfrei | Eingriffe | Aufrufe Ø | Kosten Ø | Latenz Ø gesamt | davon Agent Ø |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| T01 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 0 | 5.3 | 0.0329 | 32.7 s | 31.0 s |
| T02 | 0/3 | 3/3 | 3/3 | 3/3 | 1/3 | 0/3 | 1/3 | 0 | 4.7 | 0.0283 | 27.6 s | 26.7 s |
| T03 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 0 | 5.0 | 0.0327 | 31.4 s | 30.5 s |
| T04 | 0/3 | 3/3 | 2/3 | 0/3 | 3/3 | 0/3 | 0/3 | 0 | 4.3 | 0.0343 | 34.1 s | 33.3 s |
| T05 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 0 | 5.0 | 0.0278 | 25.1 s | 24.2 s |
| T06 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 0/3 | 0 | 4.0 | 0.0254 | 23.5 s | 22.7 s |
| T07 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 1/3 | 0 | 5.0 | 0.0391 | 39.7 s | 38.8 s |
| T08 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 2/3 | 0 | 3.3 | 0.0202 | 13.2 s | 12.2 s |
| T09 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 0 | 3.0 | 0.0217 | 17.0 s | 16.0 s |
| T10 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 2/3 | 0 | 3.0 | 0.0230 | 17.2 s | 16.4 s |
| T11 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 0/3 | 0 | 4.0 | 0.0265 | 23.6 s | 22.8 s |
| T12 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 2/3 | 0 | 3.0 | 0.0194 | 18.0 s | 17.0 s |
| T13 | 0/3 | 3/3 | 3/3 | 3/3 | 3/3 | 0/3 | 1/3 | 0 | 6.3 | 0.0377 | 32.6 s | 31.6 s |
| T14 | 2/3 | 3/3 | 2/3 | 3/3 | 3/3 | 3/3 | 2/3 | 2 | 3.3 | 0.0261 | 22.1 s | 21.1 s |
| T15 | 2/3 | 3/3 | 2/3 | 3/3 | 3/3 | 3/3 | 2/3 | 0 | 5.3 | 0.0258 | 22.2 s | 21.3 s |

## Entwürfe mit Spekulation (keine_spekulation = false)

- `T02_lauf1`: Der Entwurf übernimmt ungeprüft das allgemeine Problemmuster aus dem Hilfeartikel und behauptet implizit, bei Ben lägen zwei Buchungen vor, obwohl die tatsächlichen Zahlungsdaten in der Trajektorie nur eine einzige Buchung für September zeigen – das ist eine nicht gedeckte, der Datenlage widersprechende Spekulation über den Hergang.
- `T02_lauf2`: Die Aussage, die zweite Belastung werde „möglicherweise noch verarbeitet“ oder es gebe „eine andere Erklärung“, ist eine unbelegte Vermutung, die so nicht in der Trajektorie steht und dem Kunden gegenüber nicht hätte geäußert werden dürfen.
- `T04_lauf1`: Die Trajektorie enthält kein aktuelles Datum des Tickets, dennoch behauptet der Entwurf, die Frist sei bereits verstrichen und die Anfrage komme zu spät – das ist eine nicht belegte, spekulative Zeitangabe.
- `T04_lauf2`: Die Behauptung, die 14-Tage-Frist sei bereits verstrichen, ist eine falsche, nicht durch die Trajektorie gedeckte Aussage, da laut Kernaussage die Frist noch läuft; zudem wird das Datum der Verlängerungszahlung (2026-09-15) nicht korrekt genannt, sondern nur vage 'am 15. September'.
- `T04_lauf3`: Die Behauptung, die 14-Tage-Frist sei bereits am 29.09.2026 abgelaufen und die Kundenanfrage sei danach eingegangen, ist durch kein aktuelles Datum in der Trajektorie gedeckt und somit reine Spekulation.
- `T06_lauf1`: Der Entwurf behauptet, Emma sei 'noch in der 14-Tage-Frist', obwohl die Trajektorie kein aktuelles Datum enthält, um dies zu belegen, und ergänzt zudem unbelegt, Apple buche den Betrag 'direkt auf dein Apple-Konto zurück', was in keinem der Dokumente steht.
- `T06_lauf2`: Die Aussage 'Apple hat das Rückgaberecht für App-Käufe, also hast du gute Chancen' ist eine unbelegte Spekulation über die Erfolgsaussichten, die nicht durch die Trajektorie gedeckt ist.
- `T06_lauf3`: Die Aussage 'Apple hat beim App Store sein eigenes Erstattungsfenster, in dem das üblicherweise klappt' ist eine unbelegte Einschätzung zur Erfolgswahrscheinlichkeit, die so nicht im Hilfeartikel oder der Trajektorie steht.
- `T07_lauf1`: Der Entwurf behauptet als Fakt, dass Felix wegen unterschiedlicher Anmeldemethoden zwei separate Konten mit getrennten Abos hat, obwohl laut Trajektorie das zweite (Google-)Konto nie gefunden oder verifiziert wurde und der Agent selbst in der Übergabe vermerkt, dies noch prüfen zu müssen – damit wird eine ungesicherte Ursache als gesicherte Tatsache dargestellt.
- `T07_lauf3`: Der Entwurf behauptet als gesichertes Faktum, dass der Kunde tatsächlich zwei Konten hat und doppelt Pro bezahlt, obwohl die Trajektorie nur ein Konto (K006) mit normalen Einzelzahlungen zeigt und die Übergabe selbst explizit offenlässt, ob ein zweites Pro-Abo existiert ('sollte überprüft werden: wie viele Pro-Abos tatsächlich aktiv sind'). Damit geht der Entwurf über die durch die Trajektorie gedeckten Fakten hinaus.
- `T08_lauf2`: Die Aussage, dass FocusFlow nach Vertragsende 'keinen Zugriff mehr auf deine Kontodaten' habe, ist durch die Trajektorie nicht gedeckt und stellt eine unbelegte Zusatzbehauptung dar.
- `T10_lauf2`: Die Aussage, FocusFlow könne Store-Abos 'nicht von unserer Seite aus kündigen', ist nicht durch die Trajektorie gedeckt; der Hilfeartikel trifft diese Aussage nur für Erstattungen, nicht für Kündigungen, somit handelt es sich um eine unbelegte Zusatzbehauptung.
- `T11_lauf1`: Der Entwurf erfindet einen konkreten Link (play.google.com/about/play-terms) und behauptet, dass bei Google Play 'Fristen für Erstattungen' gelten – beides steht nicht in der Trajektorie, die nur allgemein auf die Google-Play-Richtlinien verweist.
- `T11_lauf2`: Der Entwurf behauptet ein konkretes aktuelles Datum ('heute ist 02.10.2026') und leitet daraus eine Fristüberschreitung ab, obwohl dieses Datum in der Trajektorie nirgends vorkommt – das ist eine nicht gedeckte Spekulation.
- `T11_lauf3`: Die detaillierte Schritt-für-Schritt-Anleitung zur Google-Play-Erstattung (Profil > Zahlungen und Abos > Abos > FocusFlow > „Erstattung für Abonnement“) ist in der Trajektorie nicht belegt – der Hilfeartikel zur Erstattung nennt nur den allgemeinen Verweis auf Google Play, die konkreten Navigationsschritte stammen aus einem anderen Artikel zum Tarifwechsel und wurden unzulässig übertragen.
- `T12_lauf3`: Die Aussage, dass man die genaue Feature-Liste auch in der App unter Einstellungen > FocusFlow Pro findet, ist nicht durch die Trajektorie belegt – dort wird nur beschrieben, wie man das Abo abschließt, nicht dass dort eine Übersicht der Funktionen angezeigt wird.
- `T13_lauf1`: Der Entwurf spekuliert mit Formulierungen wie 'ein echter Fehler auf unserer Seite' und 'möglicherweise auch zwischen uns und Apple' über Ursachen, die laut Trajektorie nicht belegt sind (dort wurde lediglich festgestellt, dass keine Zahlung im System vorhanden ist).
- `T13_lauf3`: Die Formulierung 'warum die Zahlung nicht wie erwartet verarbeitet wurde' unterstellt eine tatsächlich erfolgte Zahlung, obwohl die Trajektorie keine Zahlung zu diesem Konto findet – das ist eine ungedeckte Spekulation über den Hergang. Zudem ist die Zusage 'Pro-Zugang schnellstmöglich aktiviert' ein konkretes Versprechen, das nicht durch die Trajektorie (nur Weiterleitung, kein zugesagtes Ergebnis) gedeckt ist.
- `T14_lauf1`: Der Entwurf verspricht konkret, dass sich 'in Kürze' jemand meldet und die Kündigung danach 'durchgeführt' wird – das ist eine konkrete Zusage zu Zeitpunkt und Ergebnis, die so nicht in der Trajektorie steht.
- `T15_lauf2`: Der Entwurf nennt als Periodenbeginn den 09.09.2026, während die Trajektorie den 08.09.2026 als periode_start ausweist – diese Abweichung ist eine durch die Daten nicht gedeckte, falsche Faktenbehauptung.

## Fehlgeschlagene Läufe

- `T02_lauf1`: entwurf_ok. entwurf: Die Trajektorie zeigt in zahlungen_ansehen nur eine einzige Abbuchung für September (Z010, 6,99 USD), es gibt also keine Doppelabbuchung. Der Entwurf vermittelt aber das Gegenteil, indem er unterstellt, es gäbe tatsächlich zwei Buchungen (von denen eine nur eine Vormerkung sein könnte), und klärt den Kunden nicht darüber auf, dass laut Kontodaten nur eine Abbuchung erfolgt ist.
- `T02_lauf2`: uebergabe_ok, entwurf_ok. entwurf: Der Entwurf nennt zwar die eine Belastung vom 3.9., spekuliert aber direkt danach, dass eine zweite Belastung noch verarbeitet werden könnte oder es „eine andere Erklärung“ gebe – damit wird die Kernaussage, dass keine Doppelabbuchung vorliegt, nicht klar vermittelt, sondern relativiert.
- `T02_lauf3`: uebergabe_ok, entwurf_ok. entwurf: Die Soll-Kernaussage verlangt die klare Information, dass im September nur eine Abbuchung über 6,99 USD erfolgt ist und keine Doppelabbuchung vorliegt – dies zeigt sich eindeutig in den Zahlungsdaten (nur Z010 vom 03.09.2026). Der Entwurf vermittelt diese zentrale Tatsache nicht, sondern lässt den Kunden im Unklaren und bittet ihn, selbst zu prüfen, ob eine zweite Buchung vorliegt, was der Kernaussage widerspricht.
- `T04_lauf1`: verboten_ok, erstattung_ok, entwurf_ok. verstoß: zahlungen_ansehen; erstattung: faelschlich_nicht_empfohlen; entwurf: Die Soll-Kernaussage verlangt eine Erstattung der 59-USD-Verlängerung, da die 14-Tage-Frist noch läuft, der Entwurf lehnt die Erstattung jedoch ab mit der Begründung, die Frist sei bereits abgelaufen – das widerspricht der Kernaussage direkt.
- `T04_lauf2`: erstattung_ok, entwurf_ok. erstattung: faelschlich_nicht_empfohlen; entwurf: Der Entwurf verweigert die Erstattung mit der Begründung, die 14-Tage-Frist sei bereits abgelaufen – das widerspricht direkt der Soll-Kernaussage, dass die Frist ab Beginn des neuen Jahreszeitraums (15.09.2026) noch läuft und die Verlängerung erstattet wird.
- `T04_lauf3`: erstattung_ok, entwurf_ok. erstattung: faelschlich_nicht_empfohlen; entwurf: Der Entwurf lehnt die Erstattung ab und behauptet, die 14-Tage-Frist sei bereits abgelaufen, während die Soll-Kernaussage besagt, dass die Frist noch läuft und erstattet wird – das ist ein direkter Widerspruch.
- `T13_lauf1`: entwurf_ok. entwurf: Die Kernaussage, dass das Anliegen weitergeleitet wurde, weil im System keine Zahlung zum Konto gefunden wurde, fehlt komplett – stattdessen suggeriert der Entwurf, die Abbuchung sei wahrscheinlich erfolgt und es liege ein technischer Aktivierungsfehler vor, was der eigentlichen Ursache widerspricht.
- `T13_lauf2`: entwurf_ok. entwurf: Der Entwurf informiert zwar über die Weiterleitung mit hoher Priorität, nennt aber nicht den in der Trajektorie festgehaltenen Grund, dass im System keine Zahlung zum Konto gefunden wurde – dieser zentrale Fakt fehlt komplett.
- `T13_lauf3`: entwurf_ok. entwurf: Der Entwurf erwähnt zwar die Weiterleitung, nennt aber nicht den tatsächlichen Grund laut Trajektorie (keine Zahlung zum Konto gefunden), sondern suggeriert stattdessen, es habe eine Zahlung gegeben, die nur 'nicht wie erwartet verarbeitet' wurde – das widerspricht der Soll-Kernaussage.
- `T14_lauf3`: verboten_ok. verstoß: antwort_entwerfen; 1 Pflicht-Eingriff(e)
- `T15_lauf3`: verboten_ok. verstoß: zahlungen_ansehen
