import json
import os
import tempfile
import unittest

from models.pergunta import Pergunta
from services.quiz_service import QuizService


class FakePerguntaRepository:
    def __init__(self, perguntas):
        self._perguntas = perguntas

    def salvar(self, entidade):
        self._perguntas.append(entidade)

    def buscar_todos(self):
        return list(self._perguntas)

    def buscar_por_id(self, entidade_id):
        for pergunta in self._perguntas:
            if pergunta.id == entidade_id:
                return pergunta
        return None

    def excluir(self, entidade_id):
        self._perguntas = [p for p in self._perguntas if p.id != entidade_id]

    def atualizar(self, entidade):
        for index, pergunta in enumerate(self._perguntas):
            if pergunta.id == entidade.id:
                self._perguntas[index] = entidade
                return
        self._perguntas.append(entidade)

    def remover(self, entidade_id):
        self._perguntas = [pergunta for pergunta in self._perguntas if pergunta.id != entidade_id]

    def carregar_perguntas(self):
        return list(self._perguntas)


class QuizServiceTest(unittest.TestCase):
    def test_obter_categorias_retorna_categorias_unicas(self) -> None:
        perguntas = [
            Pergunta(id="p1", enunciado="Pergunta 1", opcoes=["a", "b"], resposta_correta="a", dificuldade="Fácil", pontuacao=10, categoria="Python"),
            Pergunta(id="p2", enunciado="Pergunta 2", opcoes=["a", "b"], resposta_correta="b", dificuldade="Fácil", pontuacao=10, categoria="Futebol"),
            Pergunta(id="p3", enunciado="Pergunta 3", opcoes=["a", "b"], resposta_correta="a", dificuldade="Fácil", pontuacao=10, categoria="Python"),
        ]
        service = QuizService(pergunta_repository=FakePerguntaRepository(perguntas))

        self.assertEqual(service.obter_categorias(), ["Python", "Futebol"])

    def test_obter_perguntas_por_categoria_filtra_por_tema(self) -> None:
        perguntas = [
            Pergunta(id="p1", enunciado="Pergunta 1", opcoes=["a", "b"], resposta_correta="a", dificuldade="Fácil", pontuacao=10, categoria="Python"),
            Pergunta(id="p2", enunciado="Pergunta 2", opcoes=["a", "b"], resposta_correta="b", dificuldade="Fácil", pontuacao=10, categoria="Futebol"),
        ]
        service = QuizService(pergunta_repository=FakePerguntaRepository(perguntas))

        perguntas_filtradas = service.obter_perguntas_por_categoria("Futebol")

        self.assertEqual([pergunta.id for pergunta in perguntas_filtradas], ["p2"])

    def test_criar_pergunta_salva_no_repositorio(self) -> None:
        repository = FakePerguntaRepository([])
        service = QuizService(pergunta_repository=repository)

        nova_pergunta = service.criar_pergunta(
            id="p100",
            enunciado="Nova pergunta",
            opcoes=["a", "b"],
            resposta_correta="1",
            dificuldade="Médio",
            pontuacao=15,
            categoria="Python",
        )

        self.assertEqual(nova_pergunta.enunciado, "Nova pergunta")
        self.assertEqual(repository.buscar_todos()[0].id, "p100")

    def test_criar_categoria_salva_no_arquivo(self) -> None:
        with tempfile.TemporaryDirectory() as diretorio:
            caminho = os.path.join(diretorio, "categorias.json")
            service = QuizService(pergunta_repository=FakePerguntaRepository([]), caminho_categorias=caminho)

            categoria = service.criar_categoria("Futebol")

            self.assertEqual(categoria, "Futebol")
            with open(caminho, "r", encoding="utf-8") as handle:
                self.assertEqual(json.load(handle), ["Futebol"])

    def test_listar_perguntas_retorna_todas_as_perguntas(self) -> None:
        perguntas = [
            Pergunta(id="p1", enunciado="Pergunta 1", opcoes=["a", "b"], resposta_correta="a", dificuldade="Fácil", pontuacao=10, categoria="Python"),
            Pergunta(id="p2", enunciado="Pergunta 2", opcoes=["a", "b"], resposta_correta="b", dificuldade="Médio", pontuacao=15, categoria="Lógica"),
        ]
        service = QuizService(pergunta_repository=FakePerguntaRepository(perguntas))

        self.assertEqual([pergunta.id for pergunta in service.listar_perguntas()], ["p1", "p2"])

    def test_editar_pergunta_altera_dados_existentes(self) -> None:
        perguntas = [
            Pergunta(id="p1", enunciado="Pergunta 1", opcoes=["a", "b"], resposta_correta="a", dificuldade="Fácil", pontuacao=10, categoria="Python"),
        ]
        repository = FakePerguntaRepository(perguntas)
        service = QuizService(pergunta_repository=repository)

        pergunta_editada = service.editar_pergunta(
            id="p1",
            enunciado="Pergunta atualizada",
            opcoes=["x", "y"],
            resposta_correta="2",
            dificuldade="Difícil",
            pontuacao=20,
            categoria="Futebol",
        )

        self.assertEqual(pergunta_editada.enunciado, "Pergunta atualizada")
        self.assertEqual(repository.buscar_todos()[0].categoria, "Futebol")

    def test_excluir_pergunta_remove_da_lista(self) -> None:
        perguntas = [
            Pergunta(id="p1", enunciado="Pergunta 1", opcoes=["a", "b"], resposta_correta="a", dificuldade="Fácil", pontuacao=10, categoria="Python"),
            Pergunta(id="p2", enunciado="Pergunta 2", opcoes=["a", "b"], resposta_correta="b", dificuldade="Médio", pontuacao=15, categoria="Lógica"),
        ]
        repository = FakePerguntaRepository(perguntas)
        service = QuizService(pergunta_repository=repository)

        service.excluir_pergunta("p1")

        self.assertEqual([pergunta.id for pergunta in repository.buscar_todos()], ["p2"])


if __name__ == "__main__":
    unittest.main()
