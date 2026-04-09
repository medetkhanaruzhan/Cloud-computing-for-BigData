# ProposalAI — AI Technical Proposal Generator
### SIS Week 12 · Integrated Agentic Mini-Project

A full-featured Streamlit dashboard that generates structured technical proposals
(CCTV, Networking, POS, IT Infrastructure) for SME clients — acting as an
AI-assisted pre-sales engineering tool.

---

## Quick start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app
streamlit run app.py
```

The app opens at `http://localhost:8501` in your browser.

---

## Structure

```
app.py            ← single-file Streamlit application (modular functions)
requirements.txt  ← Python dependencies
README.md         ← this file
```

### Key modules inside app.py

| Section | Purpose |
|---|---|
| Data models | `ProposalRequest`, `BOMLine`, `ProposalScore`, `Insight`, `MonitoringSnapshot` |
| Domain calculators | `calculate_cctv_bom`, `calculate_networking_bom`, `calculate_pos_bom`, `calculate_it_bom` |
| Scoring engine | `score_proposal` — cost, risk, scalability axes |
| Summary generator | `generate_executive_summary` — rule-based narrative |
| Insights engine | `generate_insights` — flag detection and advice |
| Monitoring mock | `generate_monitoring` — token/cost/confidence telemetry |
| Orchestrator | `generate_proposal` — routes and assembles results |
| UI helpers | `render_metric_row`, `render_bom_table`, `render_monitoring`, etc. |
| Main | `main()` — two-column layout, session state, empty state |

---

## IT4IT mapping

| Stream | Implementation |
|---|---|
| S2P | Input form captures the business problem and budget |
| R2D | Domain calculators + scoring engine = AI decision logic |
| R2F | Dashboard output: BoM, summary, PDF-printable layout |
| D2C | Monitoring panel: tokens, cost, confidence, error flags |

---

## Notes

- No external API keys required — all logic is rule-based for offline demo
- To connect a real LLM, replace `generate_executive_summary()` with an `anthropic.Anthropic().messages.create()` call
- Currency toggle supports USD and KZT (rate hardcoded at 450)
- Export: use browser print (Ctrl+P → Save as PDF)
