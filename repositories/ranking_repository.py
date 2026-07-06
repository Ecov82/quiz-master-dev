from __future__ import annotations

import os
from typing import List

from interfaces.repository_interface import RankingRepositoryInterface
from models.ranking import Ranking
from utils.constantes import ARQUIVO_RANKING, DIRETORIO_DADOS
from utils.logger import Logger


class RankingRepository(RankingRepositoryInterface):
    def __init__(self, caminho: str | None = None, logger: Logger | None = None) -> None:
        self.caminho = caminho or os.path.join(DIRETORIO_DADOS, ARQUIVO_RANKING)
        self.logger = logger or Logger()

    def salvar(self, entidade: Ranking) -> None:
        self.salvar_partida(entidade)

    def buscar_todos(self) -> List[Ranking]:
        if not os.path.exists(self.caminho):
            return []

        registros: List[Ranking] = []
        with open(self.caminho, "r", encoding="utf-8") as handle:
            for linha in handle:
                linha = linha.strip()
                if not linha:
                    continue
                partes = linha.split(";")
                if len(partes) != 6:
                    continue
                jogador, pontuacao, medalhas, dificuldade, tempo_total, acertos_erros = partes
                acertos, erros = map(int, acertos_erros.split(","))
                registros.append(
                    Ranking(
                        jogador=jogador,
                        pontuacao=int(pontuacao),
                        medalhas=int(medalhas),
                        dificuldade=dificuldade,
                        tempo_total=float(tempo_total),
                        acertos=acertos,
                        erros=erros,
                    )
                )
        self.logger.info(f"Carregados {len(registros)} registros de ranking")
        return registros

    def buscar_por_id(self, entidade_id: str) -> Ranking | None:
        for registro in self.buscar_todos():
            if registro.jogador == entidade_id:
                return registro
        return None

    def excluir(self, entidade_id: str) -> None:
        registros = [r for r in self.buscar_todos() if r.jogador != entidade_id]
        self._salvar_arquivo(registros)
        self.logger.info(f"Ranking de {entidade_id} excluído")

    def carregar_top_10(self) -> List[Ranking]:
        rankings = sorted(self.buscar_todos(), key=lambda item: item.pontuacao, reverse=True)
        return rankings[:10]

    def salvar_partida(self, ranking: Ranking) -> None:
        os.makedirs(os.path.dirname(self.caminho), exist_ok=True)
        with open(self.caminho, "a", encoding="utf-8") as handle:
            handle.write(
                f"{ranking.jogador};{ranking.pontuacao};{ranking.medalhas};{ranking.dificuldade};"
                f"{ranking.tempo_total:.2f};{ranking.acertos},{ranking.erros}\n"
            )
        self.logger.info(f"Partida salva para jogador {ranking.jogador}")

    def _salvar_arquivo(self, registros: List[Ranking]) -> None:
        os.makedirs(os.path.dirname(self.caminho), exist_ok=True)
        with open(self.caminho, "w", encoding="utf-8") as handle:
            for ranking in registros:
                handle.write(
                    f"{ranking.jogador};{ranking.pontuacao};{ranking.medalhas};{ranking.dificuldade};"
                    f"{ranking.tempo_total:.2f};{ranking.acertos},{ranking.erros}\n"
                )
