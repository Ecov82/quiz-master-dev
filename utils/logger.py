from __future__ import annotations

import datetime
import os
from typing import Any


class Logger:
    """Logger simples para registrar eventos operacionais do sistema."""

    def __init__(self, arquivo: str = "app.log") -> None:
        self.arquivo = arquivo
        self._criar_arquivo_se_nao_existir()

    def _criar_arquivo_se_nao_existir(self) -> None:
        if not os.path.exists(self.arquivo):
            with open(self.arquivo, "w", encoding="utf-8") as _:  # noqa: WPS421
                pass

    def registrar(self, mensagem: str, nivel: str = "INFO") -> None:
        registro = f"[{datetime.datetime.now().isoformat()}] [{nivel}] {mensagem}\n"
        with open(self.arquivo, "a", encoding="utf-8") as handle:
            handle.write(registro)

    def info(self, mensagem: str) -> None:
        self.registrar(mensagem, "INFO")

    def erro(self, mensagem: str) -> None:
        self.registrar(mensagem, "ERROR")
