from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class Jogador:
    nome: str
    vidas: int = 3
    pontuacao: int = 0
    medalhas: List[str] = field(default_factory=list)
    historico_partidas: List[dict] = field(default_factory=list)

    def aplicar_pontuacao(self, pontos: int) -> None:
        self.pontuacao += pontos

    def perder_vida(self) -> None:
        self.vidas = max(0, self.vidas - 1)

    def adicionar_medalha(self, medalha: str) -> None:
        if medalha not in self.medalhas:
            self.medalhas.append(medalha)

    def registrar_partida(self, partida: dict) -> None:
        self.historico_partidas.append(partida)
