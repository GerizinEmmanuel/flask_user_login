from app import app, db
from flask import render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required

from app.models.forms import LoginForm,SignupForm,EditForm,OTPForm,PasswordForm,UsernameForm,InputPassword
from app.models.tables import User
from app.utils.otp import gerar_codigo

@app.route('/')
#@app.route("/", defaults={"nome":None})
def inicio():
    #if nome: return render_template('index.html',nome=nome)
    #else: 
        return render_template('index.html')
    
#@app.route('/login/<int:id_utilizador>',methods=['POST','GET'])
@app.route('/login',methods=['POST','GET'])
def login():
    if User.is_authenticated:
        logout_user()

    form=LoginForm()
    if form.validate_on_submit():
        utilizador = User.query.filter_by(username=form.username.data).first()
        if utilizador and utilizador.password == form.password.data:
            if utilizador.auth2:
                login_user(utilizador)
                return redirect(url_for('inicio'))
            else: return redirect(url_for('form_otp',id_utilizador=utilizador.id,login_auto='True'))
            #return render_template("index.html",utilizador=utilizador)
        else: flash("Nome de utilizador ou palavra-passe incorreta.")

    return render_template('form_login.html',form=form)

@app.route("/form_otp/<int:id_utilizador>/<string:login_auto>",methods=['GET','POST'])
@app.route("/form_otp/<int:id_utilizador>",defaults={"login_auto":None},methods=['GET','POST'])
def form_otp(id_utilizador,login_auto):
    form=OTPForm()
    global gerar_codigo
    codigo_atual=gerar_codigo.now()
    print(codigo_atual)
    
    if form.validate_on_submit():
        input_otp = form.input_otp.data

        if input_otp==codigo_atual:
            #flash("Os códigos coincidem!")
            utilizador=User.query.filter_by(id=id_utilizador).first()
            if login_auto:
                utilizador.auth2=True
                db.session.commit()
                login_user(utilizador)
                return redirect(url_for('inicio'))
            return redirect(url_for('definir_password',id_utilizador=id_utilizador))
        else: flash("O código inserido está incorreto.")
    return render_template('form_otp.html',form=form)

@app.route("/identificar",methods=['GET','POST'])
def identificar_utilizador():
    form=UsernameForm()
    if form.validate_on_submit():
        utilizador=User.query.filter_by(username=form.username.data).first()
        if utilizador:
            return redirect(url_for('form_otp',id_utilizador=utilizador.id))
        else:
            flash("Utilizador não encontrado!")
    return render_template("form_username.html",form=form)

@app.route("/definir_password/<int:id_utilizador>",methods=['GET','POST'])
def definir_password(id_utilizador):
    form=PasswordForm()
    utilizador=User.query.filter_by(id=id_utilizador).first()
    if form.validate_on_submit():
        nova_password=form.password.data
        try:
            utilizador.password=nova_password
            utilizador.auth2=True
            db.session.commit()
            flash("Palavra-passe definida com sucesso!\nInicia a sessão.")
            return redirect(url_for('login'))
        except Exception as e:
            flash("Erro ao tentar alterar a palavra-passe!")

    return render_template('form_password.html',form=form,utilizador=utilizador)

@app.route("/logout/<string:confirmar>")
@app.route("/logout",defaults={'confirmar':None})
@login_required
def logout(confirmar):
    if confirmar:
        return render_template('confirmar.html')

    logout_user()
    return redirect(url_for("inicio"))


@app.route("/registo",methods=['GET','POST'])
def registo():
    form=EditForm()
    if form.validate_on_submit():
        try:
            nome=form.name.data
            #password=form.password.data
            username=form.username.data
            email=form.email.data
            telefone=form.telefone.data
            novo_utilizador = User(username,nome,email,telefone)

            db.session.add(novo_utilizador)
            db.session.commit()
            #flash("Utilizador registado!\nInicia a sessão.")
            return redirect(url_for("form_otp",id_utilizador=novo_utilizador.id))
        except Exception as e:
            flash(f"Erro ao registar utilizador: {e}.")
    #else: 
        #print(form.errors)
        #flash("Invalid!")
    return render_template("form_dados_utilizador.html",form=form)

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
            #print(form.telefone.data)
            db.session.commit()
            #print(utilizador.telefone)
            return redirect(url_for('inicio'))
        except Exception as e:
            flash(f"Erro ao atualizar os dados: {e}")
            db.session.rollback()
    return render_template("form_dados_utilizador.html",form=form)


@app.route("/apagar/<int:id_utilizador>/<string:confirmar>",methods=['GET','POST'])
@app.route("/apagar/<int:id_utilizador>",methods=['GET','POST'],defaults={'confirmar':None})
@login_required
def apagar_utilizador(id_utilizador,confirmar):
    if confirmar:
        return render_template('confirmar.html',id_utilizador=id_utilizador)
    form=InputPassword()
    utilizador=User.query.filter_by(id=id_utilizador).first()
    if form.validate_on_submit():
        if utilizador.password==form.password.data:
            try:
                db.session.delete(utilizador)
                db.session.commit()
                flash(f"Conta de {utilizador.name} eliminada com sucesso!")
            except Exception as e:
                flash(f"Erro ao tentar apagar conta: {e}")
                db.session.rollback()
            return redirect(url_for('inicio'))
        else:
            flash("A palavra-passe está incorreta! Tenta novamente.") 
    return render_template("form_login.html",form=form)


@app.route('/teste/<int:n>/<int:m>')
def teste(n,m):
    return f"olá {n}, {m}"

@app.route('/teste2')
def teste2():
    return redirect(url_for('teste',n=3,m=5))