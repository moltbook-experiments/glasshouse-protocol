import asyncio
import logging
from typing import List, Dict, Any
from concurrent.futures import ThreadPoolExecutor
import time
import random

from config import config
from logger import setup_logging, log_simulation_event
from requester_agent import RequesterAgent
from worker_agent import WorkerAgent
from verifier_agent import VerifierAgent
from skillsets import JOB_TYPES, get_random_skillsets
from performance_monitor import get_performance_monitor

logger = logging.getLogger(__name__)

class SimulationRunner:
    """Manages concurrent UAT simulation of agent interactions."""

    def __init__(self, config_obj=None):
        self.config = config_obj or config
        self.requesters: List[RequesterAgent] = []
        self.workers: List[WorkerAgent] = []
        self.verifiers: List[VerifierAgent] = []
        self.performance_monitor = get_performance_monitor()

    async def initialize_agents(self):
        """Initialize all simulation agents."""
        loop = asyncio.get_event_loop()

        # Create requesters
        num_requesters = self.config.get('simulation.num_requesters', 5)
        api_tokens = self.config.get('agents.api_tokens', [f"token_{i}" for i in range(100)])  # Mock tokens

        for i in range(num_requesters):
            agent = RequesterAgent(
                agent_id=f"requester_{i}",
                api_token=api_tokens[i % len(api_tokens)],
                base_url=self.config.get('agents.base_url')
            )
            self.requesters.append(agent)

        # Create workers
        num_workers = self.config.get('simulation.num_workers', 10)
        proficiency_dist = self.config.get('agents.proficiency_distribution')

        for i in range(num_workers):
            proficiency = self._select_proficiency(proficiency_dist)
            skillsets = get_random_skillsets()
            agent = WorkerAgent(
                agent_id=f"worker_{i}",
                api_token=api_tokens[(i + num_requesters) % len(api_tokens)],
                base_url=self.config.get('agents.base_url'),
                skillsets=skillsets,
                proficiency=proficiency
            )
            self.workers.append(agent)

        # Create verifiers
        num_verifiers = self.config.get('simulation.num_verifiers', 3)
        for i in range(num_verifiers):
            agent = VerifierAgent(
                agent_id=f"verifier_{i}",
                api_token=api_tokens[(i + num_requesters + num_workers) % len(api_tokens)],
                base_url=self.config.get('agents.base_url')
            )
            self.verifiers.append(agent)

        log_simulation_event('agents_initialized', {
            'requesters': num_requesters,
            'workers': num_workers,
            'verifiers': num_verifiers
        })

    def _select_proficiency(self, distribution: Dict[str, float]) -> str:
        """Select proficiency level based on distribution."""
        import random
        rand = random.random()
        cumulative = 0.0
        for level, prob in distribution.items():
            cumulative += prob
            if rand <= cumulative:
                return level
        return 'intermediate'  # fallback

    async def run_simulation(self, duration_seconds: int = None):
        """Run the complete simulation."""
        if duration_seconds is None:
            duration_seconds = self.config.get('simulation.duration_seconds', 300)

        log_simulation_event('simulation_started', {'duration': duration_seconds})

        start_time = time.time()
        end_time = start_time + duration_seconds

        # Create concurrent tasks
        tasks = []

        # Requester tasks: claim tokens and post jobs
        for requester in self.requesters:
            task = asyncio.create_task(self._run_requester_cycle(requester, end_time))
            tasks.append(task)

        # Worker tasks: find and execute jobs
        for worker in self.workers:
            task = asyncio.create_task(self._run_worker_cycle(worker, end_time))
            tasks.append(task)

        # Verifier tasks: verify completed jobs
        for verifier in self.verifiers:
            task = asyncio.create_task(self._run_verifier_cycle(verifier, end_time))
            tasks.append(task)

        # Wait for all tasks to complete or timeout
        try:
            await asyncio.wait_for(asyncio.gather(*tasks, return_exceptions=True), timeout=duration_seconds)
        except asyncio.TimeoutError:
            logger.info("Simulation duration reached, stopping tasks")

        log_simulation_event('simulation_completed', {
            'actual_duration': time.time() - start_time,
            'total_requesters': len(self.requesters),
            'total_workers': len(self.workers),
            'total_verifiers': len(self.verifiers)
        })

    async def _run_requester_cycle(self, requester: RequesterAgent, end_time: float):
        """Run the requester's behavior cycle."""
        posting_interval = self.config.get('jobs.posting_interval_seconds', 5)

        while time.time() < end_time:
            # Claim tokens if needed
            if requester.get_balance() < 10:  # Minimum balance
                await asyncio.get_event_loop().run_in_executor(
                    self.executor, requester.claim_faucet
                )

            # Post a job
            job_data = self._generate_random_job()
            await asyncio.get_event_loop().run_in_executor(
                self.executor, requester.post_job, job_data
            )

            await asyncio.sleep(posting_interval)

    async def _run_worker_cycle(self, worker: WorkerAgent, end_time: float):
        """Run the worker's behavior cycle."""
        while time.time() < end_time:
            # Find available jobs (mock - in real implementation, query API)
            available_jobs = await self._find_available_jobs(worker)

            for job in available_jobs:
                if worker.can_execute_job(job):
                    # Accept and execute job
                    accepted = await asyncio.get_event_loop().run_in_executor(
                        self.executor, worker.accept_job, job['id']
                    )
                    if accepted:
                        result = await asyncio.get_event_loop().run_in_executor(
                            self.executor, worker.execute_job, job
                        )
                        if result['status'] == 'completed':
                            await asyncio.get_event_loop().run_in_executor(
                                self.executor, worker.submit_proof, job['id'], result['proof']
                            )

            await asyncio.sleep(1)  # Check for jobs every second

    async def _run_verifier_cycle(self, verifier: VerifierAgent, end_time: float):
        """Run the verifier's behavior cycle."""
        while time.time() < end_time:
            # Find jobs needing verification (mock)
            jobs_to_verify = await self._find_jobs_needing_verification()

            for job_id, proof in jobs_to_verify:
                verification = await asyncio.get_event_loop().run_in_executor(
                    self.executor, verifier.verify_job, job_id, proof
                )
                if verification['is_valid']:
                    await asyncio.get_event_loop().run_in_executor(
                        self.executor, verifier.submit_verification, job_id, verification
                    )

            await asyncio.sleep(2)  # Check every 2 seconds

    def _generate_random_job(self) -> Dict[str, Any]:
        """Generate a random job for posting."""
        job_types = list(JOB_TYPES.keys())
        job_type = random.choice(job_types)
        job_config = JOB_TYPES[job_type]

        return {
            'type': job_type,
            'title': f"Sample {job_type.replace('_', ' ')} job",
            'description': f"Automated test job for {job_type}",
            'payment_amount': job_config['base_payment'],
            'required_skills': job_config['required_skills'],
            'complexity': job_config['complexity']
        }

    async def _find_available_jobs(self, worker: WorkerAgent) -> List[Dict[str, Any]]:
        """Mock: Find available jobs (in real impl, query API)."""
        # For simulation, return some mock jobs
        return [
            {
                'id': f"job_{random.randint(1000, 9999)}",
                'type': random.choice(list(JOB_TYPES.keys())),
                'payment_amount': 10
            }
            for _ in range(random.randint(0, 3))  # 0-3 jobs
        ]

    async def _find_jobs_needing_verification(self) -> List[tuple]:
        """Mock: Find jobs needing verification."""
        # Return mock job-proof pairs
        return [
            (f"job_{random.randint(1000, 9999)}", {'mock': 'proof'})
            for _ in range(random.randint(0, 2))  # 0-2 jobs
        ]

async def run_uat_simulation(config_file: str = None):
    """Main entry point for UAT simulation."""
    if config_file:
        config.load_config(config_file)

    setup_logging()

    runner = SimulationRunner()
    await runner.initialize_agents()
    await runner.run_simulation()

if __name__ == "__main__":
    asyncio.run(run_uat_simulation())