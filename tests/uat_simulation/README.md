# UAT Agent Simulation

This directory contains the User Acceptance Testing (UAT) simulation system for the Glasshouse Protocol. The simulation creates realistic agent interactions to validate the protocol's end-to-end functionality.

## Overview

The UAT simulation includes:
- Multiple agent types (Requester, Worker, Verifier)
- Diverse job types based on real agent economy scenarios
- Skill-based job matching with proficiency levels
- Hardware capability requirements
- Performance monitoring and structured logging
- Automated test scenarios based on user stories

## Configuration

Simulation parameters are configured via YAML files. Create a `config/uat_config.yaml` file:

```yaml
simulation:
  duration_seconds: 300
  num_requesters: 5
  num_workers: 10
  num_verifiers: 3
  concurrency_level: 10

agents:
  base_url: 'http://127.0.0.1:8000'
  api_tokens:
    - 'token1'
    - 'token2'
    # Add more tokens as needed

jobs:
  types:
    - name: 'data_processing'
      complexity: 2.0
      payment: 10
    - name: 'content_generation'
      complexity: 1.5
      payment: 8
  posting_interval_seconds: 5

logging:
  level: 'INFO'
  format: 'json'
  file: 'uat_simulation.log'
```

## Usage

### Running UAT Scenarios

```bash
# Run all UAT scenarios
python tests/uat_simulation/run_uat.py

# Run specific scenario
python -c "from simulation_runner import SimulationRunner; asyncio.run(SimulationRunner().run_scenario('buyer_financial_portfolio'))"
```

### Manual Simulation

```python
from uat_simulation import RequesterAgent, WorkerAgent, VerifierAgent
from uat_simulation.config import config

# Create agents
requester = RequesterAgent('req-001', 'token1')
worker = WorkerAgent('work-001', 'token2')
verifier = VerifierAgent('ver-001', 'token3')

# Simulate interaction
job_id = requester.post_job({
    'type': 'data_processing',
    'title': 'Process dataset',
    'payment_amount': 10
})

if job_id:
    worker.accept_job(job_id)
    result = worker.execute_job({'id': job_id, 'type': 'data_processing'})
    if result['status'] == 'completed':
        proof = result['proof']
        verification = verifier.verify_job(job_id, proof)
        verifier.submit_verification(job_id, verification)
```

## Agent Types

### RequesterAgent
- Claims tokens from faucet
- Posts jobs with payment reservation
- Handles rate limiting and insufficient funds

### WorkerAgent
- Matches jobs based on skills and hardware capabilities
- Executes jobs with configurable success rates
- Generates proof artifacts
- Supports different proficiency levels

### VerifierAgent
- Validates proof artifacts
- Performs consensus checking
- Tracks verification statistics

## Job Types

Jobs are categorized by required skills and hardware:

- **data_processing**: Data analysis tasks
- **content_generation**: Text creation and editing
- **code_review**: Programming and code analysis
- **security_audit**: Vulnerability assessment
- **identity_verification**: Trust and reputation tasks
- **gpu_rendering**: GPU-intensive processing
- **iot_actuation**: Hardware control tasks

## Skillsets

Agents have specialized skillsets:

- **Technical**: data_analysis, content_generation, code_development, etc.
- **A2A Service**: trust_reputation, micropayments, specialized_labor, etc.

## Logging

The simulation uses structured JSON logging with performance metrics:

- **simulation**: High-level simulation events
- **agent**: Individual agent actions
- **job**: Job lifecycle events
- **performance**: Metrics and timing data

Logs are written to `uat_simulation.log` by default.

## Cleanup

After running simulations, clean up test data:

```bash
python tests/uat_simulation/cleanup.py
```

## CI/CD Integration

The `run_uat.py` script can be integrated into CI/CD pipelines:

```bash
# In your CI script
python tests/uat_simulation/run_uat.py
if [ $? -ne 0 ]; then
    echo "UAT failed"
    exit 1
fi
```

## Performance Monitoring

The simulation includes performance monitoring:

- API response times
- Job execution durations
- Agent success rates
- System throughput metrics

Monitor logs for performance data during test runs.