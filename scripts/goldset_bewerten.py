"""Bewertung des Goldsets nach dem Umbau mit genau dem Lineal von v3: score.py aus UC4-Commit f4a922c (Judge j2).

Die Funktionen von score.py werden unverändert geladen (git show f4a922c:score.py). Die Hauptschleife unten ist die
von score.py main(), mit zwei Unterschieden: Ausgabe nach UC6 (evals/goldset_nachher/) statt ins UC4-Repo, und eine
zusätzliche Spalte „scheitert nur an Konto-Blockade“ (verboten_ok ist das einzige verfehlte Kriterium, und jeder
blockierte Aufruf kam von der Konto-Bindung). Danach der Vergleich je Ticket mit UC4 evals/scores_v3.jsonl (j2).

    ../ai-uc-07-deployment/.venv/bin/python scripts/goldset_bewerten.py

Harte Grenze: Agent-Kosten (lauf_uebersicht.json) + Judge-Kosten bleiben unter --budget; vor jedem Urteil wird der
Höchstbetrag eines Urteils reserviert.
"""

import argparse
import json
import os
import statistics
import subprocess
import sys
import types
from collections import defaultdict
from pathlib import Path

HIER = Path(__file__).resolve().parent.parent
UC4 = HIER.parent / "ai-uc-04-agents-mcp"
SCORE_COMMIT = "f4a922c"
URTEIL_MAX_USD = 0.10  # reichlich: ca. 15k Eingabe-Tokens × 2 USD/Mio. + 4000 Ausgabe-Tokens × 10 USD/Mio.


def score_j2() -> types.ModuleType:
    quelle = subprocess.run(["git", "show", f"{SCORE_COMMIT}:score.py"], cwd=UC4, capture_output=True, text=True,
                            check=True).stdout
    sys.path.insert(0, str(UC4))  # score.py importiert werkzeuge.ROOT aus UC4 (Daten identisch zu UC7, per diff geprüft)
    modul = types.ModuleType("score_j2")
    modul.__file__ = f"{UC4}/score.py@{SCORE_COMMIT}"
    exec(compile(quelle, modul.__file__, "exec"), modul.__dict__)
    assert modul.JUDGE_VERSION == "j2"
    return modul


def env_laden(pfad: Path) -> None:
    for zeile in pfad.read_text(encoding="utf-8").splitlines():
        if "=" in zeile and not zeile.lstrip().startswith("#"):
            k, v = zeile.split("=", 1)
            os.environ[k.strip()] = v.strip().strip('"').strip("'")


def nur_konto_blockade(z: dict, aufgabe: dict, trajektorie: list[dict]) -> bool:
    """Lauf gescheitert, und zwar nur an verboten_ok, und jeder Eintrag, der dort als Verstoß zählt (verbotene Aktion
    oder blockierter Aufruf), ist ein von der Konto-Bindung blockierter Aufruf."""
    if z["erfolg"] or not z["agent_ok"]:
        return False
    verfehlt = [k for k in ("pflicht_ok", "verboten_ok", "erstattung_ok", "uebergabe_ok", "entwurf_ok") if z[k] is False]
    verstoesse = [e for e in trajektorie if e["werkzeug"] in aufgabe["verbotene_aktionen"] or e.get("blockiert")]
    return verfehlt == ["verboten_ok"] and bool(verstoesse) and all(e.get("blockiert_art") == "fremdes_konto" for e in verstoesse)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--laufordner", default=str(HIER / "evals" / "goldset_nachher"))
    ap.add_argument("--budget", type=float, default=8.0)
    ap.add_argument("--urteil-max", type=float, default=URTEIL_MAX_USD, help="Reserve je Judge-Urteil in USD")
    ap.add_argument("--ohne-vergleich", action="store_true", help="nur bewerten, kein Vergleich mit v3")
    a = ap.parse_args()
    s = score_j2()
    laufordner = Path(a.laufordner)
    aufgaben = {t["id"]: t for t in json.loads(s.AUFGABEN.read_text(encoding="utf-8"))["aufgaben"]}
    agent_kosten = json.loads((laufordner / "lauf_uebersicht.json").read_text(encoding="utf-8"))["kosten_usd"]

    env_laden(HIER / ".env")
    import anthropic
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"].strip())

    zeilen, trajektorien, judge_kosten = [], {}, 0.0
    for run_dir in sorted(p for p in laufordner.iterdir() if (p / "lauf.json").exists()):
        lauf = json.loads((run_dir / "lauf.json").read_text(encoding="utf-8"))
        aufgabe = aufgaben[lauf["ticket_id"]]
        trajektorie = s.lese_jsonl(run_dir / "trajektorie.jsonl")
        z = {"run_id": lauf["run_id"], "ticket_id": lauf["ticket_id"], "agent_ok": lauf["subtype"] == "success",
             "prompt_version": lauf.get("prompt_version", "v1"), "eingriffe": lauf.get("eingriffe"),
             "kosten_usd": lauf["kosten_usd"] or 0.0, "dauer_s": lauf["dauer_s"], "num_turns": lauf["num_turns"],
             "sdk_start_s": lauf.get("sdk_start_s"), "agent_s": lauf.get("agent_s"), "sdk_ende_s": lauf.get("sdk_ende_s"),
             **s.bewerte_deterministisch(aufgabe, trajektorie)}
        if z["entwurf"] is None:
            z.update(entwurf_ok=False, entwurf_ok_begruendung="kein Entwurf gespeichert",
                     keine_spekulation=None, keine_spekulation_begruendung="kein Entwurf")
        else:
            judge_pfad = run_dir / f"judge_{s.JUDGE_VERSION}.json"  # Cache: Judge nur einmal pro Lauf und Fassung
            if not judge_pfad.exists():
                if agent_kosten + judge_kosten + a.urteil_max > a.budget:
                    sys.exit(f"Abbruch vor {run_dir.name}: Budget {a.budget:.2f} USD würde überschritten.")
                urteil = s.judge_entwurf(client, aufgabe, z["entwurf"], trajektorie)
                judge_pfad.write_text(json.dumps(urteil, ensure_ascii=False, indent=2), encoding="utf-8")
            z.update(json.loads(judge_pfad.read_text(encoding="utf-8")))
            judge_kosten += z.get("judge_kosten_usd", 0.0)
        z["erfolg"] = z["agent_ok"] and all(z[k] is True for k in s.KRITERIEN if z[k] is not None)
        z["erfolg_streng"] = z["erfolg"] and z.get("keine_spekulation") is True
        z["pflicht_ohne_eingriff"] = z["pflicht_ok"] and not z["eingriffe"]
        # UC6-Zusatz, ändert keine Bewertung:
        z["konto_blockaden"] = sum(e.get("blockiert_art") == "fremdes_konto" for e in trajektorie)
        z["nur_konto_blockade"] = nur_konto_blockade(z, aufgabe, trajektorie)
        zeilen.append(z)
        trajektorien[z["run_id"]] = trajektorie

    with open(laufordner / "scores.jsonl", "w", encoding="utf-8") as f:
        for z in zeilen:
            f.write(json.dumps(z, ensure_ascii=False) + "\n")
    bericht = s.bericht_schreiben(laufordner.name, zeilen, aufgaben, judge=True)
    (laufordner / "results.md").write_text(bericht, encoding="utf-8")
    if a.ohne_vergleich:
        print(f"{sum(z['erfolg'] for z in zeilen)}/{len(zeilen)} erfolgreich, Agent {agent_kosten:.4f} USD, Judge {judge_kosten:.4f} USD")
        return
    (laufordner / "vergleich.md").write_text(vergleich(zeilen, agent_kosten, judge_kosten), encoding="utf-8")
    print(vergleich(zeilen, agent_kosten, judge_kosten))


def vergleich(nachher: list[dict], agent_kosten: float, judge_kosten: float) -> str:
    v3 = [json.loads(z) for z in (UC4 / "evals" / "scores_v3.jsonl").read_text(encoding="utf-8").splitlines()]
    je = lambda zeilen: {t: [z for z in zeilen if z["ticket_id"] == t] for t in sorted({z["ticket_id"] for z in zeilen})}
    a, b = je(v3), je(nachher)
    out = ["# Goldset: v3 gegen „Schutz im Code“", "",
           f"Beide Seiten mit score.py aus UC4-Commit {SCORE_COMMIT} (Judge j2) bewertet. v3: UC4 evals/scores_v3.jsonl. "
           "Nachher: UC7 Commit 945d475, Prompt v3 unverändert.", "",
           "| Ticket | v3 ok | nachher ok | v3 pass^3 | nachher pass^3 | Kosten Ø v3 | Kosten Ø nachher | Läufe mit Konto-Blockade | scheitert nur an Konto-Blockade |",
           "|---|---|---|---|---|---|---|---|---|"]
    for t in sorted(set(a) | set(b)):
        za, zb = a.get(t, []), b.get(t, [])
        ok = lambda zs: f"{sum(z['erfolg'] for z in zs)}/{len(zs)}"
        p3 = lambda zs: "✓" if zs and all(z["erfolg"] for z in zs) else "✗"
        kosten = lambda zs: f"{statistics.mean(z['kosten_usd'] for z in zs):.4f}" if zs else "–"
        out.append(f"| {t} | {ok(za)} | {ok(zb)} | {p3(za)} | {p3(zb)} | {kosten(za)} | {kosten(zb)} | "
                   f"{sum(z['konto_blockaden'] > 0 for z in zb)} | {sum(z['nur_konto_blockade'] for z in zb)} |")
    gesamt = lambda zs, tz: (f"{sum(z['erfolg'] for z in zs)}/{len(zs)}",
                             f"{sum(all(z['erfolg'] for z in v) for v in tz.values())}/{len(tz)}")
    (va, pa), (vb, pb) = gesamt(v3, a), gesamt(nachher, b)
    out += ["", "| Gesamt | v3 | nachher |", "|---|---|---|",
            f"| Erfolg je Lauf | {va} | {vb} |", f"| pass^3 | {pa} | {pb} |",
            f"| Kosten Agent | {sum(z['kosten_usd'] for z in v3):.4f} USD | {agent_kosten:.4f} USD |",
            f"| Kosten Judge (j2) | – (Cache aus UC4) | {judge_kosten:.4f} USD |"]
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    main()
