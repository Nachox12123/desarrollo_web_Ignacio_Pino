from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://cc5002:programacionweb@localhost:3306/tarea2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'clave_secreta_flask'
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)

# ---------------------------
# MODELOS
# ---------------------------
class Region(db.Model):
    __tablename__ = 'region'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200))
    comunas = db.relationship('Comuna', backref='region', lazy=True)

class Comuna(db.Model):
    __tablename__ = 'comuna'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200))
    region_id = db.Column(db.Integer, db.ForeignKey('region.id'))

class AvisoAdopcion(db.Model):
    __tablename__ = 'aviso_adopcion'
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.Enum('gato', 'perro'), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    unidad_medida = db.Column(db.Enum('a', 'm'), nullable=False)
    comuna_id = db.Column(db.Integer, db.ForeignKey('comuna.id'))
    sector = db.Column(db.String(100))
    cantidad = db.Column(db.Integer)
    nombre = db.Column(db.String(200))
    email = db.Column(db.String(100))
    celular = db.Column(db.String(15))
    descripcion = db.Column(db.Text(500))
    fecha_ingreso = db.Column(db.DateTime, default=datetime.now)
    fecha_entrega = db.Column(db.DateTime, default=datetime.now)
    fotos = db.relationship('Foto', backref='aviso', lazy=True)
    contactos = db.relationship('ContactarPor', backref='aviso', lazy=True)
    comuna = db.relationship('Comuna', backref='avisos')

class Foto(db.Model):
    __tablename__ = 'foto'
    id = db.Column(db.Integer, primary_key=True)
    ruta_archivo = db.Column(db.String(300), nullable=False)
    nombre_archivo = db.Column(db.String(300), nullable=False)
    actividad_id = db.Column(db.Integer, db.ForeignKey('aviso_adopcion.id'))

class ContactarPor(db.Model):
    __tablename__ = 'contactar_por'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.Enum('whatsapp', 'telegram', 'X', 'instagram', 'tiktok', 'otra'), nullable=False)
    identificador = db.Column(db.String(150))
    actividad_id = db.Column(db.Integer, db.ForeignKey('aviso_adopcion.id'))

# ---------------------------
# RUTAS
# ---------------------------

# Portada
@app.route('/')
def portada():
    menu = [
        {'nombre': 'Agregar aviso de adopción', 'url': url_for('formulario')},
        {'nombre': 'Ver listado de adopciones', 'url': url_for('listado', page=1)},
        {'nombre': 'Estadísticas', 'url': url_for('estadisticas')}
    ]
    avisos = AvisoAdopcion.query.order_by(AvisoAdopcion.fecha_ingreso.desc()).limit(5).all()
    return render_template('Portada.html', mensaje_bienvenida="Bienvenido a la plataforma de adopciones",
                           menu=menu, avisos=avisos)


@app.route('/formulario')
def formulario():
    regiones = Region.query.all()
    comunas = Comuna.query.all()
    return render_template('Formulario.html', regiones=regiones, comunas=comunas)

@app.route('/add_aviso', methods=['POST'])
def add_aviso():
    # Obtener datos del formulario
    tipo = request.form.get('tipo') 
    edad = int(request.form.get('edad'))
    unidad_medida = request.form.get('unidad_medida')  
    comuna_id = int(request.form.get('comuna_id'))  
    sector = request.form.get('sector')
    cantidad = int(request.form.get('cantidad'))
    nombre = request.form.get('nombre')
    email = request.form.get('email')
    celular = request.form.get('celular')
    descripcion = request.form.get('descripcion')

    comuna = Comuna.query.get(comuna_id)
    if not comuna:
        flash("La comuna seleccionada no existe.", "error")
        return redirect(url_for('formulario_aviso'))

    aviso = Aviso(
        tipo=tipo,
        edad=edad,
        unidad_medida=unidad_medida,
        comuna_id=comuna_id,
        sector=sector,
        cantidad=cantidad,
        nombre=nombre,
        email=email,
        celular=celular,
        descripcion=descripcion,
        fecha_ingreso=datetime.now(),
        fecha_entrega=datetime.now()
    )

    db.session.add(aviso)
    db.session.commit()
    flash("Aviso agregado correctamente.", "success")
    return redirect(url_for('listado_avisos'))
# Listado de avisos con paginación
@app.route('/listado')
def listado():
    page = request.args.get('page', 1, type=int)
    per_page = 5
    avisos_pag = AvisoAdopcion.query.order_by(AvisoAdopcion.fecha_ingreso.desc()) \
                                    .paginate(page=page, per_page=per_page, error_out=False)
    return render_template('Listado.html',
                           avisos=avisos_pag.items,
                           pagina=avisos_pag.page,
                           paginas=avisos_pag.pages)


@app.route('/detalle/<int:aviso_id>')
def detalle_aviso(aviso_id):
    aviso = AvisoAdopcion.query.get_or_404(aviso_id)
    fotos = aviso.fotos
    contactos = aviso.contactos
    return render_template('Detalle.html', aviso=aviso, fotos=fotos, contactos=contactos)

@app.route('/estadisticas')
def estadisticas():
    return render_template('Estadisticas.html')

# ---------------------------
# RUN
# ---------------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
    app.run(debug=True)
