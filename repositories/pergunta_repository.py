from __future__ import annotations

import json
import os
from typing import List

from interfaces.repository_interface import PerguntaRepositoryInterface
from models.pergunta import Pergunta
from utils.constantes import ARQUIVO_PERGUNTAS, DIRETORIO_DADOS
from utils.logger import Logger


class PerguntaRepository(PerguntaRepositoryInterface):
    def __init__(self, caminho: str | None = None, logger: Logger | None = None) -> None:
        self.caminho = caminho or os.path.join(DIRETORIO_DADOS, ARQUIVO_PERGUNTAS)
        self.logger = logger or Logger()

    def salvar(self, entidade: Pergunta) -> None:
        self.logger.info(f"Salvando pergunta {entidade.id}")
        perguntas = self.carregar_perguntas()
        perguntas.append(entidade)
        self._salvar_arquivo(perguntas)

    def atualizar(self, entidade: Pergunta) -> None:
        perguntas = self.carregar_perguntas()
        for index, pergunta in enumerate(perguntas):
            if pergunta.id == entidade.id:
                perguntas[index] = entidade
                self._salvar_arquivo(perguntas)
                self.logger.info(f"Pergunta atualizada {entidade.id}")
                return
        self.salvar(entidade)

    def remover(self, entidade_id: str) -> None:
        perguntas = [pergunta for pergunta in self.carregar_perguntas() if pergunta.id != entidade_id]
        self._salvar_arquivo(perguntas)
        self.logger.info(f"Pergunta removida {entidade_id}")

    def buscar_todos(self) -> List[Pergunta]:
        return self.carregar_perguntas()

    def buscar_por_id(self, entidade_id: str) -> Pergunta | None:
        perguntas = self.carregar_perguntas()
        for pergunta in perguntas:
            if pergunta.id == entidade_id:
                return pergunta
        return None

    def excluir(self, entidade_id: str) -> None:
        perguntas = [p for p in self.carregar_perguntas() if p.id != entidade_id]
        self._salvar_arquivo(perguntas)
        self.logger.info(f"Pergunta {entidade_id} excluída")

    def carregar_perguntas(self) -> List[Pergunta]:
        if not os.path.exists(self.caminho):
            self.logger.info("Arquivo de perguntas não encontrado, retornando lista vazia")
            return []

        with open(self.caminho, "r", encoding="utf-8") as handle:
            conteudo = json.load(handle)

        perguntas = [Pergunta(**item) for item in conteudo]
        self.logger.info(f"Carregadas {len(perguntas)} perguntas")
        return perguntas

    def _salvar_arquivo(self, perguntas: List[Pergunta]) -> None:
        os.makedirs(os.path.dirname(self.caminho), exist_ok=True)
        with open(self.caminho, "w", encoding="utf-8") as handle:
            json.dump([p.__dict__ for p in perguntas], handle, ensure_ascii=False, indent=4)
