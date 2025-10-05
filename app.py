from flask import Flask, render_template, url_for, redirect
from flask_login import LoginManager, login_required, current_user

login_manager = LoginManager()
#O gerenciador de login contém o código que permite que seu aplicativo e o Flask-Login trabalhem juntos, como carregar um usuário a partir de um ID, para onde enviar os usuários quando eles precisam fazer login e coisas do tipo.

login_manager.login_view = 'login_blue.login'
#Define para qual rota redirecionar se o usuário não estiver logado

login_manager.login_message = "Por favor, faça o login para acessar esta página."
login_manager.login_message_category = "warning"
#mensagens customizadas


def createFlask_app():

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'ana123'
    #Por padrão, o Flask-Login usa sessões para autenticação. Isso significa que você deve definir a chave secreta no seu aplicativo, caso contrário, o Flask exibirá uma mensagem de erro solicitando isso.

    login_manager.init_app(app)
    from login import users

    @login_manager.user_loader
    def load_user(user_id):
        return users.get(user_id)
        #Você precisará fornecer um user_loader retorno de chamada. Este retorno de chamada é usado para recarregar o objeto de usuário a partir do ID de usuário armazenado na sessão. Ele deve receber o strID de um usuário e retornar o objeto de usuário correspondente.

    from login import login_blue
    from sensorss import sensors_blue
    from atuadoress import atuadores_blue

    app.register_blueprint(login_blue, url_prefix='/')
    app.register_blueprint(sensors_blue, url_prefix='/sensors')
    app.register_blueprint(atuadores_blue, url_prefix='/atuadores')

    @app.route('/home')
    @login_required
    def home():
        return render_template("home.html")
    
    return app


if __name__ == '__main__':
    app = createFlask_app()
    app.run(host='0.0.0.0', port=8080, debug=True)