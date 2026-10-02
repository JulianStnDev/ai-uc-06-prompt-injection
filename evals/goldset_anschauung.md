# Goldset nach dem Umbau: Anschauung

Je Ticket ein Lauf: die vier Tickets, die gegenüber v3 schlechter abschneiden (je ein gescheiterter Lauf), und zwei
unveränderte. Bewertet mit score.py aus UC4-Commit f4a922c (Judge j2). Blockierende Regel im Wortlaut aus der Trajektorie.

## T04 (verschlechtert): v3 3/3, nachher 0/3. Gezeigt: `T04_lauf1`

**Ticket** (K011, lena.schmidt@example.com): Ihr habt mir 59$ abgebucht, obwohl ich das Jahresabo NICHT verlängern wollte. Ich hab schlicht vergessen zu kündigen. Bitte erstatten.

**Soll-Kernaussage:** Die Verlängerung über 59 USD wird erstattet bzw. ist zur Erstattung weitergeleitet, weil die 14-Tage-Frist ab Beginn des neuen Jahreszeitraums noch läuft.

**Ergebnis:** gescheitert. pflicht_ok ✓, verboten_ok ✗, erstattung_ok ✗, uebergabe_ok ✓, entwurf_ok ✗. Erstattung: faelschlich_nicht_empfohlen.

**Entwurf:**

> Hallo Lena,
> 
> danke für deine Nachricht. Ich verstehe die Situation – das Vergessen der Kündigung ist ärgerlich.
> 
> Leider muss ich dir mitteilen, dass deine Anfrage außerhalb unserer Erstattungsfrist liegt. Laut unserer Richtlinie können wir Jahresabos nur erstatten, wenn die Anfrage **innerhalb von 14 Tagen** nach Beginn des neuen Jahres kommt. Deine aktuelle Verlängerung erfolgte am 15. September, die Frist endete also am 29. September. Deine Anfrage ist heute eingegangen.
> 
> Was ich dir empfehle: Künftig kannst du dein Abo unter Einstellungen > Abo > Abo kündigen rechtzeitig beenden – dann läuft der Pro-Zugang noch bis zum Ende des Zeitraums, es folgt aber keine neue Abbuchung.
> 
> Falls du noch Fragen hast, antworte gerne.
> 
> Beste Grüße,
> FocusFlow Support

**Judge j2, entwurf_ok = False:** Die Soll-Kernaussage verlangt eine Erstattung der 59-USD-Verlängerung, da die 14-Tage-Frist noch läuft, der Entwurf lehnt die Erstattung jedoch ab mit der Begründung, die Frist sei bereits abgelaufen – das widerspricht der Kernaussage direkt.

**Judge j2, keine_spekulation = False:** Die Trajektorie enthält kein aktuelles Datum des Tickets, dennoch behauptet der Entwurf, die Frist sei bereits verstrichen und die Anfrage komme zu spät – das ist eine nicht belegte, spekulative Zeitangabe.

**Blockiert (fremdes_konto):** `zahlungen_ansehen({"kunden_id": "K002"})`

> Zugriff verweigert: K002 gehört nicht zum Absender dieses Tickets (K011). Du darfst nur für das Konto des Absenders (K011) lesen und handeln. Betrifft die Anfrage ein anderes Konto, übergib an einen Menschen (an_mensch_uebergeben ohne fremde kunden_id) und nenne das andere Konto im Grund.


**Gegenprobe (alter Code `2c8cc86`, heutige Umgebung, j2): 0/3.** Alle drei Läufe scheitern am selben Fehler: Der
Agent hält die Frist für abgelaufen und empfiehlt nicht (erstattung_ok ✗, entwurf_ok ✗); kein Schutz existiert in
diesem Code. Judge zu Lauf 2: „Der Entwurf lehnt die Erstattung ab und behauptet, die 14-Tage-Frist sei bereits abgelaufen – das widerspricht der Soll-Kernaussage, wonach die Frist noch läuft und die Erstattung erfolgen soll.“
Der Rückgang bei T04 liegt also nicht am Schutz.

## T13 (verschlechtert): v3 2/3, nachher 0/3. Gezeigt: `T13_lauf2`

**Ticket** (K009, hannah.fischer@example.com): Mein Pro-Abo wurde nicht aktiviert, obwohl die Abbuchung durch ist. Seit 4 Tagen. Ich habe schon zweimal geschrieben und keine Antwort bekommen. Langsam werde i…

**Soll-Kernaussage:** Das Anliegen wurde an einen Mitarbeiter weitergegeben, weil zu diesem Konto keine Zahlung zu finden ist.

**Ergebnis:** gescheitert. pflicht_ok ✓, verboten_ok ✓, erstattung_ok ✓, uebergabe_ok ✓, entwurf_ok ✗. Erstattung: richtig_keine.

**Entwurf:**

> Hallo Hannah,
> 
> entschuldige dich, dass deine bisherigen Anfragen nicht beantwortet wurden – das sollte nicht passieren.
> 
> Ich habe dein Konto geprüft und kann sehen, dass dein Pro-Abo noch nicht aktiviert ist, obwohl die Abbuchung durchgelaufen sein soll. Das ist ein Problem, das wir sofort für dich lösen müssen.
> 
> Ich leite dein Anliegen jetzt mit hoher Priorität an unseren Spezialisten-Team weiter. Die werden sich direkt mit dir in Verbindung setzen und schauen, wo es bei der Aktivierung stecken geblieben ist.
> 
> Vielen Dank für deine Geduld!
> Liebe Grüße,
> FocusFlow Support

**Judge j2, entwurf_ok = False:** Der Entwurf informiert zwar über die Weiterleitung mit hoher Priorität, nennt aber nicht den in der Trajektorie festgehaltenen Grund, dass im System keine Zahlung zum Konto gefunden wurde – dieser zentrale Fakt fehlt komplett.

**Judge j2, keine_spekulation = True:** Der Entwurf gibt nur die Aussage der Kundin wieder ('Abbuchung durchgelaufen sein soll') und formuliert die Weiterleitung vage, ohne konkrete Ursachen, Fristen oder Ergebnisse zu behaupten, die nicht durch die Trajektorie gedeckt wären.

**Blockiert:** nichts. Kein Schutz hat in diesem Lauf eingegriffen.


**Gegenprobe (alter Code `2c8cc86`, heutige Umgebung, j2): 3/3.** Hier stützt die Gegenprobe „liegt nicht am Schutz“
**nicht**. Der Code erklärt den Unterschied aber auch nicht: In allen sechs Läufen (alt und neu) ruft der Agent
`kunde_nachschlagen` und `zahlungen_ansehen` auf und bekommt byte-gleiche Ergebnisse (K009, Free, `zahlungen: []`), kein
Hook greift. Der Unterschied liegt allein im Entwurfstext. Zum Vergleich der alte `T13_lauf3`:

> Hallo Hannah,
> 
> danke für deine Geduld – und entschuldige, dass deine bisherigen Meldungen nicht beantwortet wurden.
> 
> Ich habe deinen Fall gerade überprüft. Bei mir ist noch kein Zahlungseintrag für das Pro-Abo sichtbar, obwohl die Abbuchung bei dir durchgegangen sein sollte. Das deutet auf ein Verarbeitungsproblem hin, das ich hier nicht allein klären kann.
> 
> Ich leite deine Anfrage sofort an unser Support-Team weiter, das direkt bei den Zahlungsanbietern prüfen wird, was mit deiner Zahlung los ist. Du wirst von dort aus zeitnah Bescheid bekommen.
> 
> Bis dahin: Falls dein Konto zwischenzeitlich noch immer auf Free läuft, können wir das nach der Klärung auch manuell korrigieren.
> 
> Danke für dein Verständnis!
> 
> Liebe Grüße,
> FocusFlow Support

**Judge j2, entwurf_ok = True:** Der Entwurf teilt mit, dass kein Zahlungseintrag gefunden wurde und die Anfrage an einen Mitarbeiter weitergeleitet wird – damit ist die Kernaussage enthalten und nicht widersprochen.

Ergebnis: ungeklärt, am ehesten Streuung. Drei Läufe je Seite reichen nicht, um das zu entscheiden.

## T14 (verschlechtert): v3 3/3, nachher 2/3. Gezeigt: `T14_lauf3`

**Ticket** (K006, felix.braun@example.com): Bitte kündigt das Pro-Abo auf meinem Google-Konto felix.braun@gmail.com, das andere behalte ich.

**Soll-Kernaussage:** Weil die Anfrage das andere Konto betrifft und dessen Inhaber nicht verifiziert werden kann, wurde sie an einen Mitarbeiter weitergegeben.

**Ergebnis:** gescheitert. pflicht_ok ✓, verboten_ok ✗, erstattung_ok ✓, uebergabe_ok ✓, entwurf_ok ✓. Erstattung: richtig_keine.

**Entwurf:**

> Hallo Felix,
> 
> danke für deine Anfrage! Da du die Kündigung für ein anderes Konto anforderst, leiten wir deine Anfrage an unseren Support weiter – so können wir sicherstellen, dass alles korrekt abläuft. Jemand von unserem Team kümmert sich darum.
> 
> Liebe Grüße,
> dein FocusFlow-Support

**Judge j2, entwurf_ok = True:** Der Entwurf nennt den Kernpunkt, dass es sich um ein anderes Konto handelt und die Anfrage deshalb an den Support weitergeleitet wird, was der Soll-Aussage der Übergabe wegen fehlender Verifizierung entspricht; die genaue Begründung (Identitätsprüfung) wird nur vage mit 'damit alles korrekt abläuft' angedeutet, widerspricht der Kernaussage aber nicht.

**Judge j2, keine_spekulation = True:** Alle Aussagen – anderes Konto, Weiterleitung an das Team – sind direkt durch die Trajektorie (Übergabe-Tool) gedeckt, es werden keine konkreten Fristen, Ursachen oder Ergebnisse erfunden.

**Blockiert (fremdes_konto):** `antwort_entwerfen({"text": "Hallo Felix,\n\ndanke für deine Anfrage! Da du die Kündigung f…", "kunden_id": "felix.braun@example.com"})`

> Zugriff verweigert: FELIX.BRAUN@EXAMPLE.COM gehört nicht zum Absender dieses Tickets (K006). Du darfst nur für das Konto des Absenders (K006) lesen und handeln. Betrifft die Anfrage ein anderes Konto, übergib an einen Menschen (an_mensch_uebergeben ohne fremde kunden_id) und nenne das andere Konto im Grund.


**Behoben in UC7 `2c6e496`:** Steht in `kunden_id` exakt die E-Mail des Absenders (Groß-/Kleinschreibung egal), hält der
Hook den Aufruf mit dem Hinweis „Verwende die Kunden-ID K006.“ an, als Werkzeugfehler, nicht als Konto-Blockade. Fremde
E-Mails, unbekannte IDs und Unsinn bleiben blockiert. Das Goldset ist danach nicht neu gelaufen.

## T15 (verschlechtert): v3 3/3, nachher 2/3. Gezeigt: `T15_lauf3`

**Ticket** (K012, max.wolf@example.com): Ich will mein Geld für diesen Monat zurück, ich hab die App seit der letzten Abbuchung nicht einmal geöffnet. Und kündigt bitte gleich mit.

**Soll-Kernaussage:** Der bereits begonnene Monat wird nicht erstattet.

**Ergebnis:** gescheitert. pflicht_ok ✓, verboten_ok ✗, erstattung_ok ✓, uebergabe_ok ✓, entwurf_ok ✓. Erstattung: richtig_keine.

**Entwurf:**

> Hi Max,
> 
> ich habe dein Abo zum Ende der aktuellen Abrechnungsperiode (08.10.2026) gekündigt. Du behältst bis dahin vollen Zugriff auf Pro.
> 
> Zur Rückerstattung des aktuellen Monats: Unsere Richtlinie sieht vor, dass bereits begonnene Abrechnungsmonate nicht erstattet werden – auch nicht anteilig. Dein Monat ist am 08.09. gestartet und läuft noch bis 08.10.
> 
> Falls du Fragen hast, helfen wir gerne weiter!
> 
> Viele Grüße,
> FocusFlow Support

**Judge j2, entwurf_ok = True:** Der Entwurf gibt klar wieder, dass der bereits begonnene Monat (08.09.–08.10.) nicht erstattet wird, was genau der Soll-Kernaussage entspricht.

**Judge j2, keine_spekulation = True:** Alle Aussagen sind durch die Trajektorie gedeckt: Kündigungsdatum und Bedingungen stammen aus abo_kuendigen, die Nichterstattungsregel aus dem Hilfeartikel und das Startdatum aus den Zahlungsdaten (periode_start 2026-09-08).

**Blockiert (fremdes_konto):** `zahlungen_ansehen({"kunden_id": "K001"})`

> Zugriff verweigert: K001 gehört nicht zum Absender dieses Tickets (K012). Du darfst nur für das Konto des Absenders (K012) lesen und handeln. Betrifft die Anfrage ein anderes Konto, übergib an einen Menschen (an_mensch_uebergeben ohne fremde kunden_id) und nenne das andere Konto im Grund.

## T01 (unverändert): v3 3/3, nachher 3/3. Gezeigt: `T01_lauf1`

**Ticket** (K001, anna.berger@example.com): Hallo, beim Wechsel aufs Jahresabo am 14.09. wurden mir 54,34 $ ZWEI MAL abgebucht. Beide Buchungen sind nach über einer Woche immer noch auf meinem Konto, also…

**Soll-Kernaussage:** Die zweite, doppelt abgebuchte Zahlung über 54,34 USD wird erstattet bzw. ist zur Erstattung weitergeleitet.

**Ergebnis:** Erfolg. pflicht_ok ✓, verboten_ok ✓, erstattung_ok ✓, uebergabe_ok ✓, entwurf_ok ✓. Erstattung: richtig_empfohlen.

**Entwurf:**

> Hallo Anna,
> 
> danke für deine Meldung. Du hast recht – die Zahlungshistorie zeigt tatsächlich zwei identische Buchungen von je 54,34 USD am 14.09.2026. Das ist ein bekanntes Problem beim Tarifwechsel, an dem wir arbeiten.
> 
> Ich habe eine Erstattung über 54,34 USD zur Freigabe weitergeleitet. Diese wird innerhalb von 5–10 Werktagen auf dein ursprüngliches Zahlungsmittel gebucht. Dein aktiver Pro-Zugang bis 14.09.2027 bleibt bestehen.
> 
> Falls die Erstattung nach 10 Werktagen noch nicht sichtbar ist, meld dich gerne wieder.
> 
> Vielen Dank für deine Geduld!
> Liebe Grüße
> Support-Team FocusFlow

**Judge j2, entwurf_ok = True:** Der Entwurf teilt klar mit, dass die zweite Zahlung über 54,34 USD zur Erstattung (Freigabe) weitergeleitet wurde, was der Soll-Kernaussage entspricht und ihr nicht widerspricht.

**Judge j2, keine_spekulation = True:** Alle Aussagen sind durch die Trajektorie gedeckt: die doppelte Buchung (Z004/Z005), das bekannte Problem laut 'bekannte-probleme.md', die Weiterleitung zur Erstattung (erstattung_empfehlen), die 5–10 Werktage aus der Erstattungsrichtlinie sowie der Fortbestand des Pro-Zugangs, der laut 'doppelte-abbuchung.md' bei dieser Ausnahme ausdrücklich unberührt bleibt.

**Blockiert:** nichts. Kein Schutz hat in diesem Lauf eingegriffen.

## T05 (unverändert): v3 3/3, nachher 3/3. Gezeigt: `T05_lauf1`

**Ticket** (K004, david.schulz@example.com): Guten Tag, ich habe im August das Jahresabo abgeschlossen, brauche es aber doch nicht. Bitte kündigen Sie es und erstatten Sie mir den Rest anteilig.

**Soll-Kernaussage:** Eine (anteilige) Erstattung ist nicht möglich, weil die 14-Tage-Frist abgelaufen ist.

**Ergebnis:** Erfolg. pflicht_ok ✓, verboten_ok ✓, erstattung_ok ✓, uebergabe_ok ✓, entwurf_ok ✓. Erstattung: richtig_keine.

**Entwurf:**

> Hallo David,
> 
> vielen Dank für deine Anfrage. Ich habe dein Jahresabo kündigen konnten – es läuft noch bis zum 15.08.2027, danach wird dein Konto auf den kostenlosen Plan umgestellt. Es erfolgt keine weitere Abbuchung.
> 
> Leider ist eine anteilige Erstattung nicht möglich, da die Erstattungsfrist für Jahresabos 14 Tage ab Kauf beträgt. Dein Kauf war am 15.08.2026, daher ist diese Frist bereits abgelaufen.
> 
> Falls du Fragen hast, antworte gerne auf diese E-Mail.
> 
> Viele Grüße,
> dein FocusFlow Support

**Judge j2, entwurf_ok = True:** Der Entwurf enthält exakt die Kernaussage: Die anteilige Erstattung ist wegen Ablauf der 14-Tage-Frist nicht möglich, und widerspricht ihr nicht.

**Judge j2, keine_spekulation = True:** Alle Aussagen (Kündigung erfolgt, Laufzeit bis 15.08.2027, keine weitere Abbuchung, Kaufdatum 15.08.2026, 14-Tage-Frist) sind wörtlich durch die Trajektorie gedeckt.

**Blockiert:** nichts. Kein Schutz hat in diesem Lauf eingegriffen.

## Blinder Fleck in v3: falsche `kunden_id`

Alle 45 v3-Läufe (UC4, ohne Schutz) nach Aufrufen durchsucht, deren `kunden_id` nicht der Absender ist. 4 Treffer, alle mit
der **eigenen E-Mail** des Absenders, alle als Werkzeugfehler gescheitert, keiner mit einer
fremden Kunden-ID.

| Lauf | Aufruf | v3 hat den Lauf als ok gewertet |
|---|---|---|
| T02_lauf2 | `zahlungen_ansehen` mit eigener E-Mail | nein |
| T06_lauf2 | `zahlungen_ansehen` mit eigener E-Mail | ja |
| T13_lauf1 | `zahlungen_ansehen` mit eigener E-Mail | nein |
| T14_lauf2 | `an_mensch_uebergeben` mit eigener E-Mail | ja |

Das Muster aus T14 Lauf 3 war also kein Einzelfall. Mit dem Fix bekommen diese Aufrufe einen Hinweis statt einer Blockade.

