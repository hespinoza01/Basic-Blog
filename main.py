from flask import Flask, render_template as render, session, redirect, url_for, request

app = Flask(__name__, template_folder='views')

# Diccionarios para almacenar la información
USERS = {}

# Función a ejecutarse antes de responder cada petición
@app.before_request
def before_request_handler():
    if 'usernamme' not in session and request.endpoint in ['index']:
        return redirect(url_for('acceso'))
    elif 'username' in session and request.endpoint in ['acceso', 'registro']:
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


@app.route('/acceso')
def acceso():
    return render('acceso.html')


@app.route('/registro')
def registro():
    return 'registro'


if __name__ == '__main__':
    app.run(port=9000, debug=True)