from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Iterable


class RepositoryInterface(ABC):
    """Interface que define operações genéricas de persistência."""

    @abstractmethod
    def salvar(self, entidade: Any) -> None:
        raise NotImplementedError

    @abstractmethod
    def buscar_todos(self) -> Iterable[Any]:
        raise NotImplementedError

    @abstractmethod
    def buscar_por_id(self, entidade_id: str) -> Any:
        raise NotImplementedError

    @abstractmethod
    def excluir(self, entidade_id: str) -> None:
        raise NotImplementedError


class RankingRepositoryInterface(RepositoryInterface, ABC):
    @abstractmethod
    def carregar_top_10(self) -> list[Any]:
        raise NotImplementedError

    @abstractmethod
    def salvar_partida(self, ranking: Any) -> None:
        raise NotImplementedError


class PerguntaRepositoryInterface(RepositoryInterface, ABC):
    @abstractmethod
    def carregar_perguntas(self) -> list[Any]:
        raise NotImplementedError

    @abstractmethod
    def atualizar(self, entidade: Any) -> None:
        raise NotImplementedError

    @abstractmethod
    def remover(self, entidade_id: str) -> None:
        raise NotImplementedError


class UsuarioRepositoryInterface(RepositoryInterface, ABC):
    @abstractmethod
    def autenticar(self, email: str, senha: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def buscar_por_email(self, email: str) -> Any:
        raise NotImplementedError
