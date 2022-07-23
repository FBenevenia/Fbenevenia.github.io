from datetime import datetime
from email.policy import default
import functools
from turtle import title
from flask import Flask, flash ,jsonify, redirect, render_template,request,session,url_for,g,abort
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import post_dump
from sqlalchemy import ForeignKey
from werkzeug.security import check_password_hash, generate_password_hash
app=Flask(__name__)
app.secret_key = 'super secret key'
CORS(app)
# configuro la base de datos, con el nombre el usuario y la clave
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://b58a0c8d16a5e3:99f2a323@us-cdbr-east-06.cleardb.net/heroku_d72c663c2c9d595'
#                                               user:clave@localhost/nombreBaseDatos
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db= SQLAlchemy(app)
ma=Marshmallow(app)
# defino la tabla
class User(db.Model):   # la clase Contacto hereda de db.Model     
    id=db.Column(db.Integer, primary_key=True)   #define los campos de la tabla
    usuario=db.Column(db.String(50))
    password=db.Column(db.Text)
    def __init__(self,usuario,password):   #crea el  constructor de la clase
        self.usuario=usuario   # no hace falta el id porque lo crea sola mysql por ser auto_incremento
        self.password=password
    def __repr__(self) -> str:
        return f'User: {self.usuario}'

class Contacto(db.Model):   # la clase Contacto hereda de db.Model     
    id=db.Column(db.Integer, primary_key=True)   #define los campos de la tabla
    nombre=db.Column(db.String(40))
    apellido=db.Column(db.String(40))
    telefono=db.Column(db.Integer)
    mail=db.Column(db.String(100))
    asunto=db.Column(db.String(50))
    descripcion=db.Column(db.String(500))
    def __init__(self,nombre,apellido,telefono,mail,asunto,descripcion):   #crea el  constructor de la clase
        self.nombre=nombre   # no hace falta el id porque lo crea sola mysql por ser auto_incremento
        self.apellido=apellido
        self.telefono=telefono
        self.mail=mail
        self.asunto=asunto
        self.descripcion=descripcion

class PostPE(db.Model):   # la clase PostPE hereda de db.Model     
    id=db.Column(db.Integer, primary_key=True)   #define los campos de la tabla
    author=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    creado=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    titulo=db.Column(db.String(50))
    body=db.Column(db.String(500))
    def __init__(self,author,titulo,body):   #crea el  constructor de la clase
        self.author=author   # no hace falta el id porque lo crea sola mysql por ser auto_incremento
        self.titulo=titulo
        self.body=body

db.create_all()  # crea las tablas
#  ************************************************************

@app.route('/')
def indexs():
    return "<h1>Corriendo servidor Flask</h1>"


class UserSchema(ma.Schema):
    class Meta:
        fields=('id','usuario','password')
User_schema=UserSchema()            # para crear un producto
Users_schema=UserSchema(many=True)  # multiples registros
 
# crea los endpoint o rutas (json)
@app.route('/Users',methods=['GET'])
def get_Users():
    all_users=User.query.all()     # query.all() lo hereda de db.Model
    result=Users_schema.dump(all_users)  # .dump() lo hereda de ma.schema
    return jsonify(result)

#Crear usuario
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        password = request.form.get('password')
        user = User(usuario, generate_password_hash(password))
        error = None
        if not usuario:
            error = 'Se requiere nombre de usuario'
        elif not password:
            error = 'Se requiere contraseña'
        
        user_name = User.query.filter_by(usuario=usuario).first()
        if user_name == None:
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))            
        else:
            error = f'El usuario {usuario} ya está registrado'
        flash(error)
    return render_template('register.html')


#Iniciar Sesión
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        password = request.form.get('password')
        error = None
        user = User.query.filter_by(usuario=usuario).first()

        if user == None:
            error = 'Nombre de usuario incorrecto'
        elif not check_password_hash(user.password, password):
            error = 'La contraseña es incorrecta'

        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('index'))
        flash(error)
    return render_template('login.html')

@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get_or_404(user_id)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('login'))
        return view(**kwargs)
    return wrapped_view

class ContactoSchema(ma.Schema):
    class Meta:
        fields=('id','nombre','apellido','telefono','mail','asunto','descripcion')
Contacto_schema=ContactoSchema()            # para crear un producto
Contactos_schema=ContactoSchema(many=True)  # multiples registros
 
# crea los endpoint o rutas (json)
#@app.route('/Contactos',methods=['GET'])
#def get_Contactos():
#    all_contactos=Contacto.query.all()     # query.all() lo hereda de db.Model
#    result=Contactos_schema.dump(all_contactos)  # .dump() lo hereda de ma.schema
#    return jsonify(result)
 
# crea los endpoint
@app.route('/formulario', methods=['GET','POST'])
def formulario():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        telefono = request.form.get('telefono')
        mail = request.form.get('mail')        
        asunto = request.form.get('asunto')
        descripcion = request.form.get('descripcion')        

        contactoF = Contacto(nombre,apellido,telefono,asunto,mail,descripcion)
        error = None
        if not descripcion:
            error = 'Se requiere una descripcion'
        if error is not None:
            flash(error)
        else:
            db.session.add(contactoF)
            db.session.commit()
            return redirect(url_for('formulario'))
        flash(error)
    return render_template('formulario.html')

# crea los endpoint
@app.route('/admin',methods=['GET'])
def admin():
    contactoF=Contacto.query.all()
    db.session.commit()
    return render_template('admin.html', Contacto=contactoF)

def get_contactoF(id):
    contactoF = Contacto.query.get_or_404(id)
    return contactoF

@app.route('/updateC/<int:id>', methods=['GET','POST'])
def updateC(id):
    contactoF=get_contactoF(id)
    if request.method == 'POST':
        contactoF.nombre = request.form.get('nombre')
        contactoF.apellido = request.form.get('apellido')
        contactoF.telefono = request.form.get('telefono')
        contactoF.mail = request.form.get('mail')
        contactoF.asunto = request.form.get('asunto')
        contactoF.descripcion = request.form.get('descripcion')
        error = None
        if not contactoF.descripcion:
            error = 'Se requiere una descripcion'
        if error is not None:
            flash(error)
        else:
            db.session.add(contactoF)
            db.session.commit()
            return redirect(url_for('admin'))
        flash(error)
    return render_template('update.html', contactoF=contactoF)

# elimina comentario
@app.route('/deleteF/<int:id>')
def deleteF(id):
    contactoF=get_contactoF(id)
    db.session.delete(contactoF)
    db.session.commit()
    return redirect(url_for('admin'))


class PostPESchema(ma.Schema):
    class Meta:
        fields=('id','author','creado','titulo','body')
PostPE_schema=PostPESchema()            # para crear un producto
PostPEs_schema=PostPESchema(many=True)  # multiples registros

# crea los endpoint
@app.route('/home')
def home():
    return render_template('index.html')

# crea los endpoint
@app.route('/presentacion')
def presentacion():
    return render_template('presentacion.html')

# crea los endpoint
@app.route('/simulacion')
def simulacion():
    return render_template('simulacion.html')



#obtener usuario.. nose no funciona
def get_user(id):
    users = User.query.get_or_404(id)
    return users

# crea los endpoint
@app.route('/PostPEs')
def index():
    postPEs=PostPE.query.all()     # query.all() lo hereda de db.Model
    db.session.commit()
    return render_template('Procesos_Estocasticos.html', PostPEs=postPEs, get_user=get_user)

@app.route('/create', methods=['GET','POST'])
@login_required
def create_postPE():
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        body = request.form.get('body')

        post = PostPE(g.user.id, titulo, body)
        error = None
        if not titulo:
            error = 'Se requiere un titulo'
        if error is not None:
            flash(error)
        else:
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('index'))
        flash(error)
    return render_template('createp.html')

#obtener post
def get_post(id):
    post = PostPE.query.get_or_404(id)
    if post is None:
        abort(404, f'Id {id} de la publicacion no existe')
    return post

@app.route('/update/<int:id>', methods=['GET','POST'])
@login_required
def update(id):
    post = get_post(id)
    if request.method == 'POST':
        post.titulo = request.form.get('titulo')
        post.body = request.form.get('body')
        error = None
        if not post.titulo:
            error = 'Se requiere un titulo'
        if error is not None:
            flash(error)
        else:
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('index'))
        flash(error)
    return render_template('updatep.html',post=post)

# elimina post
@app.route('/delete/<int:id>')
@login_required
def delete(id):
    post = get_post(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('index'))


# programa principal *******************************
if __name__=='__main__':  
    app.run(debug=True)
    #, port=5000