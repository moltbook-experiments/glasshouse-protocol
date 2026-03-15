#!/usr/bin/env python3
"""
UAT Runner for Glasshouse Protocol Agent Simulation.

This script runs automated User Acceptance Tests for the agent simulation system.
It can be integrated with CI/CD pipelines for automated testing.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add the simulation directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from config import config
from logger import setup_logging
from simulation_runner import SimulationRunner
from uat_scenarios import UATScenarios

async def run_uat_scenarios():
    """Run all UAT scenarios."""
    print("Starting UAT scenarios...")

    scenarios_runner = UATScenarios()

    # Run each UAT scenario
    scenario_methods = [
        ('buyer_financial_portfolio', scenarios_runner.run_financial_portfolio_optimization_uat),
        ('new_seller_trust_building', scenarios_runner.run_new_seller_trust_building_uat),
        ('enterprise_production_ai', scenarios_runner.run_enterprise_production_ai_uat),
        ('freelance_quality_competition', scenarios_runner.run_freelance_quality_competition_uat),
        ('researcher_scientific_reproducibility', scenarios_runner.run_researcher_reproducibility_uat)
    ]

    results = {}
    for scenario_name, scenario_method in scenario_methods:
        print(f"Running scenario: {scenario_name}")
        try:
            result = await scenario_method()
            # Scenario methods return boolean, convert to expected format
            results[scenario_name] = {'success': result}
            print(f"Scenario {scenario_name}: {'PASSED' if result else 'FAILED'}")
        except Exception as e:
            print(f"Scenario {scenario_name}: ERROR - {e}")
            results[scenario_name] = {'success': False, 'error': str(e)}

    return results

def main():
    """Main entry point for UAT runner."""
    # Setup logging
    setup_logging()

    # Run scenarios
    try:
        results = asyncio.run(run_uat_scenarios())

        # Summary
        total = len(results)
        passed = sum(1 for r in results.values() if r.get('success', False))

        print(f"\nUAT Results: {passed}/{total} scenarios passed")

        if passed == total:
            print("All UAT scenarios passed!")
            return 0
        else:
            print("Some UAT scenarios failed.")
            return 1

    except Exception as e:
        print(f"UAT runner failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())