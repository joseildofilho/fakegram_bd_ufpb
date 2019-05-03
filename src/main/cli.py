import os

DIV_SIZE = 10

class Interface:

    div = lambda _: print("#" * DIV_SIZE)

    def __init__(self, gerente, fill=False):
        self.gerente = gerente
        if fill:
            self.gerente.fill()

    def start(self):
        while True:
            print("starating")
            fechar = self.login()
            if fechar == 'fechar':
                break
            self.menu()

        
    def clear(self):
        os.system('clear')

    def login(self):
        logged = False
        while not logged:
            self.div()
            print("""
                    1 - Login
                    2 - Cadastrar Perfil
                    3 - Fechar App
                    """)
            resposta = self.get_input(3)
            self.clear()

            if resposta == 1:
                resposta = self.fazer_login()
                if resposta:
                    logged = True
            elif resposta == 2:
                logged = self.cadastrar_usuario()
            elif resposta == 3:
                logged = True
                resposta = "fechar"
        return resposta

    def fazer_login(self):
        self.div()

        print("""
                1 - nome_usuario
                2 - senha
                """)
        login = input("Login: ")
        senha = input("Senha: ")

        self.clear()

        return self.gerente.logar(login, senha)

    def cadastrar_usuario(self):
        nome = input("Nome Perfil: ")
        while not self.gerente._validar_nome_perfil(nome):
            print("nome de perfil invalido ")
            nome = input("Nome Perfil: ")
        senha = input("Senha: ")
        self.gerente.cadastrar_perfil([nome, "", senha, "", False])

    def get_input(self, rang):
        resposta = 0
        while not resposta:
            try:
                resposta = int(input("Digite um numero para esolher sua opção: "))
                if resposta not in [i + 1 for i in range(rang)]:
                    resposta = 0
                    print("Resposta Invalida")
            except Exception:
                print("Resposta Invalida")
        return resposta

    def menu(self):
        resposta = 0
        while resposta != 10:
            print("""
                1 - Ver seu perfil
                2 - Ver suas postagens
                3 - Ver seus seguidores
                4 - Ver seus seguidos
                5 - Linha do tempo
                6 - Directs
                7 - Notificações
                8 - Bloqueios
                9 - Busca
                10 - Sair
            """)
            resposta = self.get_input(10)

            if resposta == 1:
                self.ver_perfil()
            elif resposta == 2:
                pass
            elif resposta == 3:
                pass
            elif resposta == 4:
                pass
            elif resposta == 5:
                pass
            elif resposta == 6:
                pass
            elif resposta == 7:
                pass
            elif resposta == 8:
                pass
            elif resposta == 9:
                pass

    def ver_perfil(self):
        np, bio, _, n, p = self.gerente.perfil_atual
        print("""
                Nome Perfil: {}
                Biografia: {}
                Nome: {}
                Privacidade: {}

                Enter - voltar
                """.format(np, bio, n, p)) 
        input()
