# pip install Flask-SQLAlchemy
# pip install pymysql
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import math

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/pais'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:senai%40123@localhost/reciclagem'


db = SQLAlchemy(app)

class Pais(db.Model):
    __tablename__ = 'pais'

    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(80), nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    populacao = db.Column(db.Integer, nullable=False)
    pib = db.Column(db.Float, nullable=False)
    totalLixo = db.Column(db.Float, nullable=False)
    totalReciclado = db.Column(db.Float, nullable=False)

    def __init__(self, nome, ano, populacao, pib, totalLixo, totalReciclado):
        self.nome = nome
        self.ano = ano
        self.populacao = populacao
        self.pib = pib
        self.totalLixo = totalLixo
        self.totalReciclado = totalReciclado

with app.app_context():
    db.create_all()  

@app.route("/listar")
def listar():
    # Configurações de paginação
    ITEMS_PER_PAGE = 10
    page = request.args.get('page', 1, type=int)  # Página atual (padrão: 1)
    
    # Consulta total de itens
    total_items = Pais.query.count()
    total_pages = math.ceil(total_items / ITEMS_PER_PAGE)
    
    # Consulta para obter apenas os itens da página atual
    paises = (Pais.query
            .order_by(Pais.nome)  # Ordenação opcional
              .offset((page - 1) * ITEMS_PER_PAGE)
            .limit(ITEMS_PER_PAGE)
            .all())

    return render_template("listar.html", paises=paises, page=page, total_pages=total_pages)


@app.route("/")
@app.route("/index")
def index():
    paises = Pais.query.order_by(Pais.nome).all()  # Ordena os países em ordem alfabética
    return render_template("index.html", paises=paises) 

@app.route("/cadastrar")
def cadastrar():
    return render_template("cadastro.html") 

@app.route("/cadastro", methods=['GET','POST'])
def cadastro():
    if request.method == "POST":
        nome = request.form.get("nome")
        ano = request.form.get("ano")
        populacao = request.form.get("populacao")
        pib = request.form.get("pib")
        totalLixo = request.form.get("totalLixo")
        totalReciclado = request.form.get("totalReciclado")
        
        if nome and ano and populacao and pib and totalLixo and totalReciclado:
            p = Pais(nome,ano,populacao,pib,totalLixo,totalReciclado)
            db.session.add(p)
            db.session.commit()
            
    return redirect(url_for("index"))

@app.route("/excluir/<int:id>")
def excluir(id):
    # Obter o país a ser excluído
    pais = Pais.query.filter_by(_id=id).first()
    
    # Excluir o país se existir
    if pais:
        db.session.delete(pais)
        db.session.commit()
    
    # Configurações de paginação
    ITEMS_PER_PAGE = 10
    page = request.args.get('page', 1, type=int)  # Página atual, padrão 1
    
    # Atualizar o total de itens e calcular o número de páginas
    total_items = Pais.query.count()
    total_pages = math.ceil(total_items / ITEMS_PER_PAGE)
    
    # Consultar apenas os itens da página atual
    paises = (Pais.query
            .order_by(Pais.nome)  # Ordenação opcional
              .offset((page - 1) * ITEMS_PER_PAGE)
            .limit(ITEMS_PER_PAGE)
            .all())
    
    # Renderizar a página com os dados atualizados
    return render_template("listar.html", paises=paises, page=page, total_pages=total_pages)

@app.route("/atualizar/<int:id>", methods=['GET', 'POST'])
def atualizar(id):
    pais = Pais.query.filter_by(_id=id).first()
    
    if request.method == "POST":
            nome = request.form.get("nome")
            ano = request.form.get("ano")
            populacao = request.form.get("populacao")
            pib = request.form.get("pib")
            totalLixo = request.form.get("totalLixo")
            totalReciclado = request.form.get("totalReciclado")
            
            if nome and ano and populacao and pib and totalLixo and totalReciclado:
                pais.nome = nome
                pais.ano = ano
                pais.populacao = populacao
                pais.pib = pib
                pais.totalLixo = totalLixo
                pais.totalReciclado = totalReciclado
                
                db.session.commit()
                
                return redirect(url_for("listar"))
            
    return render_template("atualizar.html", pais=pais)

@app.route("/sobre")
def sobre():
    return render_template("sobre.html") 
            
if __name__ == '__main__':
    app.run(debug=True)