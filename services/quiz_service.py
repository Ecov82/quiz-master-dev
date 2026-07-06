from __future__ import annotations

import json
import os
import random
from typing import List

from interfaces.service_interface import ServiceInterface
from models.jogador import Jogador
from models.pergunta import Pergunta
from models.ranking import Ranking
from repositories.pergunta_repository import PerguntaRepository
from repositories.ranking_repository import RankingRepository
from utils.constantes import MEDALHAS, NIVEIS_DIFICULDADE, TEMPO_POR_PERGUNTA_SEGUNDOS
from utils.cronometro import Cronometro
from utils.logger import Logger


class QuizService(ServiceInterface):
    """Service que concentra toda a regra de negócio do quiz."""

    def __init__(
        self,
        pergunta_repository: PerguntaRepository | None = None,
        ranking_repository: RankingRepository | None = None,
        logger: Logger | None = None,
        caminho_categorias: str | None = None,
    ) -> None:
        self.pergunta_repository = pergunta_repository or PerguntaRepository()
        self.ranking_repository = ranking_repository or RankingRepository()
        self.logger = logger or Logger()
        self.cronometro = Cronometro()
        self.caminho_categorias = caminho_categorias or os.path.join(os.path.dirname(__file__), "..", "data", "categorias.json")

    def iniciar(self) -> None:
        self.logger.info("Quiz service iniciado")

    def executar(self, *args: object, **kwargs: object) -> object:
        raise NotImplementedError("Operação genérica não suportada")

    def obter_dificuldades(self) -> List[str]:
        return NIVEIS_DIFICULDADE.copy()

    def obter_categorias(self) -> List[str]:
        categorias = self._carregar_categorias()
        for pergunta in self.pergunta_repository.carregar_perguntas():
            if pergunta.categoria not in categorias:
                categorias.append(pergunta.categoria)
        self.logger.info(f"Categorias disponíveis: {categorias}")
        return categorias

    def _carregar_categorias(self) -> List[str]:
        if not os.path.exists(self.caminho_categorias):
            return []
        with open(self.caminho_categorias, "r", encoding="utf-8") as handle:
            dados = json.load(handle)
        return dados if isinstance(dados, list) else []

    def _salvar_categorias(self, categorias: List[str]) -> None:
        os.makedirs(os.path.dirname(self.caminho_categorias), exist_ok=True)
        with open(self.caminho_categorias, "w", encoding="utf-8") as handle:
            json.dump(categorias, handle, ensure_ascii=False, indent=4)

    def criar_categoria(self, categoria: str) -> str:
        categoria_limpa = categoria.strip()
        if not categoria_limpa:
            raise ValueError("Categoria inválida")

        categorias = self._carregar_categorias()
        if categoria_limpa not in categorias:
            categorias.append(categoria_limpa)
            self._salvar_categorias(categorias)
        self.logger.info(f"Categoria criada: {categoria_limpa}")
        return categoria_limpa

    def obter_perguntas_por_dificuldade(self, dificuldade: str, categoria: str | None = None) -> List[Pergunta]:
        todas = self.pergunta_repository.carregar_perguntas()
        perguntas = [
            pergunta
            for pergunta in todas
            if pergunta.dificuldade == dificuldade and (categoria is None or categoria == "Todas" or pergunta.categoria == categoria)
        ]
        if len(perguntas) < 5:
            perguntas.extend(
                pergunta
                for pergunta in todas
                if pergunta.dificuldade == dificuldade and pergunta not in perguntas
            )
        self.logger.info(
            f"Carregado {len(perguntas)} perguntas para dificuldade {dificuldade} e categoria {categoria or 'todas'}"
        )
        return perguntas

    def obter_perguntas_por_categoria(self, categoria: str) -> List[Pergunta]:
        perguntas = [
            pergunta
            for pergunta in self.pergunta_repository.carregar_perguntas()
            if pergunta.categoria == categoria
        ]
        self.logger.info(f"Carregado {len(perguntas)} perguntas para categoria {categoria}")
        return perguntas

    def selecionar_perguntas_aleatorias(self, quantidade: int, dificuldade: str, categoria: str | None = None) -> List[Pergunta]:
        perguntas = self.obter_perguntas_por_dificuldade(dificuldade, categoria)
        quantidade = min(quantidade, len(perguntas))
        selecionadas = random.sample(perguntas, quantidade)
        self.logger.info(f"Selecionadas {len(selecionadas)} perguntas aleatórias")
        return selecionadas

    def listar_perguntas(self) -> List[Pergunta]:
        perguntas = self.pergunta_repository.carregar_perguntas()
        self.logger.info(f"Listadas {len(perguntas)} perguntas")
        return perguntas

    def editar_pergunta(
        self,
        id: str,
        enunciado: str,
        opcoes: List[str],
        resposta_correta: str,
        dificuldade: str,
        pontuacao: int,
        categoria: str = "Geral",
    ) -> Pergunta:
        perguntas = self.pergunta_repository.carregar_perguntas()
        for index, pergunta in enumerate(perguntas):
            if pergunta.id == id:
                pergunta_editada = Pergunta(
                    id=pergunta.id,
                    enunciado=enunciado,
                    opcoes=opcoes,
                    resposta_correta=resposta_correta,
                    dificuldade=dificuldade,
                    pontuacao=pontuacao,
                    categoria=categoria,
                )
                self.pergunta_repository.atualizar(pergunta_editada)
                self.logger.info(f"Pergunta editada: {id}")
                return pergunta_editada
        raise ValueError("Pergunta não encontrada")

    def excluir_pergunta(self, id: str) -> None:
        perguntas = self.pergunta_repository.carregar_perguntas()
        if not any(pergunta.id == id for pergunta in perguntas):
            raise ValueError("Pergunta não encontrada")
        self.pergunta_repository.remover(id)
        self.logger.info(f"Pergunta removida: {id}")

    def verificar_resposta(self, pergunta: Pergunta, resposta: str) -> bool:
        acertou = pergunta.verificar_resposta(resposta)
        self.logger.info(
            f"Resposta para pergunta {pergunta.id}: {'correta' if acertou else 'incorreta'}"
        )
        return acertou

    def calcular_medalha(self, pontuacao: int) -> str:
        if pontuacao >= 80:
            return MEDALHAS["ouro"]
        if pontuacao >= 50:
            return MEDALHAS["prata"]
        return MEDALHAS["bronze"]

    def criar_pergunta(
        self,
        id: str,
        enunciado: str,
        opcoes: List[str],
        resposta_correta: str,
        dificuldade: str,
        pontuacao: int,
        categoria: str = "Geral",
    ) -> Pergunta:
        pergunta = Pergunta(
            id=id,
            enunciado=enunciado,
            opcoes=opcoes,
            resposta_correta=resposta_correta,
            dificuldade=dificuldade,
            pontuacao=pontuacao,
            categoria=categoria,
        )
        self.pergunta_repository.salvar(pergunta)
        self.logger.info(f"Pergunta criada: {pergunta.id}")
        return pergunta

    def criar_ranking(
        self,
        jogador: Jogador,
        dificuldade: str,
        acertos: int,
        erros: int,
        tempo_total: float,
    ) -> Ranking:
        medalha = self.calcular_medalha(jogador.pontuacao)
        jogador.adicionar_medalha(medalha)

        ranking = Ranking(
            jogador=jogador.nome,
            pontuacao=jogador.pontuacao,
            medalhas=len(jogador.medalhas),
            dificuldade=dificuldade,
            tempo_total=tempo_total,
            acertos=acertos,
            erros=erros,
        )
        self.logger.info(f"Ranking criado para jogador {jogador.nome}")
        return ranking

    def salvar_ranking(self, ranking: Ranking) -> None:
        self.ranking_repository.salvar_partida(ranking)
        self.logger.info(f"Ranking salvo para jogador {ranking.jogador}")

    def criar_jogador(self, nome: str) -> Jogador:
        jogador = Jogador(nome=nome)
        self.logger.info(f"Jogador criado: {nome}")
        return jogador

    def tempo_por_pergunta(self) -> int:
        return TEMPO_POR_PERGUNTA_SEGUNDOS
