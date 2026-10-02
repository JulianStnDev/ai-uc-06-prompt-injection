🇩🇪 [Deutsche Version](README_DE.md)

# UC6 — Prompt Injection & Guardrails: Attacking the Support Agent

> Status: Branch (a), threat model ([docs/BEDROHUNGSMODELL.md](docs/BEDROHUNGSMODELL.md), in German). No measurements yet, no API cost. The target is the live support agent from [UC7](https://github.com/JulianStnDev/ai-uc-07-deployment).

## Problem
The support agent from UC7 is online. Every visitor with a personal link picks a fictional customer and writes free text to an agent that reads customer data, cancels subscriptions and recommends refunds. Free text is an attack surface: a language model cannot reliably tell instructions from data. UC6 asks: what can an attacker achieve with text, which guardrail actually holds, and where is there only one?

## PM Decision
UC7 is attacked, not rebuilt. That way every defense counts in the real product. Sequence:

1. **Branch (a):** threat model from the UC7 code (commit `2c8cc86`), without API calls.
2. **Branch (b):** test cases (attacks plus the same number of harmless controls), baseline measurement.
3. **Then:** defenses as separate PRs in the UC7 repo, each re-measured here. A defense only counts if the attack success rate drops and the control cases are still solved.

Decisions: [docs/decisions.md](docs/decisions.md).

## Architecture Sketch
Two repos with clear jobs:

- **This repo:** threat model, test cases, measurement scripts, results.
- **UC7:** code of the agent and of the defenses.

Tests run locally against a pinned UC7 commit, not against the live URL (otherwise they would use up the demo's monthly budget and skew its statistics). Diagram of entry points and guardrails: [docs/BEDROHUNGSMODELL.md, section 5](docs/BEDROHUNGSMODELL.md#5-diagramm-einfallstore-und-schutzschichten).

## Evaluation Results
No measurements yet. Findings from the threat model, read from the code only:

- **Money is protected structurally:** no tool pays out or sends anything; the agent can only recommend.
- **No hook checks the sender's account.** Whether the agent acts for the right account is governed by the prompt alone. A rule check flags violations only after the run.
- **Only one layer, the prompt,** stands in front of three threats: reading other customers' data, cancelling another customer's subscription, and promising a refund in the draft without recommending it.
- **Denial of wallet is capped:** without a link no run starts, one link costs at most 2.50 USD, the month at most 5 USD.

## Cost & Latency
- Cost per 1000 requests: not measured yet (branch b). Branch (a): 0 USD API cost.
- p95 latency: not measured yet (branch b)
- Quality metric: planned are attack success rate per category and control pass rate

## Learnings
- My picture of UC7 was "the hooks check the sender's account". The code says: the hooks check the tool name and the duties; only the prompt checks the account. A threat model pays off before the first attack, if you write it from the code rather than from memory.
- In the demo, visitors decide on their own recommendations. The human in the loop is the attacker there, and the shadow-mode confirmation rate gets skewed.

## What I Would Do Differently
Still open.
