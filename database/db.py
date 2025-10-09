from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

# --- Configuración de la base de datos ---
DB_NAME = "tarea2"
DB_USERNAME = "cc5002"
DB_PASSWORD = "programacionweb"
DB_HOST = "localhost"
DB_PORT = 3306

DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

db = SQLAlchemy()

# --- MODELOS ---

class Region(db.Model):
    __tablename__ = 'region'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(200), nullable=False)

    comunas = db.relationship("Comuna", back_populates="region")


class Comuna(db.Model):
    __tablename__ = 'comuna'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(200), nullable=False)
    region_id = db.Column(db.Integer, db.ForeignKey('region.id'), nullable=False)

    region = db.relationship("Region", back_populates="comunas")
    avisos = db.relationship("Aviso", back_populates="comuna")


class Aviso(db.Model):
    __tablename__ = 'aviso_adopcion'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fecha_ingreso = db.Column(db.DateTime, nullable=False, default=datetime.now)
    comuna_id = db.Column(db.Integer, db.ForeignKey('comuna.id'), nullable=False)
    sector = db.Column(db.String(100))
    nombre = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    celular = db.Column(db.String(15))
    tipo = db.Column(db.String(20), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    unidad_medida = db.Column(db.String(2), nullable=False)
    fecha_entrega = db.Column(db.DateTime, nullable=False)
    descripcion = db.Column(db.Text(500))

    comuna = db.relationship("Comuna", back_populates="avisos")


# --- FUNCIONES DE BASE DE DATOS ---

def crear_aviso(datos, fotos, contactos):
    """
    Inserta un aviso de adopción con sus fotos y contactos asociados.
    datos: dict con los campos del aviso
    fotos: lista de tuplas (ruta_archivo, nombre_archivo)
    contactos: lista de tuplas (nombre, identificador)
    """
    session = db.session()
    try:
        aviso = Aviso(**datos)
        session.add(aviso)
        session.commit()

        # Guardar fotos
        for ruta, nombre in fotos:
            session.add(Foto(ruta_archivo=ruta, nombre_archivo=nombre, actividad_id=aviso.id))

        # Guardar contactos
        for nombre, identificador in contactos:
            session.add(ContactarPor(nombre=nombre, identificador=identificador, actividad_id=aviso.id))

        session.commit()
        return True
    except Exception as e:
        print("Error al crear aviso:", e)
        session.rollback()
        return False
    finally:
        session.close()


def obtener_ultimos_avisos(limit=5):
    session = db.session()
    avisos = session.query(Aviso).order_by(Aviso.id.desc()).limit(limit).all()
    session.close()
    return avisos


def obtener_todos_avisos(pagina=1, por_pagina=5):
    session = db.session()
    offset = (pagina - 1) * por_pagina
    avisos = session.query(Aviso).order_by(Aviso.id.desc()).offset(offset).limit(por_pagina).all()
    total = session.query(Aviso).count()
    session.close()
    return avisos, total


def obtener_aviso_por_id(aviso_id):
    session = db.session()
    aviso = session.query(Aviso).filter_by(id=aviso_id).first()
    session.close()
    return aviso


def obtener_regiones():
    session = db.session()
    regiones = session.query(Region).all()
    session.close()
    return regiones


def obtener_comunas_por_region(region_id):
    session = db.session()
    comunas = session.query(Comuna).filter_by(region_id=region_id).all()
    session.close()
    return comunas
    total = session.query(Aviso).count()
    session.close()
    return avisos, total


def obtener_aviso_por_id(aviso_id):
    session = SessionLocal()
    aviso = session.query(Aviso).filter_by(id=aviso_id).first()
    session.close()
    return aviso


def obtener_regiones():
    session = SessionLocal()
    regiones = session.query(Region).all()
    session.close()
    return regiones


def obtener_comunas_por_region(region_id):
    session = SessionLocal()
    comunas = session.query(Comuna).filter_by(region_id=region_id).all()
    session.close()
    return comunas
