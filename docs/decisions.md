# Entscheidungen

<!-- Format:
## YYYY-MM-DD: Kurztitel
Kontext, Optionen, Entscheidung, Begründung
-->

## 2026-09-18: Status-Vokabular für meta.json

Kontext: meta.json legt "status": "planned" fest, ohne definierte erlaubte Werte —
das driftet über mehrere Repos auseinander (planned/in-progress/wip/...).

Optionen: (a) einfach: planned → active → done, (b) zusätzlich mit
parked/abandoned für verworfene Use Cases, (c) feiner: research →
building → evaluating → shipped.

Entscheidung: (a) — planned, active, done. Zusätzlich in CLAUDE.md verankert.

Begründung: Bei einem Solo-Portfolio mit meist einem aktiven Repo lohnt sich
keine feinere Staffelung. CLAUDE.md-Verankerung, damit der Agent das Vokabular
bei jedem neuen Repo automatisch mitliest statt dass ich mich erinnern muss.

## 2026-10-02: Ziel ist der live laufende UC7-Agent, Verteidigungen als PRs in UC7

Kontext: UC6 soll Prompt Injection und Guardrails zeigen. Ein eigener Spielzeug-Agent wäre schnell gebaut, aber jede
Verteidigung daran bliebe folgenlos.

Optionen: (a) eigener kleiner Agent nur für UC6, (b) den UC7-Agent angreifen, Verteidigungen in UC7 einbauen.

Entscheidung: (b). Dieses Repo enthält Bedrohungsmodell, Testfälle, Messskripte und Ergebnisse. Verteidigungen kommen
als eigene PRs ins UC7-Repo. Jede Messung nennt den UC7-Commit, gegen den sie lief.

Begründung: Der UC7-Agent ist echt deployt, hat echte Schutzschichten (Schattenmodus, Variante A, Kostendeckel) und
seine Entscheidungen von 2026-09-28 nennen Prompt Injection ausdrücklich als offenes Thema für UC6.

## 2026-10-02: Branch (a) nur Bedrohungsmodell, aus dem Code, ohne API

Entscheidung: Branch (a) liest den UC7-Code (Commit `2c8cc86`) und schreibt das Bedrohungsmodell. Keine API-Aufrufe,
keine Änderung an UC7. Fundstellen als Permalinks auf den Commit, damit sie auch nach Verteidigungs-PRs stimmen.

Begründung: Erst wissen, wo die Schichten wirklich stehen, dann Testfälle gezielt dorthin legen. Beim Lesen hat sich
gezeigt, dass das wichtig ist: Die Identitätsprüfung („nur für das Konto des Absenders handeln“) steckt nicht in einem
Hook, sondern nur im Prompt.

## 2026-10-02: Schaden bewerten, als wäre der Betrieb echt

Kontext: In der Demo sind alle Kunden fiktiv und nichts wird gebucht. Streng bewertet wäre fast jeder Schaden
„niedrig“.

Entscheidung: Der Schaden in der Matrix wird für den gedachten echten Betrieb bewertet. Wo die Demo anders ist, steht
es dabei.

Begründung: UC7 ist mit dem Schattenmodus ausdrücklich die Vorstufe zum echten Betrieb. Ein Bedrohungsmodell, das
alles für harmlos erklärt, priorisiert nichts.

## 2026-10-02: Tests lokal gegen den UC7-Code, nicht gegen die Live-URL

Optionen: (a) Angriffe über die öffentliche URL mit einem persönlichen Link, (b) lokal mit dem UC7-Code und eigenen
Daten- und Artikelordnern.

Entscheidung: (b), endgültig festgelegt in Branch (b).

Begründung: Über die Live-URL verbrauchen Tests den Monatsdeckel der Demo (4,50 USD) und landen in der Statistik der
Konsole. Lokal lässt sich außerdem Kategorie K3 (versteckte Anweisungen in Daten) testen, ohne UC7 zu ändern: Der
Werkzeugkasten nimmt eigene Ordner für Daten und Hilfeartikel an.

Offen: UC5 hat seine Angriffsdemo mit dem Modell nach UC6 verschoben (UC5, docs/decisions.md, 30.09.2026). Ob UC6
auch den Text-to-SQL-Copiloten angreift, entscheide ich nach den UC7-Messungen.

## 2026-10-02: Scope ist das echte Produkt, nicht die Portfolio-Demo

Kontext: Die erste Fassung des Bedrohungsmodells mischte Produkt und Demo. Demo-Themen (Besucher mit Link, Bots,
Besucher als Freigeber) standen gleichberechtigt in der Matrix und verschoben die Prioritäten.

Entscheidung: UC6 betrachtet das echte FocusFlow-Produkt. Angreifer ist ein eingeloggter Kunde (Absender durch den Login
fest) oder jemand, der Text in Daten platzieren kann, die der Agent liest. Demo-Spezifisches (Kundenauswahl im
Formular, persönliche Links, Bots und Denial of Wallet über die Demo, Besucher als Freigeber in der Konsole, Rohdaten
in der Zeitleiste) steht in einem eigenen Abschnitt „Demo-spezifisch, bewusst ausgeklammert“ und zählt nicht in die
Matrix. B12 (verfälschte Schattenmodus-Daten) ist ganz dorthin gewandert. B7 heißt im Produkt nur noch „ein Ticket wird
teuer“. B10 (vergiftete Daten) steigt auf Priorität 2, weil im Produkt Kunden Teile ihrer Daten selbst bestimmen.

Begründung: Verteidigungen sollen das Produkt sicherer machen. Eine Matrix, die von Demo-Eigenheiten geprägt ist,
würde die falschen Lücken zuerst schließen.

## 2026-10-02: Abbruch durch einen Sicherheitsfilter beim Ausformulieren der Angriffe

Was passiert ist: Beim Ausformulieren der Testfälle für Branch (b), also der konkreten Angriffstexte für die
Kategorien K1 bis K3, hat ein Sicherheitsfilter die Antwort abgebrochen. Vorgabe war, in diesem Fall nicht
umzuformulieren, sondern zu stoppen und zu melden. So ist es geschehen. Danach war nichts geschrieben: keine Datei,
kein Commit, keine `.env`, kein API-Aufruf, keine Kosten. UC7 war unverändert.

Folge: siehe nächster Eintrag.

## 2026-10-02: Von „Angriffe messen“ zu „Schutz im Code beweisen“

Kontext: Geplant war, Angriffe auszuformulieren (K1 bis K3, je 8/8, 8/8, 6/6 mit Kontrollfällen, 3 Läufe je Fall) und
die Angriffs-Erfolgsquote zu messen. Das scheitert am Sicherheitsfilter. Es wäre auch inhaltlich die schwächere Frage:
Eine Erfolgsquote misst vor allem, wie gut der Prompt hält, also genau die Schicht, auf die wir uns nicht mehr
verlassen wollen.

Optionen: (a) Angriffstexte umformulieren, bis der Filter nicht mehr greift, (b) fertige Angriffssammlungen von
außen übernehmen, (c) keine Angriffstexte, stattdessen die Lücken im Code schließen und deterministisch belegen.

Entscheidung: (c). UC6 schreibt keine Angriffstexte. Die Lücken aus der Matrix werden im UC7-Code geschlossen
(Konto-Bindung per Hook, Erstattungsregeln im Werkzeug, Prüfung von Entwürfen ohne Empfehlung, Konsole gegen
Automation Bias). Jede Lücke bekommt mindestens einen Test ohne API, der Werkzeug oder Hook direkt mit dem Aufruf
aufruft, den ein erfolgreicher Angriff erzeugen würde: vorher wäre er durchgekommen, jetzt wird er blockiert. Der
Nutzen wird mit dem UC4-Goldset (15 Tickets) nach dem Umbau geprüft. Keine harmlose Anfrage darf neu blockiert werden.

Begründung: (a) widerspricht der Vorgabe und dem Zweck des Filters. (b) bringt fremde Texte ins Repo, deren Inhalt ich
nicht verantworte, und misst weiter den Prompt. (c) beweist Schutz, der nicht vom Modell abhängt: Egal, wie ein
Angreifer das Modell überredet, der Aufruf mit fremder `kunden_id` oder eine regelwidrige Empfehlung kommt nicht durch.
Die Tests sind reproduzierbar und kosten nichts. Preis: Wie oft das Modell auf Angriffe hereinfällt, wissen wir nicht.
Für Lücken, die der Code nicht schließen kann (Ton, zweite Ordnung im Antwort-Modell, Text aus vergifteten Daten),
bleibt das Restrisiko und wird in der Matrix so benannt.

Damit überholt: die Testkategorien K1 bis K5 und die Erfolgsdefinitionen aus der ersten Fassung des
Bedrohungsmodells. Weiter gültig: Tests laufen lokal gegen den UC7-Code, nicht gegen die Live-Demo.

## 2026-10-02: T13 als Streuung gewertet, keine weiteren Läufe

Kontext: T13 schafft im Goldset nachher 0 von 3, in der Gegenprobe mit altem Code (`2c8cc86`, gleiche Umgebung) 3 von 3.
Kein Schutz hat in T13 eingegriffen.

Optionen: (a) T13 als offene Einschränkung führen und mit mehr Läufen klären (ca. 1 USD), (b) als Streuung werten.

Entscheidung: (b). Weil das Modell auf beiden Ständen identischen Input bekommt (Prompt, Werkzeuge, Ergebnisse
byte-gleich, kein Hook), kann der Code den Unterschied nicht verursachen. Geprüft: Werkzeugbeschreibungen
(`uc4_agent/mcp_server.py`) und System-Prompts sind zwischen `2c8cc86` und `5c9c262` unverändert; die Werkzeug-Ergebnisse
aller sechs Läufe sind byte-gleich.

Folge: Der Satz „Schutz kostet 1 Lauf (Fehlalarm, behoben), 1 Lauf ist ein echter Fund, Rest nicht durch den Schutz
verursacht“ ist gedeckt und steht in Matrix und README.
