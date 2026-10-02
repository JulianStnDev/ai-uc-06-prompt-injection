"""Die neue Konsole lokal ansehen, ohne API und ohne Neon: zwei Fälle aus dem Schutz im Code (UC7, PR #11).

    ../ai-uc-07-deployment/.venv/bin/python scripts/konsole_lokal.py
    # dann im Browser: http://127.0.0.1:8765/login  →  Zugangscode „lokal-konsole“  →  Support console

Läuft mit dem UC7-Code im Nachbarordner (aktueller Checkout, für PR #11 also Branch feat/schutz-im-code). Daten in
einer frischen SQLite-Datei unter --daten (Standard: ein Temp-Ordner), nie in Neon: DATABASE_URL bleibt leer, und die
UC7-.env wird nicht geladen. Statt des Modells spielt ein festes Drehbuch zwei Läufe ab. Jeder Werkzeugaufruf geht
durch den echten PreToolUse-Hook aus agent.baue_optionen; was der Hook ablehnt, wird nicht ausgeführt. Judge und
Antwort-Schreiber sind Platzhalter ohne API. Kein Angriffstext: beide Tickets sind gewöhnliche Kundenanfragen.

Fall „Zusage ohne Empfehlung“: Ben (K002) meldet eine doppelte Abbuchung. Der Agent empfiehlt nichts, schreibt aber
einen Satz aus einem echten UC4-Entwurf, der eine Erstattung zusagt.
Fall „blockiert“: Anna (K001) meldet eine doppelte Abbuchung. Der Agent fragt zuerst die Zahlungen von K009 ab (wie
T15 im Goldset mit K001), der Hook blockiert, danach empfiehlt er korrekt Z005.

--screenshots ORDNER legt zusätzlich konsole.png, kunde_ben.png und fall_anna.png ab (headless Chrome).
"""

import argparse
import os
import subprocess
import sys
import tempfile
from pathlib import Path

HIER = Path(__file__).resolve().parent.parent
UC7 = HIER.parent / "ai-uc-07-deployment"
CODE = "lokal-konsole"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

BEN_TEXT = "Hallo, mir wurden im September die 6,99 USD zweimal abgebucht. Könnt ihr das prüfen?"
BEN_ENTWURF = ("Hallo Ben,\n\ndanke für deine Nachricht. Ich habe mir deine Zahlungen angesehen und sehe für September "
               "nur eine Buchung. Dann erstatten wir dir den doppelt belasteten Betrag sofort.\n\nViele Grüße\nFocusFlow Support")
ANNA_TEXT = "Hallo, mir wurden die 54,34 USD für das Jahresabo doppelt abgebucht. Bitte erstattet mir eine Buchung."
ANNA_ENTWURF = ("Hallo Anna,\n\ndanke für deine Nachricht. Die doppelte Buchung über 54,34 USD ist zur Erstattung "
                "weitergeleitet. Ein Mitarbeiter prüft sie, du bekommst danach Bescheid.\n\nViele Grüße\nFocusFlow Support")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--daten", help="Ordner für die SQLite-Datei (Standard: neuer Temp-Ordner)")
    ap.add_argument("--screenshots", help="Ordner für die Screenshots (PNG)")
    a = ap.parse_args()

    os.environ.pop("DATABASE_URL", None)
    os.environ["ANTHROPIC_API_KEY"] = "sk-ant-lokal-platzhalter"  # das Drehbuch ruft nie die API
    sys.path.insert(0, str(UC7))
    import app.main as web
    web.load_dotenv = lambda *x, **k: None  # nicht die UC7-.env (dort stehen Key und Neon-URL)
    from app.einstellungen import Einstellungen
    from claude_agent_sdk import AssistantMessage, ResultMessage, TextBlock
    from fastapi.testclient import TestClient
    from uc4_agent import agent

    daten = Path(a.daten or tempfile.mkdtemp(prefix="uc7-konsole-"))
    cfg = Einstellungen(zugangscode=CODE, session_secret="lokal", daten_dir=daten, monatsdeckel_usd=4.50,
                        max_parallele_laeufe=1, cookie_secure=False, database_url=None, replay_takt_s=0)

    def drehbuch(prompt, options, kasten):
        hook = options.hooks["PreToolUse"][0].hooks[0]  # derselbe Hook wie im echten Lauf

        async def aufruf(werkzeug, eingabe):
            out = await hook({"tool_name": agent.PREFIX + werkzeug, "tool_input": eingabe}, None, None)
            if out.get("hookSpecificOutput", {}).get("permissionDecision") != "deny":
                kasten.aufrufen(werkzeug, eingabe)

        async def q():
            yield AssistantMessage(content=[TextBlock("Ich schaue mir das Konto an.")], model=agent.MODELL)
            if kasten.absender_id == "K002":
                await aufruf("kunde_nachschlagen", {"suche": "ben.hoffmann@example.com"})
                await aufruf("zahlungen_ansehen", {"kunden_id": "K002"})
                await aufruf("antwort_entwerfen", {"text": BEN_ENTWURF})
            else:
                await aufruf("kunde_nachschlagen", {"suche": "anna.berger@example.com"})
                await aufruf("zahlungen_ansehen", {"kunden_id": "K009"})  # falsches Konto: der Hook blockiert
                await aufruf("zahlungen_ansehen", {"kunden_id": "K001"})
                await aufruf("erstattung_empfehlen", {"kunden_id": "K001", "zahlungs_id": "Z005", "betrag_usd": 54.34,
                                                      "begruendung": "Doppelte Abbuchung am 14.09., gleiche Beschreibung."})
                await aufruf("antwort_entwerfen", {"text": ANNA_ENTWURF})
            yield ResultMessage(subtype="success", duration_ms=1000, duration_api_ms=900, is_error=False, num_turns=6,
                                session_id="lokal", total_cost_usd=0.0, result="Erledigt.")
        return q()

    def judge(ticket, text, ereignisse, entscheidung):
        return {"keine_spekulation": True, "keine_spekulation_begruendung": "Platzhalter (lokal, kein Judge)",
                "keine_zusage": True, "keine_zusage_begruendung": "Platzhalter (lokal, kein Judge)", "judge_version": "lokal",
                "modell": "lokal", "input_tokens": 0, "output_tokens": 0, "kosten_usd": 0.0, "dauer_s": 0.0}

    def antwort(lauf, empfehlungen):
        return {"text": "Platzhalter für die endgültige Antwort (lokal, kein Modell).", "kosten_usd": 0.0,
                "modell": "lokal", "input_tokens": 0, "output_tokens": 0}

    def ohne_zusage(lauf, kommentar):
        return {"text": "Platzhalter: Antwort ohne Zusage (lokal, kein Modell).", "kosten_usd": 0.0, "modell": "lokal",
                "input_tokens": 0, "output_tokens": 0}

    erzeuge = lambda: web.create_app(cfg, query_fn=drehbuch, judge_fn=judge, antwort_fn=antwort, zusage_fn=ohne_zusage)

    # 1. Beide Läufe anlegen, wie im Browser (Formular, dann Laufseite mit Stream)
    with TestClient(erzeuge()) as c:
        c.post("/login", data={"code": CODE})
        laeufe = {}
        for kunde, text in (("K002", BEN_TEXT), ("K001", ANNA_TEXT)):
            r = c.post("/lauf", data={"kunden_id": kunde, "text": text}, follow_redirects=False)
            run_id = r.headers["location"].rsplit("/", 1)[-1]
            with c.stream("GET", f"/lauf/{run_id}/stream") as s:
                for _ in s.iter_lines():
                    pass
            laeufe[kunde] = run_id
        seiten = {"konsole": c.get("/freigaben").text, "kunde_ben": c.get(f"/lauf/{laeufe['K002']}").text,
                  "fall_anna": c.get(f"/lauf/{laeufe['K001']}").text}
    print(f"Daten: {daten}\nLäufe: Ben (Zusage ohne Empfehlung) {laeufe['K002']}, Anna (blockiert) {laeufe['K001']}")

    # 2. Server starten (gleiche SQLite-Datei)
    import uvicorn
    server = uvicorn.Server(uvicorn.Config(erzeuge(), host="127.0.0.1", port=a.port, log_level="warning"))
    if a.screenshots:
        import threading, time
        threading.Thread(target=server.run, daemon=True).start()
        ende = time.time() + 10
        while not server.started:
            if time.time() > ende:
                sys.exit(f"Server startet nicht auf Port {a.port} (belegt? anderen Port mit --port wählen).")
            time.sleep(0.05)
        ziel = Path(a.screenshots).resolve(); ziel.mkdir(parents=True, exist_ok=True)
        for name, html in seiten.items():
            datei = ziel / f"{name}.html"  # mit <base>, damit CSS und Skripte vom laufenden Server kommen
            datei.write_text(html.replace("<head>", f'<head><base href="http://127.0.0.1:{a.port}/">', 1), encoding="utf-8")
            subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--screenshot={ziel / name}.png",
                            "--window-size=1280,1700", "--virtual-time-budget=3000", datei.as_uri()],
                           check=True, capture_output=True)
            datei.unlink()
            print(f"Screenshot: {ziel / name}.png")
        server.should_exit = True
        return
    print(f"Konsole: http://127.0.0.1:{a.port}/login  (Zugangscode „{CODE}“, dann „Support console“). Beenden mit Ctrl+C.")
    server.run()


if __name__ == "__main__":
    main()
