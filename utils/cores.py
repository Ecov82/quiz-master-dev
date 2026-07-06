from __future__ import annotations


class Cores:
    RESET = "\033[0m"
    VERMELHO = "\033[31m"
    VERDE = "\033[32m"
    AMARELO = "\033[33m"
    AZUL = "\033[34m"
    NEGRITO = "\033[1m"

    @classmethod
    def aplicar(cls, texto: str, cor: str) -> str:
        return f"{cor}{texto}{cls.RESET}"
