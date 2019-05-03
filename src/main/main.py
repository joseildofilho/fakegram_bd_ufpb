from build_database import Tables
from gerente_perfil import GerentePerfil
from cli import Interface

tabelas = Tables()
gerente_perfil = GerentePerfil()
cli = Interface(gerente_perfil, True)

def start():    

    tabelas.drop_database()
    print('Starting program')
    print("building tables")
    tabelas.build()
    print("stating CLI")
    cli.start()

    tabelas.drop_database()
