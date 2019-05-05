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
                self.conversas()
            elif resposta == 7:
                self.notificacoes()
            elif resposta == 8:
                self.bloqueios()
            elif resposta == 9:
                self.buscar()

    def buscar(self):
        resposta = 0
        while resposta != 3:
            self.clear()
            self.div()
            print("""

                        1 - Buscar por nome de perfil, nome real, ou biografia.
                        2 - Buscar topico
                        3 - Voltar

                    """)
            self.div()
            resposta = self.get_input(3)
            if resposta == 1:
                self.buscar_perfil()
            elif resposta == 2:
                self.buscar_topico()
            self.clear()

    def buscar_perfil(self):
        self.clear()
        resposta = input("digite o nome do perfil: ")
        perfis = self.gerente.buscar_perfil(resposta)
        if not perfis:
            print("""
                        Não encontramos nenhum perfil
                        Enter - Voltar
                    """)
            input()
            return

        reposta = 0
        while reposta != 1:
            print("""
                    1 - voltar
                    [2 - N] para visitar perfil
                """)
            for index, perfil in enumerate(perfis):
                print("""
                        [{}] - Nome: {} 
                        """.format(index + 2, perfil[0]))
            resposta = self.get_input(len(perfil) + 1)
            if resposta == 1:
                break
            else:
                self.ver_perfil_busca(perfis[resposta - 2])
            self.clear()

    def ver_perfil_busca(self, perfil):
        if self.gerente.sou_seguidor(perfil[0]):
            perfil_show = """
                    
                    ########################
                    
                    ELE TE SEGUE

                    #######################

                    Nome Perfil: {}
                    Biografia: {}
                    Nome: {}
                    1 - Voltar
                    [2 - N] Post
            """.format(perfil[0], perfil[1], perfil[3])
            print(perfil_show)
            posts = self.gerente.get_posts(perfil[0])
            if not posts:
                print("""
                        Não há posts para mostrar
                        """)
            for index, post in enumerate(posts):
                print("""
                    [{}] - Numero
                       [Autor]: {}
                       [Foto]: {}
                       [Texto]: {} 
                       [Data]: {}
                        """.format(index + 2, post[0], post[-1], post[1], post[2]))
                print(post)
            resposta = self.get_input(len(posts) + 1)
            if resposta == 1:
                self.clear()
                return
            else:
                post = posts[resposta - 2]
                post = [post[4], post[5], post[1], post[0]]
                self.ver_post(post)
        else:
            if perfil[-1]:
                print("""
                        Perfil: {}
                        Você não pode ver este perfil, ele é privado.
                        1 - Pedir para seguir
                        2 - Voltar
                        """.format(perfil[0]))
                resposta = self.get_input(2)
                if resposta == 1:
                    self.gerente.seguir(perfil[0])
            else:
                perfil_show = """
                        Nome Perfil: {}
                        Biografia: {}
                        Nome: {}
                        1 - Pedir para seguir
                        2 - Voltar
                """.format(perfil[0], perfil[1], perfil[3])
                print(perfil_show)
                posts = self.gerente.get_posts(perfil[0])
                if not posts:
                    print("""
                            Não há posts para mostrar
                            """)
                for post in posts:
                    print(post)
                resposta = self.get_input(2)
                if resposta == 1:
                    self.gerente.seguir(perfil[0])
                

    def buscar_topico(self):
        self.clear()

        topic = input("Digite o topico desejado: ")
        topicos = self.gerente.buscar_topico(topic)

        if not topicos:
            print("""
                    *** NÃO HÁ TOPICOS COM ESTE NOME ***
                    """)
        for topico in topicos:
            print("""
                        '{}' criados em '{}'
                    """.format(topico[0], topico[1]))
        print("Enter - Voltar")
        input()
        self.clear()

    def bloqueios(self):
        self.clear()
        resposta = 0
        while resposta != 3:
            bloqueados = self.gerente.get_bloqueados()
            self.div()
            print("""
                        1 - Bloquear
                        2 - Desbloquear
                        3 - Voltar
                    """)
            if not bloqueados:
                print("""
                            Você não bloqueou ninguem.
                        """)
            else:
                print("""
                            *** Bloqueados ***
                """)
            for bloqueado in bloqueados:
                print("""
                            {}
                        """.format(bloqueado[1]))
            resposta = self.get_input(3)
            if resposta == 1:
                resposta = input("Quem você gostaria de bloquear: ")
                self.gerente.bloquear(resposta)
            elif resposta == 2:
                resposta = input("Quem você gostaria de desbloquear: ")
                self.gerente.desbloquear(resposta)

    def notificacoes(self):
        self.clear()
        notificacoes = self.gerente.ver_notificacoes()
        if not notificacoes:
            print("""
                        Não há notificações
                        Enter - Voltar
                    """)
            input()
            return
        for notificacao in notificacoes:
            print(notificacao)
            msg = """
                    [Perfil]: {}
                    [Ação]  : {}
                    [Data]  : {}
                    {}
                    """
            aux = ""
            if notificacao[-1] != 0:
                aux = "[Mensagem]: {}"
                aux = aux.format(self.gerente.get_mensagem(notificacao[-1])[1])
            msg = msg.format(notificacao[5], notificacao[4],notificacao[2], aux)
            print(msg)
            if notificacao[4] == 'seguir_pedido':
                resposta = input("Você aceita está pessoa como seu seguidor ?(Y/N)")
                if resposta.lower() == "y":
                    self.gerente.confimar_pedido_seguir(notificacao[5])
                    resposta = input("Você aceita seguir esta pessoa ?(Y/N)")
                    if resposta.lower() == 'y':
                        self.gerente.seguir(notificacao[5])
        
            
    def conversas(self):
        while True:
            conversas = self.gerente.ver_directs()

            for conversa in conversas:
                print("""
                        ({})=>({}):
                            {}
                            {}
                        """.format(conversa[1],conversa[2],conversa[3],conversa[4]))

            quem = input("[Digite o nome do usuario ou Enter para sair]: ")
            if not quem:
                return
            if not self.gerente.is_conversa_nova(quem):
                self.mandar_direct(quem)
            else:
                if self.gerente.is_publico(quem) or self.gerente.sou_seguido(quem):
                    self.mandar_direct(quem)
                else:
                    print("O perfil não é publico ou voce não é seguido por")


    def mandar_direct(self,quem):
        resposta = input("[Texto]: ")
        self.gerente.mandar_direct(resposta, quem)
        self.clear()

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
                    """.format(post[0], post[2], post[1]))

            resposta = self.get_input(quant)
            
            if resposta == stride_sair:
                return
            else:
                self.clear()
                self.ver_post(linha[resposta - stride_sair - 1])

    def ver_post(self, post):
        resposta = 0
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
                    3 - Deletar post
                    [4 - N para deletar comentarios [Apenas os seus]]

                    """)
            comentarios = self.gerente.get_comentarios(post[3])
            if not comentarios:
                print("""

                    Não há comentarios neste post, faça um.

                """)
            for index, comentario in enumerate(comentarios):
                print("""
                    [{}] - Numero
                        [Autor]: {}
                        [Comentario]: {}

                    """.format(index + 4, comentario[3], comentario[2]))
            self.div()
            resposta = self.get_input(4 + len(comentarios))
            if resposta == 1:
                self.clear()
                print("""

                    [Autor]: {}
                    [Foto] : {}
                    [Texto]: {}

                """.format(post[0], post[1], post[2]))
                self.comentar(post[3])
            elif resposta == 2:
                return
            elif resposta == 3:
                self.gerente.remove_post(post[3])
                return
            else:
                if self.gerente.perfil_atual[0] == comentarios[resposta - 4][3] or post[0] == self.gerente.perfil_atual[0]:
                    self.gerente.remove_comentario(comentarios[resposta - 4][0])
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
                        [3 - N] - Entrar no post
                    """)
            if not posts:
                self.div()
                print("""
                        Você não tem posts atualmente
                        """)
            for index, post in enumerate(posts):
                self.div()
                print("""
                    [{}] - Numero
                        [IMAGEM]: {}
                        [TEXTO]: {}
                        """.format(index + 3,post[5], post[1]))
            resposta = self.get_input(3 + len(posts))
            if resposta == 1:
                self.postar()
            elif resposta == 2:
                return
            else:
                post = posts[resposta - 3]
                post = [post[4], post[5], post[1], post[0]]
                self.ver_post(post)
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

                1 - Voltar
                2 - Editar perfil
                """.format(np, bio, n, p))
        resposta = self.get_input(2)
        if resposta == 1:
            return
        elif resposta == 2:
            self.editar_perfil()
        self.clear()

    def editar_perfil(self):
        self.clear()
        perfil = self.gerente.perfil_atual
        self.div()
        print("""
            Aperte Enter caso não deseje alterar a informação atual
            Ps.: O nome do perfil não pode ser alterado
        """)
        biografia = input("Biografia, Atual [{}]: ".format(perfil[1]))
        biografia = biografia if biografia else perfil[1]

        senha = input("Senha, Atual [{}]: ".format(perfil[2]))
        senha = senha if senha else perfil[2]

        nome_real = input("Nome Real, Atual [{}]: ".format(perfil[3]))
        nome_real = nome_real if nome_real else perfil[3]

        privacidade = input("Privacidade, Atual [{}]: ".format(perfil[4]))
        privacidade = privacidade if privacidade else perfil[4]

        perfil = [perfil[0], biografia, senha, nome_real, privacidade]

        self.gerente.alterar_perfil(perfil)

        self.gerente.set_perfil(perfil[0])

        self.clear()



