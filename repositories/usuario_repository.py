from __future__ import annotations

import json
import os
from typing import List

from interfaces.repository_interface import UsuarioRepositoryInterface
from models.usuario import Usuario
from utils.constantes import ARQUIVO_USUARIOS, DIRETORIO_DADOS
from utils.logger import Logger


class UsuarioRepository(UsuarioRepositoryInterface):
    def __init__(self, caminho: str | None = None, logger: Logger | None = None) -> None:
        self.caminho = caminho or os.path.join(DIRETORIO_DADOS, ARQUIVO_USUARIOS)
        self.logger = logger or Logger()

    def salvar(self, entidade: Usuario) -> None:
        usuarios = self.buscar_todos()
        usuarios.append(entidade)
        self._salvar_arquivo(usuarios)
        self.logger.info(f"Usuário {entidade.email} salvo")

    def buscar_todos(self) -> List[Usuario]:
        if not os.path.exists(self.caminho):
            return []

        with open(self.caminho, "r", encoding="utf-8") as handle:
            conteudo = json.load(handle)

        return [Usuario(**item) for item in conteudo]

    def buscar_por_id(self, entidade_id: str) -> Usuario | None:
        chave = entidade_id.strip().lower()
        usuarios = self.buscar_todos()
        for usuario in usuarios:
            if usuario.email.strip().lower() == chave:
                return usuario
        return None

    def excluir(self, entidade_id: str) -> None:
        usuarios = [u for u in self.buscar_todos() if u.email != entidade_id]
        self._salvar_arquivo(usuarios)
        self.logger.info(f"Usuário {entidade_id} excluído")

    def autenticar(self, email: str, senha: str) -> bool:
        usuario = self.buscar_por_email(email)
        if usuario is None:
            return False
        autenticado = usuario.verificar_senha(senha)
        self.logger.info(f"Tentativa de login para {email}: {'sucesso' if autenticado else 'falha'}")
        return autenticado

    def buscar_por_email(self, email: str) -> Usuario | None:
        return self.buscar_por_id(email)

    def _salvar_arquivo(self, usuarios: List[Usuario]) -> None:
        os.makedirs(os.path.dirname(self.caminho), exist_ok=True)
        with open(self.caminho, "w", encoding="utf-8") as handle:
            json.dump([u.__dict__ for u in usuarios], handle, ensure_ascii=False, indent=4)
