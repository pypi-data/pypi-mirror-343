import logging

from brainminer.brain import SessionManager

class AlphaMiner:

    def __init__(self, session_manager: SessionManager):
        self._session_manager = session_manager

    def mine_alphas(self, region="USA", universe="TOP3000"):
        logging.info(f"Starting alpha mining for region: {region}, universe: {universe}")
        pass