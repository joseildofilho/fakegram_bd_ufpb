from faker import Faker
import random

faker = Faker()

def insert(table, fields, values, connection):
    vs = []
    for i,v in enumerate(values):
        if type(v) == bool:
            v = str(v)
        elif v.isnumeric():
            v = str(v)
        else:
            v = "'" + v + "'"
        vs.append(v)

    aux = "INSERT INTO " + table + " ( " + ",".join(fields) + " ) VALUES ( " + ",".join(vs) + " );" 

    connection.cursor(
            lambda cursor: cursor.execute(aux)
            )

def select_profile(nome, connection):
    nom = "'" + nome + "'"
    aux = "SELECT * FROM perfil WHERE nome_perfil = {} LIMIT 1;".format(nom)

    def f_aux(cursor):
        cursor.execute(aux)
        return cursor.fetchone()
    return connection.cursor(f_aux)

def create_fake_profile():
    nome_perfil = faker.name()
    biografia   = faker.text()
    senha       = faker.credit_card_number()
    nome_real   = nome_perfil
    privacidade = True if random.random() > 0.5 else False
    return [nome_perfil, biografia, senha, nome_real, privacidade]


