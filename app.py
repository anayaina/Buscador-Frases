#______________ALUMNOS________________
#ANA PAULINA ANAYA ARIAS_____219205302
#RAMON ALEJANDRO IRIBE COTA__219211642
#______TRABAJO FINAL DESARROLLO4______

from flask import Flask, render_template, request, session
from werkzeug.utils import redirect
import secrets
import json
from passlib.hash import sha256_crypt

app = Flask(__name__)

app.secret_key = secrets.token_hex(16)

archivo = './static/frases_celebres.csv'

#leer archivo json con los diccionarios de usuarios
with open("./static/usuarios.json","r") as fh:
    diccionario_usuarios = json.load(fh)

@app.route('/')
def home():
    if 'email' in session:
        user = diccionario_usuarios[session['email']]['username']
        return render_template('home.html', username=user)
    return render_template('home.html')


@app.route('/login', methods=['GET','POST']) # GET---> info de ida del server hacia el navegador
def login():                                 # POST --> info de regreso del navegador al server
    error = None
    if request.method == 'POST':
        # Validar que el nombre de usuario exista en nuestro registro
        if (request.form['email'] in diccionario_usuarios):
            email = request.form['email']
            username = diccionario_usuarios[email]['username'] 
            password = diccionario_usuarios[email]['password']   # Contraseña hasheada guardada en nuestro registro
            # Obtener el hash de la contraseña ingresada y validar que sea la misma que tenemos registrada
            if (sha256_crypt.verify(request.form['password'], password) == True):
                session['email'] = email  # Ingresar al usuario a la sesión
                return redirect('/') # Redirigir al index
            else:
                return render_template('login.html', error='Password incorrecto')
        else:
                return render_template('login.html', error='Email incorrecto')
    else:   
        return render_template('login.html', error=None)


@app.route('/logout')
def logout():
    if 'email' in session:
        session.pop('email', None)
        return redirect('/')


@app.route('/register', methods=['GET','POST'])
def register():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        # Validar que el email ingresado en el formulario de registro no esté registrado previamente
        if (email not in diccionario_usuarios):
            # Obtener el nombre de usuario ingresada en el formulario
            username = request.form['username']
            # Obtener el hash de la contraseña ingresada en el formulario
            hash_password = sha256_crypt.hash(request.form['password'])
            # Agregar el email como llave a nuestro diccionario, mapear el username y la contraseña hasheada
            # Lista de frases favoritas creada pero vacía
            diccionario_usuarios[email] = {'username': username, 'password': hash_password, 'lista': []}
            # Actualizar el archivo json del diccionario de usuarios
            with open("./static/usuarios.json","w") as usuarios_json:
                json.dump(diccionario_usuarios, usuarios_json)
            # Iniciar sesión con el usuario recien registrado y redireccionar al index
            session['email'] = email
            return redirect('/')
        else:
            return render_template('register.html', error='El e-mail ya está registrado')
    else:   
        return render_template('register.html', error=None)

@app.route('/tabla')
def tabla():
        return render_template('tabla.html')

if __name__ == "__main__":
    app.run(debug=True)


