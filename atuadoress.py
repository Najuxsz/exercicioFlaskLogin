from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import login_required

atuadores_blue = Blueprint("atuadores_blue", __name__, template_folder="templates")

atuadores = {'Servo Motor': 122, 'Lampada': 1, 'Buzzer': 100}

@atuadores_blue.route('/listar_atuadores')
@login_required
def listar_atuadores():
    return render_template("atuadores.html", atuadores=atuadores)

@atuadores_blue.route('/registrar_atuadores', methods=['GET', 'POST'])
@login_required
def registrar_atuadores():
    global atuadores

    if request.method == 'POST':
        nome_atu = request.form['nomeAtu']
        valor_atu = request.form['valorAtu']
        
        if nome_atu:
            atuadores[nome_atu] = valor_atu
        
        return redirect(url_for('atuadores_blue.listar_atuadores'))

    return render_template("registrar_atuadores.html")

@atuadores_blue.route('/del_atuador')
@login_required
def del_atuador():
    global atuadores
    
    atuador_to_delete = request.args.get('atuador')

    if atuador_to_delete in atuadores:
        del atuadores[atuador_to_delete]
    
    return redirect(url_for('atuadores_blue.listar_atuadores'))