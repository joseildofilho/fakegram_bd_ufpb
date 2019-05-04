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
                    4 - Login Aleatorio
                    """)
            resposta = self.get_input(4)
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
            elif resposta == 4:
                self.gerente.set_perfil(self.gerente.seleciona_perfil_aleatorio()[0])
                logged = True
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
                self.ver_minhas_postagens()
            elif resposta == 3:
                self.ver_seguidores()
            elif resposta == 4:
                self.ver_seguidos()
            elif resposta == 5:
                self.linha_do_tempo()
            elif resposta == 6:
                pass
            elif resposta == 7:
                pass
            elif resposta == 8:
                pass
            elif resposta == 9:
                pass
    def linha_do_tempo(self):
        linha = self.gerente.montar_linha_do_tempo()
        self.div()
        if not linha:
            print("""
                    Não temos nada para te mostrar, aparentemente seus seguidos são muito quietos.
                    """)
            self.div()
        stride_sair = 1
        quant = len(linha) + stride_sair
        resposta = 0
        while resposta != stride_sair:
            print("""
                    1 - Voltar
                    """.format("2 .. {} Escolher um post".format(quant if linha else "")))
            for post in linha:
                print("""
                    [Autor]: {}
                    [Foto] : {}
                    [Texto]: {}
                    """.format(post[0], post[1], post[2]))

            resposta = self.get_input(quant)
            
            if resposta == stride_sair:
                return
            else:
                self.clear()
                self.ver_post(linha[resposta - stride_sair - 1])

    def ver_post(self, post):
        while resposta != 2:
            self.div()
            print("""

                [Autor]: {}
                [Foto] : {}
                [Texto]: {}

            """.format(post[0], post[1], post[2]))
            print("""

                    1 - comentar
                    2 - voltar

                    """)
            comentarios = self.gerente.get_comentarios(post[3])
            if not comentarios:
                print("""

                    Não há comentarios neste post, faça um.

                """)
            for comentario in comentarios:
                print("""

                        [Autor]: {}
                        [Comentario]: {}

                    """)
            self.div()
            resposta = self.get_input(2)
            if resposta == 1:
                self.clear()
                print("""

                    [Autor]: {}
                    [Foto] : {}
                    [Texto]: {}

                """.format(post[0], post[1], post[2]))
                self.comentar(post[4])
            self.clear()
    
    def comentar(self, id):
        resposta = input("[Comentario]: ")
        self.gerente.comentar(resposta, id)

    def ver_seguidos(self):
        seguidos = self.gerente.get_seguidos()
        if not seguidos:
            self.div()
            print("""
                        Você não gosta de ninguem ? por que não busca alguem e o segue :p
                        Enter - Voltar
                    """)
            self.div()
            input()
            self.clear()
            return
        self.div()
        print("\n*** Lista de Seguidos ***")
        for seguido in seguidos:
            print("""
                {}
            """.format(seguido))
        print("Enter - Voltar")
        self.div()   
        input()
        self.clear()
            
    def ver_seguidores(self):
        seguidores = self.gerente.get_seguidores()
        if not seguidores:
            self.div()
            print("""
                    Você é um cara muito sozinho e ninguem segue-te D:
                    Enter - Voltar
                    """)
            self.div()
            input()
            self.clear()
            return
        print("\n***Lista de seguidores***")
        for seguidor in seguidores:
            self.div()
            print("""
                {}
            """.format(seguidor))
        print("Enter para Voltar")
        self.div()
        input()
        self.clear()
        
    def ver_minhas_postagens(self):
        resposta = 0
        while resposta != 2:
            posts = self.gerente.get_posts_atual()
            print("""
                        1 - Postar
                        2 - Voltar
                    """)
            if not posts:
                self.div()
                print("""
                        Você não tem posts atualmente
                        """)
            for post in posts:
                self.div()
                print("""
                        [IMAGEM]: {}
                        [TEXTO]: {}
                        """.format(post[1], post[0]))
            resposta = self.get_input(2)
            if resposta == 1:
                self.postar()
            self.clear()

    def postar(self):
        foto = input("Digite o caminho da foto: ")
        texto = input("[Texto]: ")
        self.gerente.postar(texto, foto)

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
        self.clear()
