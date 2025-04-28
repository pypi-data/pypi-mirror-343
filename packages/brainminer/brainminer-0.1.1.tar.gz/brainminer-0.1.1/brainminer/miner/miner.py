import logging

from brainminer.brain import SessionManager, WorldQuantBrain, SimulatorSettings, PerformanceFilter, \
    AlphaSimulationResult
from typing import List

class AlphaMiner:

    def __init__(self, session_manager: SessionManager):
        self._brain = WorldQuantBrain(session_manager)

    def mine_alphas(self, alpha_list: List[str], settings: SimulatorSettings, perf_filter: PerformanceFilter) -> List[AlphaSimulationResult]:
        logging.info(f"Starting alpha mining, size: {len(alpha_list)}")
        alpha_results = self._brain.execute_multi_simulation(expression_list=alpha_list, settings=settings)
        logging.info(f"Alpha mining completed, size: {len(alpha_results)}")
        match_results = []
        for alpha_result in alpha_results:
            if alpha_result.success and alpha_result.alpha_data is not None and alpha_result.alpha_data.is_match(perf_filter):
                match_results.append(alpha_result)
        return match_results