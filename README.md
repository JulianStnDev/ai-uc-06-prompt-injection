🇩🇪 [Deutsche Version](README_DE.md)

# UC6 — Prompt Injection & Guardrails: Attacking the Support Agent

> Status: threat model for the real product ([docs/BEDROHUNGSMODELL.md](docs/BEDROHUNGSMODELL.md), in German). Next: guardrails in the UC7 code, proven by deterministic tests. No API cost yet. The target is the live support agent from [UC7](https://github.com/JulianStnDev/ai-uc-07-deployment).

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
No measurements yet. Findings from the threat model, read from the code only:

- **Money is protected structurally:** no tool pays out or sends anything; the agent can only recommend.
- **No hook checks the sender's account.** Whether the agent acts for the right account is governed by the prompt alone. A rule check flags violations only after the run.
- **The refund rules live only in the help article.** The tool checks neither the deadline nor double charges.
- **Only one layer, the prompt,** stands in front of three threats with high residual risk: reading other customers' data, acting for another customer's account, and promising a refund in the draft without recommending it.

## Cost & Latency
- Cost per 1000 requests: not measured yet (UC4 gold set after the rebuild). 0 USD API cost so far.
- p95 latency: not measured yet (UC4 gold set after the rebuild)
- Quality metric: planned are the number of gaps proven closed by a test in code, and the UC4 gold set without new blocks

## Learnings
- My picture of UC7 was "the hooks check the sender's account". The code says: the hooks check the tool name and the duties; only the prompt checks the account. A threat model pays off before the first attack, if you write it from the code rather than from memory.
- Separate demo and product: in the first version, demo quirks (visitors approving their own refunds, bots) shaped the priorities. For the product, other gaps come first.
- Prove guardrails instead of measuring attacks: an attack success rate mostly measures the prompt. A test that blocks a tool call directly holds no matter how the model was talked into it.

## What I Would Do Differently
Still open.
