from __future__ import annotations

from typing import Optional

from interfaces.service_interface import ServiceInterface
from models.usuario import Usuario
from repositories.usuario_repository import UsuarioRepository
from utils.logger import Logger


class UsuarioService(ServiceInterface):
    def __init__(self, repository: UsuarioRepository | None = None, logger: Logger | None = None) -> None:
        self.repository = repository or UsuarioRepository()
        self.logger = logger or Logger()
        self.usuario_atual: Optional[Usuario] = None

    def iniciar(self) -> None:
        self.logger.info("Usuário service iniciado")

    def executar(self, *args: object, **kwargs: object) -> None:
        raise NotImplementedError("Operação genérica não suportada")

    def cadastrar_usuario(self, nome: str, email: str, senha: str) -> None:
        usuario_existente = self.repository.buscar_por_email(email)
        if usuario_existente is not None:
            raise ValueError("Já existe um usuário cadastrado com esse email.")

        usuario = Usuario(nome=nome, email=email, senha=senha)
        self.repository.salvar(usuario)
        self.logger.info(f"Novo usuário cadastrado: {email}")

    def login(self, email: str, senha: str) -> bool:
        autenticado = self.repository.autenticar(email, senha)
        if autenticado:
            self.usuario_atual = self.repository.buscar_por_email(email)
            self.logger.info(f"Login bem-sucedido: {email}")
            return True

        self.logger.info(f"Falha no login: {email}")
        return False

    def logout(self) -> None:
        if self.usuario_atual is not None:
            self.logger.info(f"Logout do usuário {self.usuario_atual.email}")
        self.usuario_atual = None

    def obter_usuario_atual(self) -> Optional[Usuario]:
        return self.usuario_atual
