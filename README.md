🇩🇪 [Deutsche Version](README_DE.md)

# UC6 — Prompt Injection & Guardrails: Attacking the Support Agent

> Status: guardrails built into the UC7 code and proven (UC7 PR #11, not deployed yet). Threat model and residual risk: [docs/BEDROHUNGSMODELL.md](docs/BEDROHUNGSMODELL.md), in German. The target is the live support agent from [UC7](https://github.com/JulianStnDev/ai-uc-07-deployment).

## Problem
The support agent from UC7 reads customer data, cancels subscriptions and recommends refunds. A logged-in customer writes free text to it, and the agent reads data that is partly set by customers or third parties. Free text is an attack surface: a language model cannot reliably tell instructions from data. UC6 asks: what can an attacker achieve with text, which guardrail actually holds, and where is there only one?

## PM Decision
UC7 is attacked, not rebuilt. That way every defense counts in the real product. Sequence:

1. **Branch (a):** threat model from the UC7 code (commit `2c8cc86`), without API calls.
2. **Scope (Oct 2):** the real product. The attacker is a logged-in customer or whoever can place text in data the agent reads. Demo topics are listed separately.
3. **Branch (b) in UC7:** the gaps from the matrix are closed in code and proven by tests without API calls: every call a successful attack would produce got through before and is blocked now. Usefulness is checked with the UC4 gold set. UC6 writes no attack texts (reasoning in the decisions).

Decisions: [docs/decisions.md](docs/decisions.md).

## Architecture Sketch
Two repos with clear jobs:

- **This repo:** threat model, decisions, results.
- **UC7:** code of the agent, the defenses and their tests.

Everything runs locally against a pinned UC7 commit, not against the live URL (otherwise it would use up the demo's monthly budget and skew its statistics). Diagram of entry points and guardrails: [docs/BEDROHUNGSMODELL.md, section 5](docs/BEDROHUNGSMODELL.md#5-diagramm-einfallstore-und-schutzschichten).

## Evaluation Results
As of Oct 2, 2026, UC7 PR #11 (not deployed yet). Details: [evals/results.md](evals/results.md), section 10 of the [threat model](docs/BEDROHUNGSMODELL.md#10-nach-branch-b-restrisiko-nachher) (German).

| Measurement | Before | After |
|---|---|---|
| Attack calls that get through (23 cases, no API) | 16 of 23 | **0 of 23** |
| Legitimate calls that go through (14 cases, no API) | 14 of 14 | 14 of 14 |
| Promise check: promises caught / false alarms | – | 7 of 7 / **0 of 1,241** sentences (95% upper bound ≈ 0.24%) |
| UC4 gold set, success per run (judge j2) | 39 of 45 | 34 of 45 |
| UC4 gold set, pass^3 | 11 of 15 | 10 of 15 |

34 of 45 was measured **before the T14 fix** (UC7 `945d475`). The fix (the sender's own email used as customer ID gets a hint instead of a block; everything else without a customer ID stays blocked) is covered by deterministic tests, cases K8a–K8h; the gold set has not been re-run since.

**The guardrails cost 1 run (false alarm, fixed), 1 run is a real catch, the rest is not caused by the guardrails.** The false alarm (own email used as customer ID, T14) is fixed. The real catch: in T15 the agent tried to read Anna's payments. T04 also fails with the old code in a counter-test; T13 is sampling variance with identical input.

Residual risk after the rebuild:

| Threat | Before | After |
|---|---|---|
| Acting for another account, reading other customers' data | high | **low** (account binding in the hook) |
| Promising a refund without recommending it | high | **medium** (the promise check is a heuristic) |
| Unjustified refund for one's own account | medium | **low** (rules in the tool) |
| Hidden instructions in data the agent reads | medium–high | **medium** (calls are bound, draft text can still be steered) |

## Cost & Latency
- Cost per 1000 requests: about 28 USD (agent, Haiku 4.5, mean of 45 gold set runs after the rebuild). Total UC6 cost so far: 2.45 USD.
- p95 latency: 45.0 s per ticket (median 23.5 s), 45 gold set runs, local
- Quality metric: 0 of 23 attack calls get through; gold set 34 of 45, every lost run attributed individually

## Learnings
- My picture of UC7 was "the hooks check the sender's account". The code says: the hooks check the tool name and the duties; only the prompt checks the account. A threat model pays off before the first attack, if you write it from the code rather than from memory.
- Separate demo and product: in the first version, demo quirks (visitors approving their own refunds, bots) shaped the priorities. For the product, other gaps come first.
- Prove guardrails instead of measuring attacks: an attack success rate mostly measures the prompt. A test that blocks a tool call directly holds no matter how the model was talked into it.

## What I Would Do Differently
Still open.
