from typing import Dict, Any, Optional
import time
import random
import logging
from base_agent import BaseAgent

logger = logging.getLogger(__name__)

class VerifierAgent(BaseAgent):
    """Agent that verifies job completion proofs."""

    def __init__(self, agent_id: str, api_token: str, base_url: str = "http://127.0.0.1:8000"):
        super().__init__(agent_id, api_token, base_url)
        self.verification_history = []

    def verify_job(self, job_id: str, proof: Dict[str, Any]) -> Dict[str, Any]:
        """Verify a job proof and return verification result."""
        try:
            # Simulate verification process
            verification_time = random.uniform(0.5, 2.0)
            time.sleep(verification_time)

            # Check proof validity (mock consensus check)
            is_valid = self._validate_proof(proof)

            result = {
                'job_id': job_id,
                'verifier_id': self.agent_id,
                'timestamp': time.time(),
                'is_valid': is_valid,
                'verification_time': verification_time,
                'consensus_score': random.uniform(0.8, 1.0) if is_valid else random.uniform(0.0, 0.7)
            }

            self.verification_history.append(result)

            if is_valid:
                logger.info(f"Agent {self.agent_id} verified job {job_id} successfully")
            else:
                logger.warning(f"Agent {self.agent_id} rejected verification for job {job_id}")

            return result

        except Exception as e:
            logger.error(f"Agent {self.agent_id} verification error for job {job_id}: {e}")
            return {
                'job_id': job_id,
                'verifier_id': self.agent_id,
                'is_valid': False,
                'error': str(e)
            }

    def submit_verification(self, job_id: str, verification_result: Dict[str, Any]) -> bool:
        """Submit verification result to the API."""
        try:
            response = self.post(f'/api/jobs/{job_id}/results', data=verification_result)
            if response.status_code == 200:
                logger.info(f"Agent {self.agent_id} submitted verification for job {job_id}")
                return True
            else:
                logger.error(f"Agent {self.agent_id} verification submission failed: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"Agent {self.agent_id} verification submission error: {e}")
            return False

    def _validate_proof(self, proof: Dict[str, Any]) -> bool:
        """Validate the proof artifact."""
        # Mock validation logic
        required_fields = ['job_id', 'agent_id', 'timestamp', 'output_hash', 'execution_details']
        if not all(field in proof for field in required_fields):
            return False

        # Simulate random validation with bias toward success
        return random.random() < 0.9  # 90% success rate

    def get_verification_stats(self) -> Dict[str, int]:
        """Get verification statistics."""
        total = len(self.verification_history)
        valid = sum(1 for v in self.verification_history if v.get('is_valid', False))
        return {
            'total_verifications': total,
            'successful_verifications': valid,
            'failed_verifications': total - valid
        }