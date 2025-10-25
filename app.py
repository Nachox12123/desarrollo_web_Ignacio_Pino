from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import os
from werkzeug.utils import secure_filename
from sqlalchemy import func, extract

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

class Comentario(db.Model):
    __tablename__ = 'comentario'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    texto = db.Column(db.String(300), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False, default=datetime.now)
    aviso_id = db.Column(db.Integer, db.ForeignKey('aviso_adopcion.id'), nullable=False)
    aviso = db.relationship('AvisoAdopcion', backref='comentarios')

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
        return redirect(url_for('formulario'))

    aviso = AvisoAdopcion(
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
    return redirect(url_for('listado'))




@app.route('/listado')
@app.route('/listado/<int:page>')
def listado(page=1):
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


@app.route('/api/estadisticas/por_dia')
def estadisticas_por_dia():
    """Retorna la cantidad de avisos por día para gráfico de líneas"""
    try:
        resultados = db.session.query(
            func.date(AvisoAdopcion.fecha_ingreso).label('fecha'),
            func.count(AvisoAdopcion.id).label('cantidad')
        ).group_by(func.date(AvisoAdopcion.fecha_ingreso)).order_by('fecha').all()
        
        data = []
        for fecha, cantidad in resultados:
            data.append({
                'fecha': fecha.strftime('%Y-%m-%d'),
                'cantidad': cantidad
            })
        
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/estadisticas/por_tipo')
def estadisticas_por_tipo():
    """Retorna la cantidad de avisos por tipo de mascota para gráfico de torta"""
    try:
        resultados = db.session.query(
            AvisoAdopcion.tipo,
            func.count(AvisoAdopcion.id).label('cantidad')
        ).group_by(AvisoAdopcion.tipo).all()
        
        data = []
        for tipo, cantidad in resultados:
            data.append({
                'tipo': tipo,
                'cantidad': cantidad
            })
        
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/estadisticas/por_mes_tipo')
def estadisticas_por_mes_tipo():
    """Retorna la cantidad de avisos por mes y tipo para gráfico de barras"""
    try:
        resultados = db.session.query(
            extract('year', AvisoAdopcion.fecha_ingreso).label('año'),
            extract('month', AvisoAdopcion.fecha_ingreso).label('mes'),
            AvisoAdopcion.tipo,
            func.count(AvisoAdopcion.id).label('cantidad')
        ).group_by('año', 'mes', AvisoAdopcion.tipo).order_by('año', 'mes').all()
        
        data = []
        for año, mes, tipo, cantidad in resultados:
            data.append({
                'año': int(año),
                'mes': int(mes),
                'mes_nombre': datetime(int(año), int(mes), 1).strftime('%B %Y'),
                'tipo': tipo,
                'cantidad': cantidad
            })
        
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/comentarios/<int:aviso_id>')
def obtener_comentarios(aviso_id):
    """Obtiene los comentarios de un aviso específico"""
    try:
        comentarios = Comentario.query.filter_by(aviso_id=aviso_id).order_by(Comentario.fecha.desc()).all()
        
        data = []
        for comentario in comentarios:
            data.append({
                'id': comentario.id,
                'nombre': comentario.nombre,
                'texto': comentario.texto,
                'fecha': comentario.fecha.strftime('%Y-%m-%d %H:%M:%S')
            })
        
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/comentarios/<int:aviso_id>', methods=['POST'])
def agregar_comentario(aviso_id):
    """Agrega un nuevo comentario a un aviso con protecciones básicas"""
    try:
        client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.environ.get('REMOTE_ADDR', ''))
        
        comentarios_recientes = Comentario.query.filter(
            Comentario.fecha > datetime.now() - timedelta(minutes=1)
        ).count()
        
        if comentarios_recientes >= 10:  
            return jsonify({'error': 'Demasiados comentarios enviados recientemente. Espere un momento.'}), 429
        
        data = request.get_json()
     
        if not data or not isinstance(data, dict):
            return jsonify({'error': 'Datos inválidos'}), 400
            
        nombre = data.get('nombre', '').strip()
        texto = data.get('texto', '').strip()
        
        if not nombre or len(nombre) < 3 or len(nombre) > 80:
            return jsonify({'error': 'El nombre debe tener entre 3 y 80 caracteres'}), 400
        
        if not texto or len(texto) < 5 or len(texto) > 300:
            return jsonify({'error': 'El comentario debe tener entre 5 y 300 caracteres'}), 400
        
        palabras_prohibidas = ['<script', 'javascript:', 'onclick=', 'onerror=']
        contenido_total = (nombre + ' ' + texto).lower()
        
        for palabra in palabras_prohibidas:
            if palabra in contenido_total:
                return jsonify({'error': 'Contenido no permitido detectado'}), 400
        
        
        
        aviso = AvisoAdopcion.query.get(aviso_id)
        if not aviso:
            return jsonify({'error': 'El aviso no existe'}), 404
        

        comentario = Comentario(
            nombre=nombre[:80],  
            texto=texto[:300],   
            aviso_id=aviso_id,
            fecha=datetime.now()
        )
        
        db.session.add(comentario)
        db.session.commit()
        
        return jsonify({
            'id': comentario.id,
            'nombre': comentario.nombre,
            'texto': comentario.texto,
            'fecha': comentario.fecha.strftime('%Y-%m-%d %H:%M:%S'),
            'success': True
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error interno del servidor'}), 500

# ---------------------------
# RUN
# ---------------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
    app.run(debug=True)
