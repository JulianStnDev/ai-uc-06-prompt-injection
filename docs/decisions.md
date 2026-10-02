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
