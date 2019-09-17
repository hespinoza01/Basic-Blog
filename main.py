from flask import Flask, render_template as render, session, redirect, url_for, request, flash

app = Flask(__name__, template_folder='views', static_folder='public')

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SECRET_KEY'] = 'SoyUnaClaveSecreta'

# Diccionarios para almacenar la información
USERS = dict()

# Función a ejecutarse antes de responder cada petición
@app.before_request
def before_request_handler():
    if 'username' not in session and request.endpoint in ['index']:
        return redirect(url_for('acceso'))

    if 'username' in session and request.endpoint in ['acceso', 'registro']:
        return redirect(url_for('index'))


# Acción a realizar en el error 404
@app.errorhandler(404)
def page_not_found(err):
    return """
        <h1>Page not found</h1>
        <a href='/'>Inicio</a>
    """


@app.route('/')
def index():
    return 'Index'


@app.route('/acceso', methods=('GET', 'POST'))
def acceso():
    if request.method == "POST":
        username = request.form['username']
        user = USERS.get(username)

        if user and user['password'] == request.form['password']:
            session['username'] = username
            return redirect(url_for('index'))

        flash('Correo o contraseña incorrecto.')

    return render('acceso.html')


@app.route('/registro', methods=('GET', 'POST'))
def registro():
    if request.method == 'POST':
        fullname = request.form['fullname']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password == confirm_password:
            USERS[username] = {'fullname': fullname, 'password': password}
            return render('registro.html', success=True)

    return render('registro.html', success=False)


if __name__ == '__main__':
    app.run(port=9000, debug=True)