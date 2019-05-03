from build_database import Tables
from gerente_perfil import GerentePerfil
from cli import Interface

tabelas = Tables()
gerente_perfil = GerentePerfil()
cli = Interface(gerente_perfil)

def start():    
    tabelas.drop_database()
    print('Starting program')
    print("building tables")
    tabelas.build()
    print('populando banco')
    gerente_perfil.fill()
    print("stating CLI")
    cli.start()

    tabelas.drop_database()
