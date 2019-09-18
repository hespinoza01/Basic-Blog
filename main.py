from flask import Flask, render_template as render, session, redirect, url_for, request, flash
from flask_mail import Mail, Message
import threading
import locale
from datetime import datetime
from config import Config

app = Flask(__name__, template_folder='views', static_folder='public')

app.config.from_object(Config) #Cargando configuraciones desde una clase externa
mail = Mail() #Inicializando instancia del objeto Mail

locale.setlocale(locale.LC_TIME, 'es_ES.utf8')

# Diccionarios para almacenar la información
USERS = dict()
POSTS = dict()

# Usuario inicial
USERS['haroldesptru@gmail.com'] = {'fullname': 'Harold Espinoza', 'password': 'abcd'}

# Publicación inicial
POSTS[1] = {
    'title': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Magni, provident.',
    'date': '17 de septiembre del 2019',
    'content': """
        Lorem ipsum dolor sit amet, consectetur adipisicing elit. Adipisci at consequatur
        consequuntur debitis dolor dolores doloribus dolorum, eius eum explicabo facere harum impedit, itaque
        laboriosam libero magnam magni minima modi molestias nam natus neque non nostrum odio omnis quasi quia
        quisquam recusandae rem repellat sed totam ullam, unde. Aliquid beatae corporis eligendi est ipsam quasi
        soluta temporibus! Consequatur esse nemo obcaecati quos repellat voluptatem? A accusantium aliquid
        architecto aspernatur consequuntur cum delectus distinctio dolor, dolore dolores eligendi exercitationem
        illum itaque laboriosam magnam magni mollitia neque nostrum numquam officiis perferendis perspiciatis
        provident quaerat quis reprehenderit repudiandae rerum saepe sapiente sed tempora veniam voluptate
        voluptates voluptatum! A ad adipisci aliquid at cupiditate dolore eligendi fugit illum iure laboriosam,
        molestiae, nobis non placeat quidem rem tempore vero voluptatem! Architecto impedit nam natus obcaecati
        repellendus rerum voluptatem. Id nobis optio ratione. Cupiditate dolorem ipsam libero magnam nobis omnis
        ratione rem repellat sint temporibus, ullam!
    """
}


# Función para el envío que correos sobre nuevas publicaciones a los usuarios registrados
def new_post_email(author='default author', post='0'):

    def send_email(post_author, post_id):
        with app.app_context():
            with mail.connect() as con:
                for user_email, values in USERS.items():
                    user_fullname = values['fullname']
                    msg = Message('Nueva publicación',
                                  sender=app.config['MAIL_USERNAME'],
                                  recipients=[user_email])

                    msg.html = render('email.html', fullname=user_fullname, author=post_author, post_id=post_id)
                    mail.send(msg)

    sender = threading.Thread(
        name='mail_sender',
        target=send_email,
        args=(author, post)
    )

    sender.start()


def get_post_date():
    new_date = datetime.now()
    post_date = new_date.strftime('%d de %B del %Y')
    return post_date


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
    return render('404.html')


@app.route('/', methods=('GET', 'POST'))
def index():
    user_fullname = USERS.get(session['username'])['fullname']
    user_email = session.get('username')

    if request.method == 'POST':
        id_post = len(POSTS) + 1
        POSTS[id_post] = {
            'title': request.form['post-title'],
            'date': get_post_date(),
            'content': request.form['post-content']
        }

        new_post_email(user_fullname, id_post)

        return redirect(url_for('index'))

    return render('inicio.html', user_fullname=user_fullname, user_email=user_email, posts=POSTS)


@app.route('/<int:id>')
def post(id):
    user_fullname = USERS.get(session['username'])['fullname']
    user_email = session.get('username')

    post = POSTS.get(id)
    title = post['title']
    date = post['date']
    content = post['content']

    return render('post.html', user_fullname=user_fullname, user_email=user_email, title=title, date=date, content=content)


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


@app.route('/salir')
def salir():
    if 'username' in session:
        session.pop('username')
        return redirect(url_for('acceso'))


if __name__ == '__main__':
    mail.init_app(app)

    app.run(port=9000, debug=True)