from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import login_required

sensors_blue = Blueprint("sensors_blue", __name__, template_folder="templates")

sensores = {'Umidade': 22, 'temperatura': 23, 'luminosidade': 1034}

@sensors_blue.route('/listar_sensores')
@login_required
def listar_sensores():
    return render_template("sensors.html", sensores=sensores)

@sensors_blue.route('/registrar_sensores', methods=['GET', 'POST'])
@login_required
def registrar_sensores():
    global sensores

    if request.method == 'POST':
        nome_sensor = request.form['nome']
        valor_sensor = request.form['valor']
        
        if nome_sensor:
            sensores[nome_sensor] = valor_sensor
        
        return redirect(url_for('sensors_blue.listar_sensores'))

    return render_template("registrar_sensores.html")

@sensors_blue.route('/del_sensor')
@login_required
def del_sensor():
    global sensores
    
    sensor_to_delete = request.args.get('sensor')

    if sensor_to_delete in sensores:
        del sensores[sensor_to_delete]
    
    return redirect(url_for('sensors_blue.listar_sensores'))