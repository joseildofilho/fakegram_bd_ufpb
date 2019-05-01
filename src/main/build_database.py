from H2Connector import H2Connector as connector
class Tables:
    
    def build(self):
        self.connection.cursor(self._create_tables)

    def _create_tables(self, cursor):
        for key, table in self.tables.items():
            #print("creating table", key)
            cursor.execute(table)
    
    def drop_database(self):
        for key in self.tables.keys():
            #print("deleting", key)
            self.connection.cursor(
                    lambda cursor: cursor.execute("DROP TABLE IF EXISTS {}".format(key))
                    )
    def __init__(self):
        self.connection = connector()

    tables = {
    'perfil' : """
            CREATE TABLE perfil(
                nome_perfil VARCHAR(50) NOT NULL PRIMARY KEY,
                biografia VARCHAR(1000) ,
                senha VARCHAR(50) NOT NULL,
                nome_real VARCHAR(50) NOT NULL,
                privacidade BOOLEAN NOT NULL
            );
        """,
        'segue' : """
            CREATE TABLE segue(
                nome_seguidor VARCHAR(50) NOT NULL REFERENCES perfil(nome_perfil),
                nome_seguido VARCHAR(50) NOT NULL REFERENCES perfil(nome_perfil),
                PRIMARY KEY (nome_seguidor, nome_seguido)
            );
        """,
        
        'bloqueia' : """
            CREATE TABLE bloqueia(
                nome_bloqueador VARCHAR(50) NOT NULL REFERENCES perfil(nome_perfil),
                nome_bloqueado VARCHAR(50) NOT NULL REFERENCES perfil(nome_perfil),
                PRIMARY KEY (nome_bloqueador, nome_bloqueado)
            );
        """,
        
        'conversa' : """
            CREATE TABLE conversa(
                id BIGINT NOT NULL AUTO_INCREMENT,
                nome_remetente VARCHAR(50) NOT NULL REFERENCES perfil(nome_perfil),
                nome_destinatario VARCHAR(50) NOT NULL REFERENCES perfil(nome_perfil),
                msg VARCHAR(255) NOT NULL,
                data datetime NOT NULL,
                PRIMARY KEY (id,nome_remetente,nome_destinatario)
            );
        """,
        
        'mensagem' : """ 
            CREATE TABLE mensagem(
              id BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
              texto VARCHAR(500) NOT NULL,
              data datetime NOT NULL,
              nome_criador VARCHAR(50) NOT NULL REFERENCES perfil(nome_perfil) /*RELACIONAMENTO TEM*/
            );
        """,
        
        'marcado_perfil' : """
            CREATE TABLE marcado_perfil(
              nome_marcado VARCHAR(50) NOT NULL REFERENCES perfil(nome_perfil),
              id_mensagem BIGINT NOT NULL REFERENCES mensagem(id),
              PRIMARY KEY (nome_marcado, id_mensagem)
            );
        """,
            
            #ESPECIALIZAÇÂO#
        'post' : """
            CREATE TABLE post(
              foto VARCHAR(100),
              id_mensagem BIGINT NOT NULL REFERENCES mensagem(id),
              PRIMARY KEY (id_mensagem)
            );
        """,
            
            #ESPECIALIZAÇÂO#
        'comentario' : """
            CREATE TABLE comentario(
              id_mensagem BIGINT NOT NULL REFERENCES mensagem(id),
              id_post BIGINT NOT NULL REFERENCES post(id_mensagem),
              PRIMARY KEY (id_mensagem)
            );
        """,
        'marcado_topico' : """
            CREATE TABLE marcado_topico(
              id_mensagem BIGINT NOT NULL REFERENCES mensagem(id),
              nome_topico VARCHAR(25) NOT NULL,               /*ENTIDADE TOPICO*/
              PRIMARY KEY (id_mensagem)
            );
        """,
        'notificacao' : """
            CREATE TABLE notificacao(
              id_notificacao BIGINT NOT NULL AUTO_INCREMENT,
              nome_notificado VARCHAR(50) NOT NULL REFERENCES perfil(nome_perfil), /*RELACIONAMENTO ENCHE O SACO*/
              data datetime NOT NULL,
              vista BOOLEAN NOT NULL,
              tipo VARCHAR(20) NOT NULL,
              nome_notificador VARCHAR(50) REFERENCES perfil(nome_perfil), /*NOTIFICADO POR PERFIL*/
              id_mensagem BIGINT  REFERENCES mensagem(id),      /*NOTIFICADO POR MENSAGEM*/
              PRIMARY KEY (id_notificacao)
            );
        """,    
        'visualiza' : """    
            CREATE TABLE visualiza(
              id_notificacao BIGINT NOT NULL REFERENCES notificacao(id_notificacao),
              nome_notificado VARCHAR(50) NOT NULL REFERENCES perfil(nome_perfil),
              PRIMARY KEY (id_notificacao,nome_notificado)
            );
        """
    }
