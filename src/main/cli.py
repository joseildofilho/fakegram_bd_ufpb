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
                1 - Login
                2 - Cadastrar Perfil
                3 - Fechar App
                """)
        resposta = self.get_input(3)
        self.clear()

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

