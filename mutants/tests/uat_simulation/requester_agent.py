from typing import Dict, Any, Optional
import time
import logging
from base_agent import BaseAgent

logger = logging.getLogger(__name__)

class RequesterAgent(BaseAgent):
    """Agent that requests work by claiming tokens and posting jobs."""

    def __init__(self, agent_id: str, api_token: str, base_url: str = "http://127.0.0.1:8000"):
        super().__init__(agent_id, api_token, base_url)
        self.balance = 0  # Track token balance for simulation

    def claim_faucet(self) -> bool:
        """Claim tokens from the faucet endpoint."""
        try:
            response = self.post('/api/faucet/claim', data={})
            if response.status_code == 200:
                data = response.json()
                tokens_received = data.get('tokens', 0)
                self.balance += tokens_received
                logger.info(f"Agent {self.agent_id} claimed {tokens_received} tokens. Balance: {self.balance}")
                return True
            elif response.status_code == 429:
                logger.warning(f"Agent {self.agent_id} hit rate limit on faucet claim")
                return False
            else:
                logger.error(f"Agent {self.agent_id} faucet claim failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            logger.error(f"Agent {self.agent_id} faucet claim error: {e}")
            return False

    def post_job(self, job_data: Dict[str, Any]) -> Optional[str]:
        """Post a job and return the job ID if successful."""
        try:
            # Check if we have sufficient tokens
            payment_amount = job_data.get('payment_amount', 0)
            if self.balance < payment_amount:
                logger.warning(f"Agent {self.agent_id} insufficient balance: {self.balance} < {payment_amount}")
                return None

            response = self.post('/api/jobs', data=job_data)
            if response.status_code == 201:
                data = response.json()
                job_id = data.get('job_id')
                # Reserve tokens
                self.balance -= payment_amount
                logger.info(f"Agent {self.agent_id} posted job {job_id}, reserved {payment_amount} tokens. Balance: {self.balance}")
                return job_id
            elif response.status_code == 402:
                logger.warning(f"Agent {self.agent_id} insufficient funds for job posting")
                return None
            else:
                logger.error(f"Agent {self.agent_id} job posting failed: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            logger.error(f"Agent {self.agent_id} job posting error: {e}")
            return None

    def get_balance(self) -> int:
        """Get current token balance."""
        return self.balance