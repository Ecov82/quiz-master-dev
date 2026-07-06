import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from controllers.quiz_controller import QuizController
from models.jogador import Jogador
from models.pergunta import Pergunta


class QuizControllerTest(unittest.TestCase):
    def test_solicitar_dado_permite_tentar_novamente_ou_voltar(self) -> None:
        controller = QuizController()

        with patch("builtins.input", side_effect=["", "0"]):
            self.assertIsNone(controller.solicitar_dado("Nome: "))

        with patch("builtins.input", side_effect=["", "Edmilson"]):
            self.assertEqual(controller.solicitar_dado("Nome: "), "Edmilson")

    def test_jogar_deve_perguntar_se_quero_jogar_outra_partida_apos_resultado(self) -> None:
        controller = QuizController()
        controller.usuario_logado = "usuario@example.com"
        controller.quiz_service = Mock()
        controller.quiz_service.obter_dificuldades.return_value = ["Fácil"]
        controller.quiz_service.obter_categorias.return_value = ["Python"]
        controller.quiz_service.criar_jogador.return_value = Jogador(nome="Ana")
        controller.quiz_service.selecionar_perguntas_aleatorias.return_value = [
            Pergunta(
                id="p1",
                enunciado="Pergunta de teste",
                opcoes=["A", "B"],
                resposta_correta="A",
                dificuldade="Fácil",
                pontuacao=10,
                categoria="Python",
            )
        ]
        controller.quiz_service.verificar_resposta.return_value = True
        controller.quiz_service.criar_ranking.return_value = SimpleNamespace(
            acertos=1,
            erros=0,
            dificuldade="Fácil",
            tempo_total=1.2,
        )
        controller.exibir_resultado_partida = Mock()

        prompts = []

        def input_mock(prompt: str) -> str:
            prompts.append(prompt)
            respostas = iter(["Ana", "1", "1", "1", "0", "0"])
            return next(respostas)

        with patch("builtins.input", side_effect=input_mock):
            controller.jogar()

        self.assertTrue(any("Deseja jogar outra partida" in prompt for prompt in prompts))


if __name__ == "__main__":
    unittest.main()
