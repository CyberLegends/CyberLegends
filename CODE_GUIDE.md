# Cyber Legends — Runnable Red Teaming & AI Labs

Ten small, inspectable Python prototypes implementing a bounded core of the [project catalogue](PROJECTS.md). These are working offline reference implementations, not complete industrial products. Each file contains editable synthetic demo data, a callable `run(data)` function and a JSON command-line interface.

## Quick start

Use Python 3.10 or newer. No pip dependencies are required for offline demos.

```bash
git clone https://github.com/CyberLegends/CyberLegends.git
cd CyberLegends
python redops_copilot.py
python -m unittest -v test_projects.py
```

On systems where Python is named `python3`, replace `python` accordingly. On Windows, `py -3` is another option.

## Code for each project

| ID | Source | Implemented behavior | Run command |
| --- | --- | --- | --- |
| CL-RT-01 | [RedOps Copilot](redops_copilot.py) | Scope-bound approvals, expiry/revocation and job decisions; no execution engine. | `python redops_copilot.py` |
| CL-RT-02 | [LLM Assurance Lab](llm_assurance_lab.py) | Canary-leak checks, separate benign/security metrics, optional live local-model evaluation. | `python llm_assurance_lab.py` |
| CL-RT-03 | [Agent Boundary Guard](agent_boundary_guard.py) | Mock read/write gateway, tenant checks, argument rules, one-use approvals and request replay checks. | `python agent_boundary_guard.py` |
| CL-RT-04 | [Cloud Attack-Path Studio](cloud_attack_path.py) | Evidence-linked graph traversal and before/after edge-removal analysis. | `python cloud_attack_path.py` |
| CL-RT-05 | [Identity Resilience Range](identity_resilience.py) | Synthetic role-transition expectations compared with observed decisions and audit events. | `python identity_resilience.py` |
| CL-RT-06 | [Purple Team Evidence Hub](purple_evidence_hub.py) | Run/alert correlation, deduplication, latency, escalation and coverage with excluded incomplete runs. | `python purple_evidence_hub.py` |
| CL-RT-07 | [RAG Trust Boundary Lab](rag_trust_lab.py) | Tenant/role filtering before lexical retrieval, deletion/revocation checks and canary isolation. | `python rag_trust_lab.py` |
| CL-RT-08 | [AI Supply Chain Assurance](ai_supply_chain.py) | SHA-256 integrity, approved-source and provenance-label checks; confined local file reads. | `python ai_supply_chain.py` |
| CL-RT-09 | [Industrial Cyber Range](industrial_cyber_range.py) | Directed zone reachability and a latching stop/reset process simulation. | `python industrial_cyber_range.py` |
| CL-RT-10 | [GeoTrust Adversarial Lab](geotrust_lab.py) | Circular geofences, accuracy margins, hysteresis, replay/staleness and implausible-speed checks. | `python geotrust_lab.py` |

[Shared CLI and optional AI adapter](common.py) · [Regression test source](test_projects.py)

## Input and output

Every module works without arguments using its built-in `DEMO` dictionary. Export that dictionary to learn the exact input schema, edit it, then supply the JSON file:

```bash
python geotrust_lab.py --dump-demo > geotrust-input.json
python geotrust_lab.py --input geotrust-input.json --output geotrust-report.json
```

The output envelope identifies the code as a prototype and includes project-specific results and limitations. Demos deliberately include both passing and failing security cases. For example, the LLM demo reports a 0.5 security failure rate because one of its two synthetic security responses contains a canary; this is an expected fixture result, not a measurement of any real model.

Timestamps are numeric seconds in a single caller-defined time base. The demos use small synthetic values for readability. Use one consistent time base when creating fixtures. `run(data)` functions do not mutate the supplied input.

```python
from redops_copilot import run, DEMO
report = run(DEMO)
assert report['decisions'][0]['allowed']
assert not report['decisions'][1]['allowed']
```

## Optional local AI

Offline mode does not contact an AI provider or download a model. To opt in, run an already-installed Ollama service at `http://127.0.0.1:11434` with an already-installed model, then replace `YOUR_INSTALLED_MODEL` below:

```bash
python llm_assurance_lab.py --ai-model YOUR_INSTALLED_MODEL
python cloud_attack_path.py --ai-model YOUR_INSTALLED_MODEL
```

- **LLM Assurance Lab:** sends the case prompts to the local model and evaluates its returned responses, then requests an explanatory annotation.
- **Other projects:** keeps all decisions deterministic and sends the resulting report to the local model only for an explanatory annotation. It does not turn those modules into autonomous red-team agents.
- AI text is returned under `ai_annotation_untrusted`; it never grants permissions, executes commands or changes verdicts.
- The adapter uses only loopback, rejects redirects, bypasses environment proxies, limits response size and caps generated tokens. Live evaluation is limited to 50 cases.
- Synthetic data is the default. If you supply confidential data, review the contents and your local model configuration before opting into AI annotation.
- Local inference is optional and was **not integration-tested against a running Ollama server** in the authoring environment. The response plumbing is covered with a mocked model in the test suite.

## Validation record

The initial code release passed **30 offline regression tests**, plus a successful CLI/JSON smoke run for all ten demos and demo-export commands. Re-run the suite after modifying code or fixtures; this record is not a claim that later changes have been tested.

The regression tests cover approval scope and expiry, cross-tenant restrictions, replay, input ambiguity, model-response scoring, graph denies/cycles, evidence requirements, identity findings, incomplete telemetry, ACL revocation, hash tampering, file-path confinement, OT isolation declarations, stop latching and geofence uncertainty.

## Boundaries and next engineering work

| Prototype area | What remains before an operational pilot |
| --- | --- |
| Authorization | Authenticated principals, signed approvals, atomic durable state, distributed replay handling and independent scope verification. |
| Cloud and identity | Provider/directory adapters, effective-permission semantics, collection completeness and environment-specific validation. |
| RAG and AI | Real retriever adapters, evaluation datasets, repeated stochastic runs, calibrated human review and broader leakage detection. |
| Supply chain | Signed provenance verification and trusted manifest distribution. A matching hash or supplied provenance label alone is not trust. |
| Industrial | Actual lab infrastructure and protocol simulators. The Python model neither controls nor tests real PLCs or safety systems. |
| Geofencing | Authenticated telemetry, persistent replay state, production geospatial rules, privacy controls and load testing. |
| Operations | Full schema validation, authentication, dashboards, durable audit storage, deployment automation, monitoring and support ownership. |

These scripts do not scan targets, deploy payloads, harvest credentials or alter external systems. They are designed for synthetic fixtures and authorized lab evaluation. A local service on the loopback port is assumed to be under the operator's control. Any production use needs a separate security review and deployment design.
