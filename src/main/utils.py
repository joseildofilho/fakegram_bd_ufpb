from faker import Faker
import random

faker = Faker()

def normalize(l):
    vs = []
    for i,v in enumerate(l):
        if type(v) == bool:
            v = str(v)
        elif v.isnumeric():
            v = str(v)
        else:
            v = "'" + v + "'"
        vs.append(v)
    return vs

def insert(table, fields, values, connection):

    vs = normalize(values)

    aux = "INSERT INTO " + table + " ( " + ",".join(fields) + " ) VALUES ( " + ",".join(vs) + " );" 

    connection.cursor(
            lambda cursor: cursor.execute(aux)
            )

def alter(table, column, fields, values, connection):

    vs = normalize(values)

    query = "UPDATE {} SET".format(table)
    for field, value in zip(fields, vs):
        query += " " + field + " = " + value + ","
    query = query[:-1] + " WHERE {} = {};".format(column.split(":")[0], column.split(":")[1])

    connection.cursor(lambda cursor: cursor.execute(query))

def remove(table, column, id, connection):
    query = "DELETE FROM {} WHERE {}='{}';".format(table, column, id)
    connection.cursor(lambda cursor: cursor.execute(query))    

def select_profile(nome, connection):
    nom = "'" + nome + "'"
    aux = "SELECT * FROM perfil WHERE nome_perfil = {} LIMIT 1;".format(nom)

    def f_aux(cursor):
        cursor.execute(aux)
        return cursor.fetchone()
    return connection.cursor(f_aux)

def create_fake_profile():
    nomes = faker.profile("username")
    nome_perfil = nomes['username']
    biografia   = faker.text()
    senha       = faker.credit_card_number()
    nome_real   = nomes['name']
    privacidade = True if random.random() > 0.5 else False
    return [nome_perfil, biografia, senha, nome_real, privacidade]


