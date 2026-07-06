import os
import tempfile
import unittest

from models.usuario import Usuario
from repositories.usuario_repository import UsuarioRepository


class UsuarioRepositoryTest(unittest.TestCase):
    def test_login_deve_aceitar_email_com_mistas_caixas_e_espacos(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            caminho = os.path.join(tmpdir, "usuarios.json")
            repository = UsuarioRepository(caminho=caminho)

            usuario = Usuario(
                nome="Edmilson",
                email="edmilson.vieira@sistemafiep.org.br",
                senha="Rc123",
            )
            repository.salvar(usuario)

            encontrado = repository.buscar_por_email("  Edmilson.Vieira@Sistemafiep.Org.Br  ")
            self.assertIsNotNone(encontrado)
            self.assertTrue(repository.autenticar("  Edmilson.Vieira@Sistemafiep.Org.Br  ", "Rc123"))


if __name__ == "__main__":
    unittest.main()
