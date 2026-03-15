from typing import Dict, Any, List, Optional
import time
import random
import logging
from base_agent import BaseAgent
from skillsets import SKILLSET_CATEGORIES, JOB_TYPES, PROFICIENCY_LEVELS

logger = logging.getLogger(__name__)

class WorkerAgent(BaseAgent):
    """Agent that executes jobs and generates proof artifacts."""

    def __init__(self, agent_id: str, api_token: str, base_url: str = "http://127.0.0.1:8000",
                 skillsets: Optional[List[str]] = None, proficiency: str = 'intermediate'):
        super().__init__(agent_id, api_token, base_url)
        self.skillsets = skillsets or random.sample(list(SKILLSET_CATEGORIES.keys()), random.randint(1, 3))
        self.proficiency = proficiency
        self.balance = 0
        # Simulate hardware capabilities
        self.hardware_capabilities = self._generate_hardware_capabilities()

    def _generate_hardware_capabilities(self) -> List[str]:
        """Generate random hardware capabilities for this agent."""
        possible_hardware = ['cpu', 'gpu', 'iot_controller', 'network_access', 'api_access', 'legal_database_access']
        # Most agents have basic CPU, some have specialized hardware
        capabilities = ['cpu']
        if random.random() < 0.3:  # 30% chance
            capabilities.append('gpu')
        if random.random() < 0.2:  # 20% chance
            capabilities.extend(random.sample(['iot_controller', 'network_access', 'api_access'], random.randint(1, 2)))
        return capabilities

    def can_execute_job(self, job_data: Dict[str, Any]) -> bool:
        """Check if this agent can execute the job based on skills and requirements."""
        job_type = job_data.get('type')
        if job_type and job_type in JOB_TYPES:
            job_config = JOB_TYPES[job_type]
            required_skills = job_config['required_skills']
            required_hardware = job_config.get('hardware_requirements', [])

            skill_match = any(skill in self.skillsets for skill in required_skills)
            hardware_match = all(hw in self.hardware_capabilities for hw in required_hardware)

            return skill_match and hardware_match

        # Fallback to manual skill check
        required_skills = job_data.get('required_skills', [])
        if not required_skills:
            return True  # No specific skills required

        return any(skill in self.skillsets for skill in required_skills)

    def _generate_hardware_capabilities(self) -> List[str]:
        """Generate random hardware capabilities for this agent."""
        possible_hardware = ['cpu', 'gpu', 'network_access', 'api_access', 'iot_controller', 'legal_database_access']
        # Most agents have CPU, some have GPU, few have specialized hardware
        capabilities = ['cpu']
        if random.random() < 0.3:  # 30% chance
            capabilities.append('gpu')
        if random.random() < 0.2:  # 20% chance
            capabilities.extend(random.sample(['network_access', 'api_access', 'iot_controller', 'legal_database_access'], random.randint(1, 2)))
        return capabilities

    def accept_job(self, job_id: str) -> bool:
        """Accept a job for execution."""
        try:
            response = self.post(f'/api/jobs/{job_id}/accept', data={})
            if response.status_code == 200:
                logger.info(f"Agent {self.agent_id} accepted job {job_id}")
                return True
            else:
                logger.warning(f"Agent {self.agent_id} failed to accept job {job_id}: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"Agent {self.agent_id} accept job error: {e}")
            return False

    def execute_job(self, job_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a job and generate proof artifact."""
        job_type = job_data.get('type', 'generic')

        # Get complexity from JOB_TYPES or default
        complexity = JOB_TYPES.get(job_type, {}).get('complexity', 1.0)
        execution_time = self._calculate_execution_time(complexity)

        # Simulate execution time
        time.sleep(execution_time)

        # Calculate success based on proficiency
        success_rate = {'beginner': 0.7, 'intermediate': 0.85, 'expert': 0.95}[self.proficiency]
        success = random.random() < success_rate

        if success:
            proof = self._generate_proof(job_data)
            logger.info(f"Agent {self.agent_id} successfully executed job {job_data.get('id')} in {execution_time:.2f}s")
            return {
                'status': 'completed',
                'proof': proof,
                'execution_time': execution_time
            }
        else:
            logger.warning(f"Agent {self.agent_id} failed to execute job {job_data.get('id')}")
            return {
                'status': 'failed',
                'error': 'Execution failed',
                'execution_time': execution_time
            }

    def submit_proof(self, job_id: str, proof: Dict[str, Any]) -> bool:
        """Submit proof artifact for job verification."""
        try:
            response = self.post(f'/api/jobs/{job_id}/results', data=proof)
            if response.status_code == 200:
                # Receive payment
                payment = proof.get('payment_amount', 0)
                self.balance += payment
                logger.info(f"Agent {self.agent_id} submitted proof for job {job_id}, received {payment} tokens. Balance: {self.balance}")
                return True
            else:
                logger.error(f"Agent {self.agent_id} proof submission failed: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"Agent {self.agent_id} proof submission error: {e}")
            return False

    def _calculate_execution_time(self, complexity: float) -> float:
        """Calculate execution time based on job complexity and agent proficiency."""
        proficiency_multiplier = {'beginner': 1.5, 'intermediate': 1.0, 'expert': 0.7}[self.proficiency]
        return complexity * proficiency_multiplier * random.uniform(0.8, 1.2)

    def _generate_proof(self, job_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a proof artifact for the completed job."""
        return {
            'job_id': job_data.get('id'),
            'agent_id': self.agent_id,
            'timestamp': time.time(),
            'output_hash': f"hash_{random.randint(1000, 9999)}",  # Mock hash
            'execution_details': {
                'skills_used': self.skillsets,
                'proficiency': self.proficiency,
                'computation_steps': random.randint(10, 100)
            },
            'payment_amount': job_data.get('payment_amount', 0)
        }

    def get_balance(self) -> int:
        """Get current token balance."""
        return self.balance