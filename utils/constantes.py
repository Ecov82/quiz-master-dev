from __future__ import annotations

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DIRETORIO_DADOS = str(BASE_DIR / "data")
ARQUIVO_PERGUNTAS = "perguntas.json"
ARQUIVO_USUARIOS = "usuarios.json"
ARQUIVO_RANKING = "ranking.txt"
NIVEIS_DIFICULDADE = ["Fácil", "Médio", "Difícil"]
MEDALHAS = {
    "ouro": "🏆 Ouro",
    "prata": "🥈 Prata",
    "bronze": "🥉 Bronze",
}
TEMPO_POR_PERGUNTA_SEGUNDOS = 20
