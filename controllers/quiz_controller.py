from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Optional

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from models.jogador import Jogador
from services.quiz_service import QuizService
from services.ranking_service import RankingService
from services.usuario_service import UsuarioService
from utils.banner import gerar_banner


class QuizController:
    """Controlador principal que faz a ponte entre UI e serviços."""

    def __init__(self) -> None:
        self.usuario_service = UsuarioService()
        self.quiz_service = QuizService()
        self.ranking_service = RankingService()
        self.usuario_logado: Optional[str] = None

    def limpar_tela(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")

    def exibir_banner(self) -> None:
        print(gerar_banner())

    def exibir_menu_principal(self) -> None:
        print("\n1 - Jogar")
        print("2 - Ranking")
        print("3 - Histórico")
        print("4 - Usuários")
        print("5 - Configurações")
        print("6 - Sobre")
        print("7 - Adicionar nova pergunta")
        print("8 - Adicionar categoria")
        print("9 - Ver perguntas cadastradas")
        print("10 - Editar pergunta existente")
        print("11 - Excluir pergunta cadastrada")
        print("0 - Sair")

    def iniciar(self) -> None:
        self.usuario_service.iniciar()
        self.quiz_service.iniciar()
        self.ranking_service.iniciar()

        while True:
            self.limpar_tela()
            self.exibir_banner()
            self.exibir_menu_principal()
            opcao = input("\nEscolha uma opção: ")

            if opcao == "1":
                self.jogar()
            elif opcao == "2":
                self.exibir_ranking()
            elif opcao == "3":
                self.exibir_historico()
            elif opcao == "4":
                self.exibir_menu_usuarios()
            elif opcao == "5":
                self.exibir_configuracoes()
            elif opcao == "6":
                self.exibir_sobre()
            elif opcao == "7":
                self.adicionar_pergunta()
            elif opcao == "8":
                self.adicionar_categoria()
            elif opcao == "9":
                self.ver_perguntas()
            elif opcao == "10":
                self.editar_pergunta()
            elif opcao == "11":
                self.excluir_pergunta()
            elif opcao == "0":
                self.sair()
                break
            else:
                input("\nOpção inválida. Pressione ENTER para continuar...")

    def solicitar_dado(self, mensagem: str, permitir_vazio: bool = False) -> str | None:
        while True:
            valor = input(mensagem).strip()
            if valor == "0":
                return None
            if permitir_vazio or valor:
                return valor
            print("Valor inválido. Digite novamente ou pressione 0 para voltar.")

    def jogar(self) -> None:
        while True:
            self.limpar_tela()
            print("\n[MODO JOGO]")

            if self.usuario_logado is None:
                print("É necessário estar logado para jogar.")
                input("Pressione ENTER para continuar...")
                return

            nome = self.solicitar_dado("Digite o nome do jogador (0 para voltar): ")
            if nome is None:
                return

            jogador = self.quiz_service.criar_jogador(nome)
            dificuldade = self.selecionar_dificuldade()
            categoria = self.selecionar_categoria()
            perguntas = self.quiz_service.selecionar_perguntas_aleatorias(10, dificuldade, categoria)
            acertos = 0
            erros = 0
            tempo_total = 0.0
            vidas = jogador.vidas

            indice_pergunta = 0
            while indice_pergunta < len(perguntas):
                self.limpar_tela()
                print(f"\n[RODADA {indice_pergunta + 1}/{len(perguntas)}]")
                pergunta = perguntas[indice_pergunta]
                print("\nPergunta:")
                print(pergunta.enunciado)
                for indice, opcao in enumerate(pergunta.opcoes, start=1):
                    print(f"{indice}. {opcao}")

                resposta = input("Escolha a alternativa: ")
                acertou = self.quiz_service.verificar_resposta(pergunta, resposta)
                if acertou:
                    jogador.aplicar_pontuacao(pergunta.pontuacao)
                    acertos += 1
                else:
                    jogador.perder_vida()
                    erros += 1
                    vidas = jogador.vidas

                if vidas <= 0:
                    print("\nSuas vidas acabaram.")
                    break

                print(f"\nVocê respondeu a pergunta {indice_pergunta + 1} de {len(perguntas)}.")
                opcao_continua = input("Deseja continuar? (1 - Sim / 0 - Não): ").strip()
                if opcao_continua == "0":
                    print("\nPartida encerrada pelo jogador.")
                    break

                indice_pergunta += 1

            ranking = self.quiz_service.criar_ranking(jogador, dificuldade, acertos, erros, tempo_total)
            self.quiz_service.salvar_ranking(ranking)
            self.exibir_resultado_partida(jogador, ranking)

            continuar = input("Deseja jogar outra partida? (1 - Sim / 0 - Não): ").strip()
            if continuar != "1":
                return

    def selecionar_dificuldade(self) -> str:
        opcoes = self.quiz_service.obter_dificuldades()
        while True:
            self.limpar_tela()
            print("\n[SELEÇÃO DE DIFICULDADE]")
            for indice, nivel in enumerate(opcoes, start=1):
                print(f"{indice} - {nivel}")
            print("0 - Voltar")

            escolha = input("Escolha o nível de dificuldade: ").strip()
            if escolha == "0":
                return opcoes[0]
            if escolha.isdigit() and 1 <= int(escolha) <= len(opcoes):
                return opcoes[int(escolha) - 1]
            print("Opção inválida. Tente novamente.")

    def selecionar_categoria(self) -> str:
        categorias = self.quiz_service.obter_categorias()
        opcoes = ["Todas"] + categorias
        while True:
            self.limpar_tela()
            print("\n[SELEÇÃO DE CATEGORIA]")
            for indice, categoria in enumerate(opcoes, start=1):
                print(f"{indice} - {categoria}")
            print("0 - Voltar")

            escolha = input("Escolha uma categoria: ").strip()
            if escolha == "0":
                return "Todas"
            if escolha.isdigit() and 1 <= int(escolha) <= len(opcoes):
                return opcoes[int(escolha) - 1]
            print("Opção inválida. Tente novamente.")

    def exibir_resultado_partida(self, jogador: Jogador, ranking: 'Ranking') -> None:
        print("\n===== RESULTADO DA PARTIDA =====")
        print(f"Jogador: {jogador.nome}")
        print(f"Pontuação: {jogador.pontuacao}")
        print(f"Vidas restantes: {jogador.vidas}")
        print(f"Medalhas: {', '.join(jogador.medalhas)}")
        print(f"Acertos: {ranking.acertos}")
        print(f"Erros: {ranking.erros}")
        print(f"Dificuldade: {ranking.dificuldade}")
        print(f"Tempo total (estimado): {ranking.tempo_total:.2f}s")
        input("\nPressione ENTER para continuar...")

    def exibir_ranking(self) -> None:
        self.limpar_tela()
        print("\n[RANKING TOP 10]")
        top_10 = self.ranking_service.obter_top_10()
        if not top_10:
            print("Nenhum registro de ranking encontrado.")
        else:
            for indice, registro in enumerate(top_10, start=1):
                print(
                    f"{indice}. {registro.jogador} - {registro.pontuacao} pontos - "
                    f"{registro.medalhas} medalhas - {registro.dificuldade}"
                )
        input("\nPressione ENTER para continuar...")

    def exibir_historico(self) -> None:
        self.limpar_tela()
        print("\n[HISTÓRICO DE PARTIDAS]")
        usuario = self.usuario_service.obter_usuario_atual()
        if usuario is None:
            print("Faça login para ver o histórico de partidas.")
            input("Pressione ENTER para continuar...")
            return

        if not hasattr(usuario, 'historico_partidas') or not usuario.historico_partidas:
            print("Nenhum histórico encontrado para este usuário.")
        else:
            for indice, partida in enumerate(usuario.historico_partidas, start=1):
                print(
                    f"{indice}. Dificuldade: {partida['dificuldade']} | "
                    f"Pontuação: {partida['pontuacao']} | Medalha: {partida['medalha']}"
                )
        input("\nPressione ENTER para continuar...")

    def exibir_menu_usuarios(self) -> None:
        self.limpar_tela()
        print("\n[USUÁRIOS]")
        print("1 - Cadastrar usuário")
        print("2 - Login")
        print("3 - Logout")
        print("0 - Voltar")

        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            self.cadastrar_usuario()
        elif opcao == "2":
            self.login_usuario()
        elif opcao == "3":
            self.logout_usuario()

    def cadastrar_usuario(self) -> None:
        self.limpar_tela()
        print("\n[CADASTRO DE USUÁRIO]")
        nome = self.solicitar_dado("Nome (0 para voltar): ")
        if nome is None:
            input("\nPressione ENTER para continuar...")
            return
        email = self.solicitar_dado("Email (0 para voltar): ")
        if email is None:
            input("\nPressione ENTER para continuar...")
            return
        senha = self.solicitar_dado("Senha (0 para voltar): ", permitir_vazio=True)
        if senha is None:
            input("\nPressione ENTER para continuar...")
            return
        try:
            self.usuario_service.cadastrar_usuario(nome, email, senha)
            print("Usuário cadastrado com sucesso.")
        except ValueError as error:
            print(f"Erro: {error}")
        input("\nPressione ENTER para continuar...")

    def login_usuario(self) -> None:
        self.limpar_tela()
        print("\n[LOGIN]")
        email = self.solicitar_dado("Email (0 para voltar): ")
        if email is None:
            input("\nPressione ENTER para continuar...")
            return
        senha = self.solicitar_dado("Senha (0 para voltar): ", permitir_vazio=True)
        if senha is None:
            input("\nPressione ENTER para continuar...")
            return
        if self.usuario_service.login(email, senha):
            self.usuario_logado = email
            print("Login realizado com sucesso.")
        else:
            print("Credenciais inválidas.")
        input("\nPressione ENTER para continuar...")

    def logout_usuario(self) -> None:
        self.usuario_service.logout()
        self.usuario_logado = None
        print("Logout realizado com sucesso.")
        input("\nPressione ENTER para continuar...")

    def adicionar_pergunta(self) -> None:
        self.limpar_tela()
        print("\n[CADASTRO DE PERGUNTA]")
        pergunta_id = self.solicitar_dado("ID da pergunta (0 para voltar): ")
        if pergunta_id is None:
            input("\nPressione ENTER para continuar...")
            return
        enunciado = self.solicitar_dado("Enunciado da pergunta (0 para voltar): ")
        if enunciado is None:
            input("\nPressione ENTER para continuar...")
            return

        opcoes = []
        for indice in range(1, 5):
            opcao = self.solicitar_dado(f"Opção {indice} (0 para voltar): ")
            if opcao is None:
                input("\nPressione ENTER para continuar...")
                return
            opcoes.append(opcao)

        resposta_correta = self.solicitar_dado("Número da resposta correta (1 a 4) (0 para voltar): ")
        if resposta_correta is None:
            input("\nPressione ENTER para continuar...")
            return

        dificuldade = self.solicitar_dado("Dificuldade (Fácil/Médio/Difícil) (0 para voltar): ")
        if dificuldade is None:
            input("\nPressione ENTER para continuar...")
            return
        pontuacao = self.solicitar_dado("Pontuação (0 para voltar): ")
        if pontuacao is None:
            input("\nPressione ENTER para continuar...")
            return
        categoria = self.solicitar_dado("Categoria (0 para voltar): ")
        if categoria is None:
            input("\nPressione ENTER para continuar...")
            return

        try:
            self.quiz_service.criar_pergunta(
                id=pergunta_id,
                enunciado=enunciado,
                opcoes=opcoes,
                resposta_correta=resposta_correta,
                dificuldade=dificuldade,
                pontuacao=int(pontuacao),
                categoria=categoria,
            )
            print("Pergunta cadastrada com sucesso.")
        except ValueError as error:
            print(f"Erro: {error}")
        input("\nPressione ENTER para continuar...")

    def adicionar_categoria(self) -> None:
        self.limpar_tela()
        print("\n[CADASTRO DE CATEGORIA]")
        categoria = self.solicitar_dado("Nome da categoria (0 para voltar): ")
        if categoria is None:
            input("\nPressione ENTER para continuar...")
            return
        try:
            self.quiz_service.criar_categoria(categoria)
            print("Categoria cadastrada com sucesso.")
        except ValueError as error:
            print(f"Erro: {error}")
        input("\nPressione ENTER para continuar...")

    def ver_perguntas(self) -> None:
        self.limpar_tela()
        print("\n[PERGUNTAS CADASTRADAS]")
        perguntas = self.quiz_service.listar_perguntas()
        if not perguntas:
            print("Nenhuma pergunta cadastrada.")
        else:
            for pergunta in perguntas:
                print(f"- {pergunta.id} | {pergunta.enunciado} | Categoria: {pergunta.categoria} | Dificuldade: {pergunta.dificuldade}")
        input("\nPressione ENTER para continuar...")

    def editar_pergunta(self) -> None:
        self.limpar_tela()
        print("\n[EDIÇÃO DE PERGUNTA]")
        pergunta_id = self.solicitar_dado("ID da pergunta a editar (0 para voltar): ")
        if pergunta_id is None:
            input("\nPressione ENTER para continuar...")
            return

        perguntas = self.quiz_service.listar_perguntas()
        pergunta = next((item for item in perguntas if item.id == pergunta_id), None)
        if pergunta is None:
            print("Pergunta não encontrada.")
            input("\nPressione ENTER para continuar...")
            return

        enunciado = self.solicitar_dado(f"Novo enunciado [{pergunta.enunciado}] (0 para voltar): ")
        if enunciado is None:
            input("\nPressione ENTER para continuar...")
            return
        opcoes = []
        for indice in range(1, 5):
            opcao = self.solicitar_dado(f"Nova opção {indice} [{pergunta.opcoes[indice - 1]}] (0 para voltar): ")
            if opcao is None:
                input("\nPressione ENTER para continuar...")
                return
            opcoes.append(opcao)
        resposta_correta = self.solicitar_dado(f"Nova resposta correta [{pergunta.resposta_correta}] (0 para voltar): ")
        if resposta_correta is None:
            input("\nPressione ENTER para continuar...")
            return
        dificuldade = self.solicitar_dado(f"Nova dificuldade [{pergunta.dificuldade}] (0 para voltar): ")
        if dificuldade is None:
            input("\nPressione ENTER para continuar...")
            return
        pontuacao = self.solicitar_dado(f"Nova pontuação [{pergunta.pontuacao}] (0 para voltar): ")
        if pontuacao is None:
            input("\nPressione ENTER para continuar...")
            return
        categoria = self.solicitar_dado(f"Nova categoria [{pergunta.categoria}] (0 para voltar): ")
        if categoria is None:
            input("\nPressione ENTER para continuar...")
            return

        try:
            self.quiz_service.editar_pergunta(
                id=pergunta_id,
                enunciado=enunciado,
                opcoes=opcoes,
                resposta_correta=resposta_correta,
                dificuldade=dificuldade,
                pontuacao=int(pontuacao),
                categoria=categoria,
            )
            print("Pergunta editada com sucesso.")
        except ValueError as error:
            print(f"Erro: {error}")
        input("\nPressione ENTER para continuar...")

    def excluir_pergunta(self) -> None:
        self.limpar_tela()
        print("\n[EXCLUSÃO DE PERGUNTA]")
        pergunta_id = self.solicitar_dado("ID da pergunta a excluir (0 para voltar): ")
        if pergunta_id is None:
            input("\nPressione ENTER para continuar...")
            return
        try:
            self.quiz_service.excluir_pergunta(pergunta_id)
            print("Pergunta excluída com sucesso.")
        except ValueError as error:
            print(f"Erro: {error}")
        input("\nPressione ENTER para continuar...")

    def exibir_configuracoes(self) -> None:
        self.limpar_tela()
        print("\n[CONFIGURAÇÕES]")
        print("Configurações futuras para tempo de jogo, modo e integração com API.")
        input("\nPressione ENTER para continuar...")

    def exibir_sobre(self) -> None:
        self.limpar_tela()
        print("\n===== SOBRE =====")
        print("Quiz Master")
        print("Sistema desenvolvido em Python com arquitetura preparada para escalar.")
        print("Permite evolução futura para API REST, SQLite, Flask, FastAPI e front-end web.")
        input("\nPressione ENTER para continuar...")

    def sair(self) -> None:
        print("\nObrigado por utilizar o Quiz Master!")
