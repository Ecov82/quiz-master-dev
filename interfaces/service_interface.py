from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class ServiceInterface(ABC):
    """Interface que define operações genéricas de serviços."""

    @abstractmethod
    def iniciar(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def executar(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError
