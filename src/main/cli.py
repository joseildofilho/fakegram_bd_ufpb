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
            (usuario, senha) = self.login()
        
    def clear(self):
        os.system('clear')

    def login(self):
        self.div()
        print("""
                0 - Login
                1 - Cadastrar Perfil
                2 - Fechar App
                """)
        resposta = self.get_input()
        self.div()

    def get_input(self):
        resposta = -1
        try:
            resposta = int(input("Digite um numero para esolher sua opção: "))
        except Exception:
            print("Resposta Invalida")
        return resposta

