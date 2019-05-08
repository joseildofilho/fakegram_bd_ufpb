from build_database import Tables
from gerente_perfil import GerentePerfil
from cli import Interface

tabelas = Tables()
gerente_perfil = GerentePerfil()
cli = Interface(gerente_perfil)

def start():    
    print('Starting program')
    print("building tables")
#    tabelas.drop_database()
    print('populando banco')
#    tabelas.build()
    #gerente_perfil.fill()
    print("stating CLI")
    cli.start()

