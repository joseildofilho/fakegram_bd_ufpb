def insert(table, fields, values, connection):
    aux = "INSERT INTO " + table + " ( " + ",".join(fields) + " ) VALUES ( " + ",".join(values) + " );" 

    connection.cursor(
            lambda cursor: cursor.execute(aux)
            )
