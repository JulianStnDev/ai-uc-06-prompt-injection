"""UC4-Goldset nach dem Umbau (UC6, Branch b): 15 Tickets × 3 Läufe gegen den UC7-Code, Prompt v3.

Läuft mit dem Python von UC7 (dort liegt das Agent SDK) und dem Key aus der .env dieses Repos:

    ../ai-uc-07-deployment/.venv/bin/python scripts/goldset_lauf.py --trocken   # nur Plan, keine API
    ../ai-uc-07-deployment/.venv/bin/python scripts/goldset_lauf.py             # echter Lauf

Harte Budgetgrenze: Ein Lauf startet nur, wenn die bisherigen Kosten plus 0,50 USD (Deckel je Lauf,
agent.MAX_BUDGET_USD) für jeden laufenden und den neuen Lauf unter --budget bleiben. So kann die Summe die Grenze
nicht überschreiten. Läufe ohne Kostenangabe zählen mit dem Deckel. Fertige Läufe werden übersprungen.
Ergebnis: evals/goldset_nachher/<ticket>_lauf<n>/ (lauf.json, trajektorie.jsonl, …) und lauf_uebersicht.json.
"""

import argparse
import asyncio
import json
import os
import subprocess
import sys
from pathlib import Path

HIER = Path(__file__).resolve().parent.parent


def env_laden(pfad: Path) -> None:
    for zeile in pfad.read_text(encoding="utf-8").splitlines():
        if "=" in zeile and not zeile.lstrip().startswith("#"):
            k, v = zeile.split("=", 1)
            os.environ[k.strip()] = v.strip().strip('"').strip("'")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--uc7", default=str(HIER.parent / "ai-uc-07-deployment"))
    p.add_argument("--laeufe", type=int, default=3)
    p.add_argument("--parallel", type=int, default=3)
    p.add_argument("--budget", type=float, default=8.0)
    p.add_argument("--ausgabe", default=str(HIER / "evals" / "goldset_nachher"))
    p.add_argument("--trocken", action="store_true", help="nur Plan ausgeben, keine API")
    a = p.parse_args()

    uc7 = Path(a.uc7).resolve()
    commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=uc7, capture_output=True, text=True).stdout.strip()
    sauber = not subprocess.run(["git", "status", "--porcelain", "--untracked-files=no"], cwd=uc7,
                                capture_output=True, text=True).stdout.strip()
    sys.path.insert(0, str(uc7))
    from uc4_agent import agent  # noqa: E402

    ausgabe = Path(a.ausgabe)
    aufgaben = agent.lade_aufgaben()
    jobs = [(t, f"{t['id']}_lauf{n}") for t in aufgaben for n in range(1, a.laeufe + 1)]
    offen = [(t, r) for t, r in jobs if not (ausgabe / r / "lauf.json").exists()]
    print(f"UC7-Commit {commit} ({'sauber' if sauber else 'NICHT sauber'}), Prompt v3, {len(jobs)} Läufe, offen {len(offen)}, "
          f"Budget {a.budget:.2f} USD, Deckel je Lauf {agent.MAX_BUDGET_USD:.2f} USD")
    if not sauber:
        sys.exit("Abbruch: UC7 hat uncommittete Änderungen. Gemessen wird nur ein fester Commit.")
    if a.trocken:
        return

    env_laden(HIER / ".env")
    if not os.environ.get("ANTHROPIC_API_KEY", "").strip():
        sys.exit("Abbruch: ANTHROPIC_API_KEY fehlt in der .env von UC6.")
    agent.api_key_pruefen = lambda: os.environ["ANTHROPIC_API_KEY"].strip()  # Key aus UC6, nicht aus uc4_agent/.env

    bisher = sum((json.loads((ausgabe / r / "lauf.json").read_text()).get("kosten_usd") or agent.MAX_BUDGET_USD)
                 for _, r in jobs if (ausgabe / r / "lauf.json").exists())
    stand = {"kosten": bisher, "laufend": 0, "uebersprungen": []}
    sem = asyncio.Semaphore(a.parallel)

    async def einer(t, r):
        async with sem:
            if stand["kosten"] + (stand["laufend"] + 1) * agent.MAX_BUDGET_USD > a.budget:
                stand["uebersprungen"].append(r)
                print(f"{r}: übersprungen (Budget)", flush=True)
                return
            stand["laufend"] += 1
            try:
                lauf = await agent.bearbeite_ticket(t, r, ausgabe, "v3")
                stand["kosten"] += lauf["kosten_usd"] if lauf["kosten_usd"] is not None else agent.MAX_BUDGET_USD
                print(f"{r}: {lauf['subtype']}, {lauf['num_turns']} Turns, {lauf['dauer_s']:.1f} s, "
                      f"{(lauf['kosten_usd'] or 0):.4f} USD, Summe {stand['kosten']:.4f} USD", flush=True)
            finally:
                stand["laufend"] -= 1

    async def alle():
        await asyncio.gather(*(einer(t, r) for t, r in offen))

    asyncio.run(alle())
    (ausgabe / "lauf_uebersicht.json").write_text(json.dumps(
        {"uc7_commit": commit, "prompt": "v3", "laeufe": len(jobs), "kosten_usd": round(stand["kosten"], 4),
         "budget_usd": a.budget, "uebersprungen": stand["uebersprungen"]}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Fertig. Kosten {stand['kosten']:.4f} USD, übersprungen {len(stand['uebersprungen'])}")


if __name__ == "__main__":
    main()
