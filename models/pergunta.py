from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class Pergunta:
    id: str
    enunciado: str
    opcoes: List[str]
    resposta_correta: str
    dificuldade: str
    pontuacao: int
    categoria: str = "Geral"

    def verificar_resposta(self, resposta: str) -> bool:
        return resposta.strip().lower() == self.resposta_correta.strip().lower()
