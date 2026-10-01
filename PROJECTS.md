# Cyber Legends — Red Teaming & AI Project Portfolio

**10 industry-focused project blueprints with runnable lab prototypes**  
Cybersecurity · Adversary simulation · AI assurance · Industrial security

> **Portfolio status:** Ten runnable Python lab prototypes are published, each implementing a bounded core of its project blueprint. The broader architectures, deliverables and roadmaps below describe proposed industrial solutions. These entries do not claim completed client work, production deployments or measured industrial performance. Suggested stacks must be validated during discovery.

**Start here:** [Code & setup guide](CODE_GUIDE.md) · [30 offline regression tests](test_projects.py). All ten synthetic CLI demos and fixture exports passed during the initial code release. Optional local-model integration remains untested against a running service.

[Back to Cyber Legends](https://github.com/CyberLegends) · [Service overview](README.md) · [Cyberlegends.org](https://cyberlegends.org)

## Project directory

| ID | Project | Industry / environment | Main outcome | Code |
| :--- | :--- | :--- | :--- | :--- |
| CL-RT-01 | [RedOps Copilot](#cl-rt-01--redops-copilot) | Enterprise / security consultancies | Human-approved adversary-simulation planning | [redops_copilot.py](redops_copilot.py) |
| CL-RT-02 | [LLM Adversarial Assurance Lab](#cl-rt-02--llm-adversarial-assurance-lab) | Banking / customer-facing AI | Repeatable AI application security evaluations | [llm_assurance_lab.py](llm_assurance_lab.py) |
| CL-RT-03 | [Agent Boundary Guard](#cl-rt-03--agent-boundary-guard) | SaaS / enterprise automation | Validation of agent permissions and approval boundaries | [agent_boundary_guard.py](agent_boundary_guard.py) |
| CL-RT-04 | [Cloud Attack-Path Studio](#cl-rt-04--cloud-attack-path-studio) | Retail / cloud-native organizations | Evidence-backed identity and exposure paths | [cloud_attack_path.py](cloud_attack_path.py) |
| CL-RT-05 | [Identity Resilience Range](#cl-rt-05--identity-resilience-range) | Enterprise / hybrid identity | Safe identity attack-path and detection validation | [identity_resilience.py](identity_resilience.py) |
| CL-RT-06 | [Purple Team Evidence Hub](#cl-rt-06--purple-team-evidence-hub) | SOC / MSSP | Measurable control coverage and detection improvements | [purple_evidence_hub.py](purple_evidence_hub.py) |
| CL-RT-07 | [RAG Trust Boundary Lab](#cl-rt-07--rag-trust-boundary-lab) | Healthcare / legal / knowledge platforms | Retrieval isolation and information-integrity testing | [rag_trust_lab.py](rag_trust_lab.py) |
| CL-RT-08 | [AI Supply Chain Assurance](#cl-rt-08--ai-supply-chain-assurance) | Software vendors / AI product teams | Model, dependency and build-provenance validation | [ai_supply_chain.py](ai_supply_chain.py) |
| CL-RT-09 | [Industrial Cyber Range](#cl-rt-09--industrial-cyber-range) | Manufacturing / OT | Simulated IT/OT segmentation and response exercises | [industrial_cyber_range.py](industrial_cyber_range.py) |
| CL-RT-10 | [GeoTrust Adversarial Lab](#cl-rt-10--geotrust-adversarial-lab) | Logistics / connected assets | Geofence, telemetry and location-policy resilience | [geotrust_lab.py](geotrust_lab.py) |

## Common delivery model

Each project progresses through **discovery → isolated prototype → validation → pilot → handover**. Pilot deployment requires an agreed scope, named system owner, test window, rollback procedure and written authorization. Timelines and commercial estimates follow discovery; none are implied here.

Shared engineering requirements:

- Separate tenants and environments; synthetic or approved sanitized datasets by default.
- Role-based access, least-privilege service identities, secrets management and explicit retention settings.
- Versioned scenarios, reproducible seeds where supported, run IDs, audit logs and evidence integrity checks.
- Human approval for consequential actions; enforce asset allowlists and limits outside the language model.
- Treat model output as a draft. Link conclusions to evidence and record uncertain or unsupported findings.
- Report coverage, failure cases and test limitations alongside outcomes; a passing test suite is not proof of complete security.

---

## CL-RT-01 — RedOps Copilot

**Industry:** Enterprise security teams and authorized security consultancies.  
**Project type:** AI-assisted red-team planning and exercise management.  
**Status:** Runnable lab prototype published; the broader architecture below remains a design roadmap.

**Code:** [redops_copilot.py](redops_copilot.py) · [Setup & run guide](CODE_GUIDE.md)  
**Run:** `python redops_copilot.py`  
**Implemented now:** Scope-bound job decisions with approval expiry and revocation; planning only, without an execution engine.

### Business problem

Exercise planning often relies on disconnected documents, inconsistent scope checks and reports that lose the link between an observation and its supporting evidence. This project creates a controlled planning workspace that keeps authorization and review visible throughout an engagement.

### Proposed solution & architecture

An analyst imports an approved asset inventory and rules of engagement. An AI assistant proposes exercise objectives and selects from a reviewed scenario catalogue. A deterministic policy service checks every proposal against asset scope, prohibited actions and test windows. A named reviewer approves the plan before an isolated runner executes permitted simulations.

**Components:** engagement workspace; scope registry; scenario catalogue; retrieval-backed planning assistant; policy engine; approval queue; isolated runner; evidence store; report builder.

**Suggested stack:** Python, FastAPI, PostgreSQL, a provider-neutral LLM adapter, a policy engine, containerized lab workers and an object store. Planning and execution use separate service identities.

### Deliverables

- Engagement intake and rules-of-engagement templates.
- Versioned scenario plans with owner, prerequisites, expected telemetry and stop conditions.
- Approval workflow, scope-validation service and tamper-evident execution records.
- Technical findings report and executive summary with evidence references.

### Validation & success criteria

Submit in-scope, out-of-scope, expired-approval and revoked-approval fixtures. Every prohibited job must be rejected by the policy service. Every accepted run must link to a current authorization, scenario version and reviewer decision. AI summaries must cite stored observations; unsupported assertions require review. Measure planning time separately from finding quality against a manual baseline.

**Roadmap:** Build the scope registry and manual workflow; add evidence-grounded AI planning; integrate lab-only simulations; pilot with one bounded engagement. Autonomous target selection, live exploitation and unrestricted tool execution are outside the initial release.

---

## CL-RT-02 — LLM Adversarial Assurance Lab

**Industry:** Banking, insurance and customer-facing AI services.  
**Project type:** Security evaluation of LLM applications.  
**Status:** Runnable lab prototype published; the broader architecture below remains a design roadmap.

**Code:** [llm_assurance_lab.py](llm_assurance_lab.py) · [Setup & run guide](CODE_GUIDE.md)  
**Run:** `python llm_assurance_lab.py`  
**Implemented now:** Synthetic canary-leak evaluation with separate security and benign-case metrics; optional live evaluation against an installed local model.

### Business problem

An AI assistant may expose sensitive context, ignore policy boundaries or produce unsafe tool requests when it encounters adversarial input. Model-level tests alone do not establish the security of the surrounding application.

### Proposed solution & architecture

A scenario registry holds approved, synthetic adversarial fixtures and normal user tasks. An evaluation scheduler sends them to a staging assistant through a scoped adapter. Deterministic checks, canary detection and human review score the resulting answers and tool requests. AI proposes variations for review and clusters recurring failure patterns; it is not the sole judge.

**Components:** scenario library; application adapter; evaluation worker; synthetic-secret vault; scoring service; reviewer console; regression dashboard.

**Suggested stack:** Python, pytest, FastAPI, PostgreSQL and an approved model gateway. Store model configuration, application build and scenario version with every run.

### Deliverables

- Threat model covering input, retrieval, output and tool boundaries.
- Synthetic evaluation dataset and a documented benign-task baseline.
- Security regression pipeline and reviewer-calibrated scoring rubric.
- Findings with reproducible test conditions, impact, remediation and retest evidence.

### Validation & success criteria

Include direct and indirect instruction-conflict cases, fabricated sensitive-data requests and tool-boundary violations. No seeded secret may appear in output for the agreed protected cases. Report security failure rate, benign-task completion and reviewer disagreement separately. Repeat stochastic cases across recorded runs; publish sample counts and variability rather than a single unqualified score.

**Roadmap:** Define the threat model; implement baseline adapters and deterministic checks; add reviewed AI-generated test variations; integrate a release gate with agreed thresholds. Testing uses staging accounts and synthetic banking records, never real customer credentials.

---

## CL-RT-03 — Agent Boundary Guard

**Industry:** SaaS platforms and enterprise workflow automation.  
**Project type:** Red teaming of tool-using AI agents.  
**Status:** Runnable lab prototype published; the broader architecture below remains a design roadmap.

**Code:** [agent_boundary_guard.py](agent_boundary_guard.py) · [Setup & run guide](CODE_GUIDE.md)  
**Run:** `python agent_boundary_guard.py`  
**Implemented now:** Mock read/write gateway with tenant isolation, argument checks, one-use approval expiry and request replay checks.

### Business problem

An agent that can read documents, send messages or modify records may cross authorization boundaries through confused instructions, excessive permissions or unreliable approval handling.

### Proposed solution & architecture

Instrument a staging agent through a tool gateway. The gateway validates requested actions, resource ownership, argument schemas and current approval state before invoking mocked tools. An adversarial evaluator supplies untrusted content and controlled workflow variations. A trace viewer correlates the agent decision, policy verdict and resulting state change.

**Components:** agent adapter; identity context; tool gateway; policy decision service; mock email, CRM and file tools; approval simulator; trace collector.

**Suggested stack:** Python or TypeScript, JSON Schema validation, FastAPI, PostgreSQL, OpenTelemetry-compatible tracing and an isolated mock-tool service.

### Deliverables

- Agent/tool permission matrix and trust-boundary diagram.
- Tests for cross-tenant access, forged approvals, replayed actions and untrusted retrieved instructions.
- Gateway policies, approval-state fixtures and incident investigation views.
- Remediation guide covering least privilege, argument validation and safe failure behavior.

### Validation & success criteria

A malicious document must not grant tool permissions. Cross-tenant requests and replayed approvals must be denied. Consequential tool calls must remain blocked until an independently verified approval is present. Repeated requests must not create duplicate actions where idempotency is required. Capture both blocked attacks and legitimate workflows incorrectly refused.

**Roadmap:** Inventory tools and permissions; build mock tools and deterministic enforcement; add adversarial workflow tests; connect a staging agent and pilot an approval dashboard. Test actions remain inside mocks until a separately approved integration phase.

---

## CL-RT-04 — Cloud Attack-Path Studio

**Industry:** Retail, e-commerce and cloud-native organizations.  
**Project type:** AI-assisted cloud exposure and identity-path analysis.  
**Status:** Runnable lab prototype published; the broader architecture below remains a design roadmap.

**Code:** [cloud_attack_path.py](cloud_attack_path.py) · [Setup & run guide](CODE_GUIDE.md)  
**Run:** `python cloud_attack_path.py`  
**Implemented now:** Evidence-linked traversal of a supplied cloud graph and before/after remediation analysis by removing edges.

### Business problem

Individual configuration findings do not always show how internet exposure, excessive permissions and valuable data combine into a business-relevant risk path.

### Proposed solution & architecture

Read-only collectors ingest approved cloud inventory, identity policies and configuration exports. A normalization layer builds an asset-and-permission graph. Deterministic rules identify candidate paths. AI translates evidence into analyst-readable narratives and proposes remediation questions; analysts validate assumptions before any finding is issued.

**Components:** scoped collectors; normalized asset model; permission graph; path-analysis rules; evidence references; remediation simulator; analyst review console.

**Suggested stack:** Python, FastAPI, PostgreSQL or a graph database, infrastructure-as-code fixtures and a model gateway restricted to sanitized metadata. Start with one cloud provider.

### Deliverables

- Asset inventory and exposure map with collection timestamps.
- Reviewed identity/exposure paths with prerequisites and uncertainty flags.
- Remediation comparison showing which graph edges each change removes.
- Executive risk summary and infrastructure-owner action list.

### Validation & success criteria

Use synthetic environments with known risky and safe configurations. Confirm that each displayed edge has a source-policy or configuration reference. Compare candidate paths with expected fixtures, including explicit deny rules and missing data. Mark stale assets and incomplete collection. Validate recommended changes in a sandbox and report operational dependencies.

**Roadmap:** Build read-only inventory ingestion; implement a bounded set of path rules; add evidence-grounded explanations; pilot on a sanitized environment export. No credential harvesting, exploitation or automatic production remediation is included.

---

## CL-RT-05 — Identity Resilience Range

**Industry:** Enterprises with hybrid identity and privileged administration.  
**Project type:** Identity-focused adversary simulation and purple-team validation.  
**Status:** Runnable lab prototype published; the broader architecture below remains a design roadmap.

**Code:** [identity_resilience.py](identity_resilience.py) · [Setup & run guide](CODE_GUIDE.md)  
**Run:** `python identity_resilience.py`  
**Implemented now:** Comparison of synthetic role-transition expectations with observed access decisions and audit events.

### Business problem

Identity risks can arise from excessive trust, stale privileges and weak separation between normal users, service identities and administrative roles. Teams need to validate these relationships without placing production identities at risk.

### Proposed solution & architecture

Create an isolated identity lab with synthetic users, groups, service accounts and applications. Import only approved, sanitized relationship models. A scenario controller performs reviewed benign simulations while the telemetry pipeline records expected control decisions. AI assists with prioritization, scenario explanations and report drafting.

**Components:** synthetic directory; role-and-trust graph; scenario controller; policy checks; authentication event collector; detection dashboard; cleanup verifier.

**Suggested stack:** isolated virtual machines, infrastructure-as-code, Python orchestration, PostgreSQL and a lab log platform. Any directory software requires appropriate licensing and lab configuration.

### Deliverables

- Synthetic identity topology and baseline privilege inventory.
- Scenarios for role separation, service-account scope and administrative approval boundaries.
- Expected-event catalogue, detection worksheets and remediation priorities.
- Reset procedures and a signed-off lab teardown checklist.

### Validation & success criteria

Known unauthorized role transitions must be rejected or explicitly identified as lab findings. Expected audit events must be correlated with scenario IDs and time windows. Restoring a snapshot must remove test-state changes. Review false alarms using normal administrative fixtures. Evidence must distinguish a theoretical trust path from a successfully validated control failure.

**Roadmap:** Build the synthetic identity environment; model trust relationships; implement approved simulations and telemetry checks; run analyst-led exercises. Live credential extraction, production persistence and password attacks are outside the project scope.

---

## CL-RT-06 — Purple Team Evidence Hub

**Industry:** Security operations centers and managed security service providers.  
**Project type:** AI-assisted detection validation and exercise reporting.  
**Status:** Runnable lab prototype published; the broader architecture below remains a design roadmap.

**Code:** [purple_evidence_hub.py](purple_evidence_hub.py) · [Setup & run guide](CODE_GUIDE.md)  
**Run:** `python purple_evidence_hub.py`  
**Implemented now:** Run/alert correlation, deduplication, detection latency, escalation checks and coverage that excludes incomplete telemetry.

### Business problem

An exercise may generate many alerts without proving that the right behavior was detected, escalated and investigated. Evidence is often scattered across logs, tickets and analyst notes.

### Proposed solution & architecture

A run registry schedules reviewed simulations or replays approved synthetic telemetry. Connectors collect matching events, alerts and tickets. A correlation service compares actual evidence with the expected result for each scenario. AI groups related observations and drafts explanations with citations; the detection engineer owns the final judgment.

**Components:** scenario/run registry; telemetry replay service; SIEM adapter; correlation engine; evidence ledger; analyst review; scorecard exporter.

**Suggested stack:** Python, FastAPI, PostgreSQL, object storage and configurable log-platform adapters. Model integrations receive redacted event fields only.

### Deliverables

- Versioned exercise catalogue and expected-detection matrix.
- Evidence-linked coverage dashboard and detection-gap backlog.
- Tuning recommendations with before/after test results.
- Executive scorecard and investigation handover package.

### Validation & success criteria

Use fixtures for detected, missed, delayed and duplicate events. Calculate detection coverage only over scenarios actually executed with adequate telemetry. Measure alert latency from known event timestamps and document clock skew. Separate successful logging, alert creation and analyst escalation. AI-generated claims without matching evidence must be flagged rather than counted as detections.

**Roadmap:** Establish run IDs and evidence schemas; integrate one telemetry source; implement rule-based correlation; add AI summaries and controlled retesting. No claimed coverage percentage is published before measured runs exist.

---

## CL-RT-07 — RAG Trust Boundary Lab

**Industry:** Healthcare, legal services and enterprise knowledge platforms.  
**Project type:** Adversarial testing of retrieval-augmented generation applications.  
**Status:** Runnable lab prototype published; the broader architecture below remains a design roadmap.

**Code:** [rag_trust_lab.py](rag_trust_lab.py) · [Setup & run guide](CODE_GUIDE.md)  
**Run:** `python rag_trust_lab.py`  
**Implemented now:** Tenant and role filtering before lexical retrieval, with deletion/revocation checks and synthetic canary isolation.

### Business problem

A knowledge assistant may retrieve material belonging to another tenant, accept instructions embedded in documents or cite sources that do not support its answer.

### Proposed solution & architecture

Construct a synthetic corpus with public, role-restricted and tenant-specific documents. An ingestion service preserves ownership and access labels. A test harness exercises retrieval and generation under different identities, including untrusted-document fixtures. An evidence evaluator checks both retrieved context and final answers, while reviewers resolve ambiguous results.

**Components:** synthetic document generator; ingestion pipeline; access-aware retriever; identity simulator; model adapter; citation checker; isolation-test dashboard.

**Suggested stack:** Python, FastAPI, PostgreSQL with a suitable vector-search component, document parsers and a provider-neutral model adapter. Use synthetic clinical or legal records.

### Deliverables

- Tenant and document-access matrix.
- Adversarial corpus with documented provenance and canary markers.
- Tests for retrieval leakage, unsupported citations and document-instruction conflicts.
- Remediation plan for ingestion controls, retrieval filters and output verification.

### Validation & success criteria

Restricted canaries must not appear in another tenant's retrieved context or generated response. Test direct questions, paraphrases and multi-turn requests. Verify that deletion and permission changes invalidate cached access. Check cited passages for actual support and record human-review agreement. Measure authorized-answer usefulness separately from isolation failures.

**Roadmap:** Build the synthetic corpus; instrument retrieval; add role/tenant tests; introduce reviewed adversarial document variations and a regression gate. Real patient, client or privileged legal data is excluded from the public dataset.

---

## CL-RT-08 — AI Supply Chain Assurance

**Industry:** AI product vendors and enterprise software teams.  
**Project type:** Adversarial validation of model and software delivery controls.  
**Status:** Runnable lab prototype published; the broader architecture below remains a design roadmap.

**Code:** [ai_supply_chain.py](ai_supply_chain.py) · [Setup & run guide](CODE_GUIDE.md)  
**Run:** `python ai_supply_chain.py`  
**Implemented now:** SHA-256 integrity, approved-source and provenance-label checks for supplied artifacts; local file access is confined to approved roots.

### Business problem

AI systems depend on model artifacts, datasets, plugins and software packages. Untracked provenance or weak build controls can allow unauthorized components into an otherwise well-designed application.

### Proposed solution & architecture

A pipeline inventories approved dependencies, model artifacts and dataset versions. Policy checks validate hashes, provenance records and approved sources before artifacts enter a quarantine environment. AI summarizes change impact from metadata; deterministic checks make admission decisions. Simulated tampering fixtures test whether the pipeline rejects unapproved changes.

**Components:** artifact inventory; provenance registry; software bill of materials; policy gate; isolated inspection environment; change-review queue; audit reports.

**Suggested stack:** Python, CI workflows, SBOM tooling, artifact hashing, a private package/artifact registry and PostgreSQL. Assess licensing and parser safety during discovery.

### Deliverables

- Model and dependency inventory with ownership and source records.
- Admission policies and reproducible build/check manifests.
- Non-executing tamper fixtures and provenance-validation tests.
- Exception process, change-impact reports and incident traceability guide.

### Validation & success criteria

Modified artifacts, absent provenance and unapproved sources must be rejected according to policy. Approved artifacts must remain reproducibly identifiable. Test exception expiry and rollback to a known approved version. Never deserialize an unknown artifact merely to inspect it. Report the limits of metadata checks: valid provenance alone does not establish that a model or dependency is safe.

**Roadmap:** Inventory artifacts; establish policy gates; test tamper fixtures in quarantine; integrate release review and periodic revalidation. No malicious dependency publication or poisoning of public datasets is involved.

---

## CL-RT-09 — Industrial Cyber Range

**Industry:** Manufacturing and industrial operational technology.  
**Project type:** Simulated IT/OT red-team and incident-response exercises.  
**Status:** Runnable lab prototype published; the broader architecture below remains a design roadmap.

**Code:** [industrial_cyber_range.py](industrial_cyber_range.py) · [Setup & run guide](CODE_GUIDE.md)  
**Run:** `python industrial_cyber_range.py`  
**Implemented now:** Abstract IT/OT zone reachability and a process-state simulation with latching stop/reset behavior; no connection to real industrial systems.

### Business problem

Manufacturing teams must assess segmentation and response readiness while protecting process safety and availability. Production controllers are unsuitable for exploratory adversarial testing.

### Proposed solution & architecture

Build an isolated digital process simulation with a simulated controller, HMI, historian and segmented IT/OT networks. A scenario controller introduces approved synthetic security events and configuration variations. Passive telemetry observes boundary behavior. AI helps explain event sequences and draft exercise debriefs; it cannot issue process-control commands.

**Components:** simulated process; virtual controller/HMI; network zones; historian; passive sensor; exercise controller; evidence timeline; instructor dashboard.

**Suggested stack:** isolated virtualization or containers, an industrial process simulator, Python, a message broker where appropriate, packet-capture analysis and a time-series store. Protocols are selected to match the training objective.

### Deliverables

- Lab topology, asset inventory and documented network boundaries.
- Approved exercise cards for segmentation, remote-access oversight and alert triage.
- Passive evidence collection and expected-response worksheets.
- Safety constraints, emergency stop, reset scripts and post-exercise report.

### Validation & success criteria

Prove there is no route from the range to production OT. Validate segmentation using lab-only allow/deny fixtures. Exercise stop and reset procedures before scenarios begin. Confirm that every scenario preserves the defined simulated safe state or triggers the expected instructor stop. Reports must distinguish simulated behavior from conclusions about real plant safety.

**Roadmap:** Agree training objectives with an OT owner; build the isolated process range; validate boundaries and resets; run supervised exercises. Live PLC exploitation, safety-system manipulation, firmware modification and production disruption are excluded.

---

## CL-RT-10 — GeoTrust Adversarial Lab

**Industry:** Logistics, fleet operations and connected-asset platforms.  
**Project type:** Geofencing and telemetry integrity red teaming with AI-assisted analysis.  
**Status:** Runnable lab prototype published; the broader architecture below remains a design roadmap.

**Code:** [geotrust_lab.py](geotrust_lab.py) · [Setup & run guide](CODE_GUIDE.md)  
**Run:** `python geotrust_lab.py`  
**Implemented now:** Circular geofences with accuracy margins and hysteresis, plus replay, stale/future telemetry and implausible-speed checks.

### Business problem

Location-based alerts can fail when telemetry is delayed, replayed, inaccurate or inconsistent with device identity. An attacker-controlled location claim must not become trusted solely because it falls inside a boundary.

### Proposed solution & architecture

A synthetic route generator creates normal and adversarial telemetry sequences for virtual assets. An ingestion gateway validates device identity, timestamps and replay controls. A geofence engine evaluates entry/exit rules with configurable accuracy margins and hysteresis. An AI-assisted analyzer groups anomalies for review while deterministic policies govern access or alerts.

**Components:** synthetic route generator; authenticated telemetry gateway; replay-control service; geofence engine; event bus; anomaly review; operations dashboard.

**Suggested stack:** Python or TypeScript, PostgreSQL/PostGIS, a message broker, a map UI and a deterministic policy engine. Location datasets contain virtual assets only.

### Deliverables

- Boundary/rule catalogue and telemetry trust model.
- Test cases for stale coordinates, duplicate messages, impossible jumps and boundary jitter.
- Event dashboard, alert-routing rules and replay-analysis report.
- Retention, consent and device-onboarding design documentation.

### Validation & success criteria

Replayed messages must not create duplicate entry/exit events. Stale or unverifiable location claims must be rejected or explicitly marked uncertain. Test accuracy margins and hysteresis against documented expected outcomes. Record missed events, false alerts and processing latency under an agreed synthetic load. AI anomaly scores must never override identity or authorization checks.

**Roadmap:** Implement the synthetic telemetry model; build deterministic geofence and replay checks; add dashboards and reviewed anomaly explanations; validate a controlled pilot with consenting asset owners. Covert tracking and interception of third-party devices are excluded.

---

## Implementation handover package

A commissioned implementation should deliver the following, scoped to the selected project:

| Area | Required output |
| :--- | :--- |
| Product | Approved requirements, users, workflows and acceptance criteria |
| Architecture | Trust boundaries, data flows, interfaces and deployment design |
| Source | Version-controlled implementation, dependency manifest and build instructions |
| Testing | Unit/integration tests, safe fixtures, validation results and known limitations |
| Operations | Monitoring, backups, incident handling, rollback and teardown procedures |
| Security | Threat model, access matrix, secrets handling and reviewed findings |
| AI assurance | Model/configuration record, evaluation dataset, human-review process and measured limitations |
| Documentation | Deployment guide, operator guide, administrator guide and evidence-backed project report |

**Release readiness:** The published scripts are runnable lab prototypes with setup instructions and offline regression coverage. They implement only the scope stated under each project’s “Implemented now” entry. Pilot readiness requires the remaining integrations, acceptance tests, security review and owner approval. Production readiness requires environment-specific validation, operating ownership and an agreed support model.

## Discuss a project

Visit [Cyberlegends.org](https://cyberlegends.org) and reference the project ID. Start with your business objective, target environment, authorized scope, data sensitivity and preferred delivery window. Arrange a private channel before exchanging system inventories, evidence or credentials.

**Cyber Legends — Secure systems. Clear evidence. Trusted intelligence.**
