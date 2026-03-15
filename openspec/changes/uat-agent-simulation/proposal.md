## Why

To validate the Glasshouse protocol through comprehensive user acceptance testing (UAT) with actual agent interactions, ensuring the system works end-to-end before production deployment. This addresses the need for realistic simulation of the agent economy to identify integration issues and performance bottlenecks early.

## What Changes

- Introduce simulation capabilities for requester agents that make actual API calls to faucet/claim and post realistic jobs.
- Add simulation for worker agents that actually run posted jobs.
- Implement simulation for verifier agents that verify completed jobs using proof guidance from worker agents.
- Create automated test scenarios that mimic real-world agent interactions.

## Capabilities

### New Capabilities
- `agent-faucet-claiming`: Simulation of agents claiming tokens from the faucet endpoint
- `job-posting-simulation`: Simulation of posting realistic jobs with proper metadata and requirements
- `job-execution-simulation`: Simulation of worker agents executing jobs and generating proof artifacts
- `job-verification-simulation`: Simulation of verifier agents validating job completion with worker-provided proofs

### Modified Capabilities
<!-- No existing capabilities are modified -->

## Impact

- Backend API endpoints (faucet/claim, jobs posting, verification)
- Database schema for tracking simulated agent interactions
- Testing infrastructure and automation scripts
- Performance monitoring for agent simulation workloads