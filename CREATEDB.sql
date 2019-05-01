DROP TABLE IF EXISTS perfil;
CREATE TABLE perfil(
nome_perfil VARCHAR(50) NOT NULL PRIMARY KEY,
biografia VARCHAR(255) NOT NULL,
senha VARCHAR(50) NOT NULL,
nome_real VARCHAR(50) NOT NULL,
privacidade BOOLEAN NOT NULL
);

DROP TABLE IF EXISTS segue;
CREATE TABLE segue(
  nome_seguidor VARCHAR(50) NOT NULL REFERENCES perfil(nome_perfil),
  nome_seguido VARCHAR(50) NOT NULL REFERENCES perfil(nome_perfil),
  PRIMARY KEY (nome_seguidor, nome_seguido)
);

DROP TABLE IF EXISTS bloqueia;
CREATE TABLE bloqueia(
  nome_bloqueador VARCHAR(50) NOT NULL REFERENCES perfil(nome_perfil),
  nome_bloqueado VARCHAR(50) NOT NULL REFERENCES perfil(nome_perfil),
  PRIMARY KEY (nome_bloqueador, nome_bloqueado)
);

DROP TABLE IF EXISTS conversa;
CREATE TABLE conversa(
  id BIGINT NOT NULL AUTO_INCREMENT,
  nome_remetente VARCHAR(50) NOT NULL REFERENCES perfil(nome_perfil),
  nome_destinatario VARCHAR(50) NOT NULL REFERENCES perfil(nome_perfil),
  msg VARCHAR(255) NOT NULL,
  data datetime NOT NULL,
  PRIMARY KEY (id,nome_remetente,nome_destinatario)
);

DROP TABLE IF EXISTS mensagem;
CREATE TABLE mensagem(
  id BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
  texto VARCHAR(500) NOT NULL,
  data datetime NOT NULL,
  nome_criador VARCHAR(50) NOT NULL REFERENCES perfil(nome_perfil) /*RELACIONAMENTO TEM*/
);

DROP TABLE IF EXISTS marcado_perfil;
CREATE TABLE marcado_perfil(
  nome_marcado VARCHAR(50) NOT NULL REFERENCES perfil(nome_perfil),
  id_mensagem BIGINT NOT NULL REFERENCES mensagem(id),
  PRIMARY KEY (nome_marcado, id_mensagem)
);

DROP TABLE IF EXISTS post;      /*ESPECIALIZAÇÂO ################################*/
CREATE TABLE post(
  foto VARCHAR(100),
  id_mensagem BIGINT NOT NULL REFERENCES mensagem(id),
  PRIMARY KEY (id_mensagem)
);

DROP TABLE IF EXISTS comentario;     /*ESPECIALIZAÇÂO #################################*/
CREATE TABLE comentario(
  id_mensagem BIGINT NOT NULL REFERENCES mensagem(id),
  id_post BIGINT NOT NULL REFERENCES post(id_mensagem),
  PRIMARY KEY (id_mensagem)
);

DROP TABLE IF EXISTS marcado_topico;
CREATE TABLE marcado_topico(
  id_mensagem BIGINT NOT NULL REFERENCES mensagem(id),
  nome_topico VARCHAR(25) NOT NULL,               /*ENTIDADE TOPICO*/
  PRIMARY KEY (id_mensagem)
);

DROP TABLE IF EXISTS notificacao;
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



DROP TABLE IF EXISTS visualiza;
CREATE TABLE visualiza(
  id_notificacao BIGINT NOT NULL REFERENCES notificacao(id_notificacao),
  nome_notificado VARCHAR(50) NOT NULL REFERENCES perfil(nome_perfil),
  PRIMARY KEY (id_notificacao,nome_notificado)
);
