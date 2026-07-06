from __future__ import annotations

import time


class Cronometro:
    """Cronômetro simples com início, parada, reinício e tempo decorrido."""

    def __init__(self) -> None:
        self._inicio: float | None = None
        self._fim: float | None = None

    def iniciar(self) -> None:
        self._inicio = time.monotonic()
        self._fim = None

    def parar(self) -> None:
        if self._inicio is None:
            return
        self._fim = time.monotonic()

    def reiniciar(self) -> None:
        self._inicio = time.monotonic()
        self._fim = None

    def tempo_decorrido(self) -> float:
        if self._inicio is None:
            return 0.0
        if self._fim is not None:
            return self._fim - self._inicio
        return time.monotonic() - self._inicio
