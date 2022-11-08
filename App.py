from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
import mysql.connector
import json

app= Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATION']=True
app.config['SQLALCHEMY_DATABASE_URI']='mysql://@localhost/agenda'
db=SQLAlchemy(app)

class Contatos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    email = db.Column(db.String(50))
    telefone = db.Column(db.Integer(10))
    empresa = db.Column(db.String(100))

def to_json(self):
    return {"id": self.id, "nome": self.nome, "email": self.email, "empresa": self.empresa}


def gera_response(status, nome_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_conteudo] = conteudo

    if (mensagem):
        body["mensagem"] = mensagem

        return Response(json.dumps(body), status=status, mimetype="application/json")

@app.route("/contatos", methods=["GET"])
def seleciona_contato():
 contatos_classe = Contatos.query.all()
 contatos_json = [contatos.to_json () for contatos in contatos_classe]

 return gera_response(200, "contatos", contatos_json)
#

@app.route("/contatos/<id>", methods=["GET"])
def seleciona_contato(id):
    contatos_classe = Contatos.query.filte_by(id=id).first()
    contatos_json = contatos_classe.to_json()

    return gera_response(200, "contatos", contatos_json)

@app.route("/contatos", methods=["POST"])
def cria_contato():
    body = request.get_json()

    try:
        contatos = Contatos(nome=body["nome"], email=body["email"], empresa=body["empresa"])
        db.session.add(contatos)
        db.session.commit()
        return gera_response(201, "contatos", contatos.to_json(), "Criado com Sucesso!")
    except Exception as e:
        print(e)
    return gera_response(400, "contatos", {}, "Erro ao cadastrar!")


@app.route("/contatos/<id>", methods=["PUT"])
def atualiza_contato(id):
    contatos_classe = Contatos.query.filte_by(id=id).first()
    body = request.get_json()
    
    try:
            if('nome' in body):
             contatos_classe.nome = body["nome"]
            if ('email' in body):
             contatos_classe.email = body["email"]
            if('empresa' in body):
             contatos_classe.empresa = body["empresa"]

            db.session.add(contatos_classe)
            db.session.commit()
            return gera_response(200, "contatos", contatos_classe.to_json(), "Atualizado com Sucesso!")
    except Exception as e:
     print(e)
    return gera_response(400, "contatos", {}, "Erro ao atualizar!")


@app.route("/contatos/<id>", methods=["DELETE"])
def deleta_contatos(id):   
    contatos_classe = Contatos.query.filte_by(id=id).first()

    try:
        db.session.delete(contatos_classe)
        db.session.commit()
        return gera_response(200, "contatos", contatos_classe.to_json(), "Deletadp com Sucesso!")
    except Exception as e:
        print(e)
    return gera_response(400, "contatos", {}, "Erro ao deletar!")

app.run()



