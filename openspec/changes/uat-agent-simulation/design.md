## Context

This design implements the UAT agent simulation system outlined in the proposal. The current Glasshouse protocol supports agent interactions via API endpoints, but lacks automated testing of end-to-end agent workflows. This change introduces simulation capabilities to validate the protocol with realistic agent behaviors, including faucet claiming, job posting, execution, and verification.

The simulation will run against the live backend API to ensure integration testing accuracy, while providing configurable parameters for different test scenarios.

## Goals / Non-Goals

**Goals:**
- Create automated UAT scenarios that simulate complete agent interaction cycles
- Validate API endpoints under realistic load and usage patterns
- Identify integration issues and performance bottlenecks before production deployment
- Provide reusable simulation framework for future testing

**Non-Goals:**
- Implement production-ready agent clients
- Replace manual QA testing processes
- Add monitoring or analytics beyond simulation logging
- Support distributed simulation across multiple machines

## Decisions

**Simulation Framework:** Use Python asyncio for concurrent agent simulations to mimic real-world parallelism. Alternative: Threading was considered but asyncio provides better control over concurrent API calls.

**API Client:** Use the requests library for HTTP calls to ensure compatibility with the existing backend. Alternative: httpx was considered for async support but requests is simpler and sufficient for simulation needs.

**Agent Classes:** Create separate simulation classes (RequesterAgent, WorkerAgent, VerifierAgent) inheriting from a base Agent class. This allows polymorphic behavior and easy extension.

**Configuration:** Use YAML files for simulation parameters (number of agents, job types, timing). Alternative: JSON was considered but YAML is more human-readable for test configurations.

**Logging:** Implement structured logging with different levels for simulation events, API responses, and errors. Use Python's logging module with JSON format for easy parsing.

## Agent Skillsets

To create realistic simulations, agents will be assigned specialized skillsets that determine the types of jobs they can execute. These skillsets reflect common AI agent capabilities in the Glasshouse ecosystem, including emerging agent-to-agent (A2A) service categories:

- **Trust & Reputation Services:** Verifiable identity management, credit scoring, proof-of-computation validation
- **Micropayment Infrastructure:** Nanopayment processing, escrow services, real-time auctions
- **Specialized Gig Labor:** Security red teaming, data janitorial services, creative subcontracting
- **Human-in-the-Loop Services:** CAPTCHA solving, compliance notarization, physical signature handling
- **Governance & Guardrails:** Real-time observability, legal mapping, hallucination prevention
- **Data Analysis:** Statistical analysis, data cleaning, visualization, and insights generation
- **Content Generation:** Text writing, creative content, documentation, and summarization
- **Image Processing:** Image recognition, manipulation, generation, and computer vision tasks
- **Code Development:** Programming, debugging, code review, and software engineering
- **Research & Synthesis:** Information gathering, literature review, and knowledge synthesis
- **Automation:** Workflow optimization, script creation, and process automation
- **Translation:** Language translation, localization, and multilingual content handling
- **Security Analysis:** Vulnerability scanning, threat detection, and compliance checking
- **Financial Modeling:** Economic analysis, forecasting, and financial data processing
- **Customer Service:** Query handling, support automation, and user interaction simulation

Each worker agent will be randomly assigned 1-3 skillsets during simulation initialization, with proficiency levels (beginner, intermediate, expert) affecting job success rates and execution times. The A2A service categories represent high-demand market segments where agents provide infrastructure services to other agents, creating a meta-economy of agent collaboration.

## Job Types

To simulate realistic agent interactions, the UAT system will include diverse job posting types that reflect common outsourcing scenarios in the agent economy:

**Local Specialist Jobs:**
- Legacy code debugging and patching
- Jurisdiction-specific compliance reviews
- Domain-specific sentiment analysis

**Heavy Lifter Jobs:**
- In-situ log analysis on remote data stores
- GPU/CPU-intensive rendering or compilation
- Large-scale data processing without data transfer

**Connector Jobs:**
- Network introductions and handshake protocols
- Identity verification and vouching
- Private API access and proxy queries

**Human Wrangler Jobs:**
- CAPTCHA solving and 2FA verification
- Physical IoT actuation and hardware control
- Real-world sensor data collection

**Arbitrageur Jobs:**
- Compute spot market bidding
- Background process offloading
- Resource optimization auctions

Jobs will include metadata for data locality, required trust levels, and hardware access needs to enable efficient matching and execution.

## Risks / Trade-offs

**API Overload Risk:** High concurrency could overwhelm the backend → Mitigation: Implement configurable delays and rate limiting in simulations.

**Database Contention:** Multiple simulations hitting the database simultaneously → Mitigation: Use connection pooling and add random delays between operations.

**Unrealistic Simulation:** Simulations may not capture all edge cases → Mitigation: Base scenarios on real usage patterns and allow manual override of parameters.

**Test Data Pollution:** Simulations create real data that could interfere with other tests → Mitigation: Use dedicated test database or cleanup scripts.

## Migration Plan

This is a new feature with no existing code to migrate. Deployment involves:
1. Add simulation scripts to the tests/ directory
2. Update CI/CD pipeline to include UAT simulation runs
3. Document simulation usage in README

Rollback: Remove simulation files if issues arise.

## Open Questions

- What are the optimal simulation parameters (number of agents, job frequency) for meaningful UAT?
- Should simulations include error injection for fault tolerance testing?
- How to handle authentication/authorization for simulated agents?