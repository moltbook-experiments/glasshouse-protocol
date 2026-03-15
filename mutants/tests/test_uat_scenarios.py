"""
Test runner for UAT scenarios.
Executes all user story-based scenarios and reports results.
"""

import asyncio
import logging
import sys
import os
from pathlib import Path

# Add the uat_simulation directory to the path
sys.path.insert(0, str(Path(__file__).parent / 'uat_simulation'))

from uat_scenarios import UATScenarios
from config import config
from logger import setup_logging

async def run_all_uat_scenarios():
    """Run all UAT scenarios and report results."""

    # Setup logging
    setup_logging()

    logger = logging.getLogger(__name__)

    # Initialize UAT scenarios
    uat = UATScenarios(config)

    # Define scenarios to run
    scenarios = [
        ('Financial Portfolio Optimization', uat.run_financial_portfolio_optimization_uat),
        ('New Seller Trust Building', uat.run_new_seller_trust_building_uat),
        ('Enterprise Production AI', uat.run_enterprise_production_ai_uat),
        ('Freelance Quality Competition', uat.run_freelance_quality_competition_uat),
        ('Researcher Reproducibility', uat.run_researcher_reproducibility_uat),
    ]

    results = {}

    print("🧪 Starting UAT Scenario Testing")
    print("=" * 50)

    for scenario_name, scenario_func in scenarios:
        print(f"\n🔄 Running: {scenario_name}")
        print("-" * 40)

        try:
            success = await scenario_func()
            results[scenario_name] = success

            if success:
                print(f"✅ {scenario_name}: PASSED")
            else:
                print(f"❌ {scenario_name}: FAILED")

        except Exception as e:
            logger.error(f"Scenario {scenario_name} failed with exception: {e}")
            results[scenario_name] = False
            print(f"💥 {scenario_name}: ERROR - {e}")

    # Summary
    print("\n" + "=" * 50)
    print("📊 UAT Test Results Summary")
    print("=" * 50)

    total_scenarios = len(scenarios)
    passed_scenarios = sum(1 for result in results.values() if result)
    failed_scenarios = total_scenarios - passed_scenarios

    print(f"Total Scenarios: {total_scenarios}")
    print(f"Passed: {passed_scenarios}")
    print(f"Failed: {failed_scenarios}")
    print(".1f")

    if failed_scenarios == 0:
        print("🎉 All UAT scenarios passed!")
        return True
    else:
        print("⚠️  Some UAT scenarios failed. Check logs for details.")
        return False

async def run_single_scenario(scenario_name: str):
    """Run a single UAT scenario by name."""

    config = load_config()
    setup_logging(config)

    uat = UATScenarios(config)

    scenario_map = {
        'financial': uat.run_financial_portfolio_optimization_uat,
        'trust': uat.run_new_seller_trust_building_uat,
        'enterprise': uat.run_enterprise_production_ai_uat,
        'quality': uat.run_freelance_quality_competition_uat,
        'reproducibility': uat.run_researcher_reproducibility_uat,
    }

    if scenario_name not in scenario_map:
        print(f"Unknown scenario: {scenario_name}")
        print("Available scenarios: financial, trust, enterprise, quality, reproducibility")
        return False

    print(f"🔄 Running single scenario: {scenario_name}")
    success = await scenario_map[scenario_name]()

    if success:
        print(f"✅ {scenario_name}: PASSED")
    else:
        print(f"❌ {scenario_name}: FAILED")

    return success

if __name__ == "__main__":
    if len(sys.argv) > 1:
        scenario_name = sys.argv[1]
        success = asyncio.run(run_single_scenario(scenario_name))
    else:
        success = asyncio.run(run_all_uat_scenarios())

    sys.exit(0 if success else 1)