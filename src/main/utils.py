def insert(table, fields, values, connection):
    aux = "INSERT INTO " + table + " ( " + ",".join(fields) + " ) VALUES ( " + ",".join(values) + " )" 

    print("Trying to excute:\n", aux)

    connection.cursor(
            lambda cursor: cursor.execute(aux)
            )
