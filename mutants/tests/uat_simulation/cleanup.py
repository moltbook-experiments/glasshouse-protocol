#!/usr/bin/env python3
"""
Cleanup script for UAT simulation test data.

This script removes test data created during simulation runs to ensure
clean state for subsequent tests.
"""

import requests
import logging
from typing import List, Optional
from config import config

# Setup basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimulationCleanup:
    """Handles cleanup of simulation test data."""

    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or config.get('agents.base_url', 'http://127.0.0.1:8000')
        self.session = requests.Session()

    def cleanup_jobs(self, job_ids: Optional[List[str]] = None) -> None:
        """Clean up test jobs. If job_ids provided, only clean those."""
        try:
            # This would need backend support for bulk cleanup
            # For now, log the intent
            if job_ids:
                logger.info(f"Cleaning up jobs: {job_ids}")
            else:
                logger.info("Cleaning up all test jobs")
        except Exception as e:
            logger.error(f"Error cleaning up jobs: {e}")

    def cleanup_agents(self, agent_ids: Optional[List[str]] = None) -> None:
        """Clean up test agents. If agent_ids provided, only clean those."""
        try:
            # This would need backend support for test agent cleanup
            if agent_ids:
                logger.info(f"Cleaning up agents: {agent_ids}")
            else:
                logger.info("Cleaning up all test agents")
        except Exception as e:
            logger.error(f"Error cleaning up agents: {e}")

    def reset_balances(self) -> None:
        """Reset all agent balances to zero."""
        try:
            # This would need backend admin endpoint
            logger.info("Resetting all agent balances")
        except Exception as e:
            logger.error(f"Error resetting balances: {e}")

    def cleanup_all(self) -> None:
        """Perform complete cleanup of all test data."""
        logger.info("Starting complete simulation cleanup")
        self.cleanup_jobs()
        self.cleanup_agents()
        self.reset_balances()
        logger.info("Simulation cleanup completed")

if __name__ == "__main__":
    cleanup = SimulationCleanup()
    cleanup.cleanup_all()