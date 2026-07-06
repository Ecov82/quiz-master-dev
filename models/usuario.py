from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Usuario:
    nome: str
    email: str
    senha: str

    def verificar_senha(self, senha: str) -> bool:
        return self.senha == senha
