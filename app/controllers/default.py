from app import app, db
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, login_required

from app.models.forms import LoginForm,SignupForm,EditForm
from app.models import User

@app.route('/')
#@app.route("/", defaults={"nome":None})
def inicio():
    #if nome: return render_template('index.html',nome=nome)
    #else: 
        return render_template('index.html')
    
@app.route('/login',methods=['POST','GET'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        utilizador = User.query.filter_by(username=form.username.data).first()
        if utilizador and utilizador.password == form.password.data:
            login_user(utilizador)
            return redirect(url_for('inicio'))
            #return render_template("index.html",utilizador=utilizador)
        else: flash("Nome de utilizador ou palavra-passe incorreta.")

    return render_template('login.html',form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("inicio"))

@app.route("/registo",methods=['GET','POST'])
def registo():
    form=SignupForm()
    if form.validate_on_submit():
        nome=form.name.data
        password=form.password.data
        username=form.username.data
        email=form.email.data
        telefone=form.telefone.data
        novo_utilizador = User(username,password,nome,email,telefone)

        db.session.add(novo_utilizador)
        db.session.commit()
        flash("Utilizador registado!\nInicia a sessão.")
        return redirect(url_for("login"))
    #else: 
        #print(form.errors)
        #flash("Invalid!")
    return render_template("form_registo.html",form=form)


@app.route("/atualizar/<int:id_utilizador>",methods=['GET','POST'])
@login_required
def atualizar_utilizador(id_utilizador):
    form=EditForm()
    utilizador = User.query.filter_by(id=id_utilizador).first()
    if form.validate_on_submit():
        try:
            utilizador.name=form.name.data
            utilizador.username=form.username.data
            utilizador.email=form.email.data
            utilizador.telefone=form.telefone.data
            print(form.telefone.data)
            db.session.commit()
            print(utilizador.telefone)
            return redirect(url_for('inicio'))
        except Exception as e:
            flash(f"Erro ao atualizar os dados: {e}")
            db.session.rollback()
    return render_template("form_editar_utilizador.html",form=form)

@app.route("/apagar/<int:id_utilizador>",methods=['GET','POST'])
@login_required
def apagar_utilizador(id_utilizador):
    utilizador=User.query.filter_by(id=id_utilizador).first()
    try:
        db.session.delete(utilizador)
        db.session.commit()
        flash(f"Conta de {utilizador.name} eliminada com sucesso!")
    except Exception as e:
        flash(f"Erro ao tentar apagar conta: {e}")
        db.session.rollback()
    return redirect(url_for('inicio'))

