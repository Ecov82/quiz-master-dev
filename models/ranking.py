from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Ranking:
    jogador: str
    pontuacao: int
    medalhas: int
    dificuldade: str
    tempo_total: float
    acertos: int
    erros: int

    def __post_init__(self) -> None:
        if self.pontuacao < 0:
            self.pontuacao = 0
        if self.tempo_total < 0:
            self.tempo_total = 0.0
