from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import UserMixin, login_user, logout_user, login_required, current_user
#Para facilitar a implementação de uma classe de usuário, você pode herdar de UserMixin, que fornece implementações padrão para todas essas propriedades e métodos. (Mas não é obrigatório.)

class Usuario(UserMixin):
    def __init__(self, id, username, senha):
        self.id = id
        self.username = username 
        self.senha = senha

    @staticmethod
    def get(user_id):
        return users.get(user_id)

login_blue = Blueprint("login_blue", __name__, template_folder="templates", url_prefix='/')


users = {
    "1": Usuario(id="1", username="aninha", senha="123"),
    "2": Usuario(id="2", username="admin", senha="321")
}

@login_blue.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    return redirect(url_for('login_blue.login'))


# --- Rotas ---
@login_blue.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        senha = request.form.get('senha')

        usuario_encontrado = None
        for user in users.values():
            if user.username == username and user.senha == senha:
                usuario_encontrado = user
                break

        if usuario_encontrado:
            login_user(usuario_encontrado)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('home'))
        else:
            error_message = "Usuário ou senha inválidos."
            return render_template('login.html', error=error_message)

    return render_template('login.html')

@login_blue.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login_blue.login'))

@login_blue.route('/registrar_usuario')
@login_required
def registrar_usuario():
    return render_template("registrar_usuario.html")

@login_blue.route('/add_user', methods=['POST'])
@login_required
def add_user():
    global users
    if request.method == 'POST':
        username = request.form.get('username')
        senha = request.form.get('senha')

        if username and senha:
            novo_id = str(max([int(k) for k in users.keys()] + [0]) + 1)
            novo_usuario = Usuario(id=novo_id, username=username, senha=senha)
            users[novo_id] = novo_usuario

    return redirect(url_for('login_blue.listar_usuarios'))

@login_blue.route('/listar_usuarios')
@login_required
def listar_usuarios():
    return render_template("usuarios.html", devices=users.values())

@login_blue.route('/del_user')
@login_required
def del_user():
    user_id_to_delete = request.args.get('user_id')

    if user_id_to_delete in users:
        del users[user_id_to_delete]

    return redirect(url_for('login_blue.listar_usuarios'))