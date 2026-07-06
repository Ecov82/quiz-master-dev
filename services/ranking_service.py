from __future__ import annotations

from typing import List

from interfaces.service_interface import ServiceInterface
from models.ranking import Ranking
from repositories.ranking_repository import RankingRepository
from utils.logger import Logger


class RankingService(ServiceInterface):
    def __init__(self, repository: RankingRepository | None = None, logger: Logger | None = None) -> None:
        self.repository = repository or RankingRepository()
        self.logger = logger or Logger()

    def iniciar(self) -> None:
        self.logger.info("Ranking service iniciado")

    def executar(self, *args: object, **kwargs: object) -> object:
        raise NotImplementedError("Operação genérica não suportada")

    def salvar_partida(self, ranking: Ranking) -> None:
        self.repository.salvar_partida(ranking)
        self.logger.info(f"Ranking salvo para jogador {ranking.jogador}")

    def obter_top_10(self) -> List[Ranking]:
        return self.repository.carregar_top_10()
