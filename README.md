# End-of-Day (EOD) Market Data Validator & Incident Routing Engine

## Project Overview
This production support utility mimics a critical Capital Markets IT environment data-integrity sentinel. It is engineered to process daily End-of-Day (EOD) market transaction feeds, systematically parse data validation streams, and isolate production-impacting anomalies before systemic risks compromise downstream trade processing layers, Risk engines, or PnL processing pipelines.

## Key Automated Protections
- **Missing Data Extraction:** Identifies empty records in critical pricing or trade execution volume fields.
- **Business Logic Breach Isolation:** Flags negative value errors that violate financial trading boundary frameworks.
- **Market Variance Detection:** Triggers real-time alerts for sudden high-volatility pricing data spikes.
- **Enterprise Alert Integration:** Outputs formatted data log reports and mimics a JSON payload transmission structure ready to seed downstream ticketing systems like ServiceNow or Jira.

