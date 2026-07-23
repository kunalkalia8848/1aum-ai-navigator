\# Architecture Decision Records (ADR) Log



This document records the architectural and design decisions made during the development of \*\*1AUM Navigator\*\*.



\---



\## ADR-001: Streamlit instead of React



\* \*\*Decision:\*\* Use Streamlit for the MVP.

\* \*\*Reason:\*\* The product is workflow- and data-oriented. Streamlit allows rapid development, visualization, and deployment within a single unified Python codebase.

\* \*\*Tradeoff:\*\* The interface has less custom CSS/design flexibility compared to a custom React application.

\* \*\*Future Trigger:\*\* Reassess after validating user demand and complex UI workflow requirements.



\---



\## ADR-002: JSON / In-Memory Session State before SQLite / PostgreSQL



\* \*\*Decision:\*\* Use Streamlit `session\_state` and local JSON dictionaries for state management.

\* \*\*Reason:\*\* Simplifies client-side assessment evaluation without requiring database infrastructure setup, schema migrations, or connection credentials.

\* \*\*Tradeoff:\*\* Multi-session persistence and enterprise user data historical tracking are not supported out of the box.

\* \*\*Future Trigger:\*\* Reassess when adding multi-user accounts, workspace collaboration, or saved assessment history.



\---



\## ADR-003: DOCX Export before PDF



\* \*\*Decision:\*\* Prioritize `.docx` document generation via `python-docx` over static PDF export.

\* \*\*Reason:\*\* Enterprise executives and strategy teams prefer editable report formats so they can refine recommendations before presenting to stakeholders.

\* \*\*Tradeoff:\*\* Visual layout consistency relies on Microsoft Word / document viewers rather than pixel-perfect PDF rendering.

\* \*\*Future Trigger:\*\* Add optional PDF rendering after stabilizing document templates.



\---



\## ADR-004: No Authentication in MVP



\* \*\*Decision:\*\* Omit login, user registration, and role-based access control (RBAC) in the initial release.

\* \*\*Reason:\*\* Eliminates user onboarding friction during demonstration, testing, and initial client walkthroughs.

\* \*\*Tradeoff:\*\* Anyone with the app URL can execute assessments in public deployment mode.

\* \*\*Future Trigger:\*\* Implement OAuth/SSO when migrating to a multi-tenant SaaS environment.



\---



\## ADR-005: Deterministic Scoring Engine



\* \*\*Decision:\*\* Rely strictly on explicit mathematical functions in Python for all readiness scores, priority indices, risk ratings, and roadmap gap-closure triggers.

\* \*\*Reason:\*\* Prevents LLM hallucinations, guarantees 100% mathematical reproducibility, and ensures complete auditability in risk-sensitive environments.

\* \*\*Tradeoff:\*\* Scoring logic is rule-based and requires explicit module code updates to adjust weighting formulas.

\* \*\*Future Trigger:\*\* Reassess if configurable scoring weights need to be exposed via UI sliders.



\---



\## ADR-006: Controlled Risk Templates



\* \*\*Decision:\*\* Use predefined risk categories, severity mappings, and mitigation templates for known enterprise AI risks.

\* \*\*Reason:\*\* Standardizes risk evaluations against established AI governance frameworks (e.g., NIST AI RMF / EU AI Act principles).

\* \*\*Tradeoff:\*\* Users must select from structured categories rather than free-form unstructured risk text.

\* \*\*Future Trigger:\*\* Allow custom user-created risk taxonomies in addition to standardized templates.



\---



\## ADR-007: Optional LLM Integration Layer



\* \*\*Decision:\*\* Design LLM integration as an optional narrative polish layer with deterministic fallback templates.

\* \*\*Reason:\*\* Ensures the core assessment tool remains 100% operational even without API key configuration or during external API outages.

\* \*\*Tradeoff:\*\* Narrative summaries generated without an active API key rely on standardized text templates rather than fully tailored prose.

\* \*\*Future Trigger:\*\* Reassess default models as new cost-effective, high-throughput LLM endpoints become available.



\---



\## ADR-008: No Permanent User-Data Retention



\* \*\*Decision:\*\* Process all assessment inputs strictly in memory without persistent cloud storage logging.

\* \*\*Reason:\*\* Protects corporate data privacy and eliminates sensitive organizational risk posture logging on public cloud servers.

\* \*\*Tradeoff:\*\* Users must download their `.docx` executive report before closing the browser tab.

\* \*\*Future Trigger:\*\* Add optional local workspace export/import (e.g., `.json` state export) for offline session saving.

