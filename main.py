
from fastapi import FastAPI, HTTPException
from typing import List, Optional
from datetime import date

app = FastAPI()
db_usuarios = [
    {"id_usuario": 1, "nombre": "Karem", "apellido": "Barandica", "tipo_registro": "usuario", "numero_identificacion": 123, "correo": "karem@mail.com"},
    {"id_usuario": 2, "nombre": "Juan", "apellido": "Pérez", "tipo_registro": "trabajador", "numero_identificacion": 456, "correo": "juan@mail.com"},
    {"id_usuario": 3, "nombre": "Empresa A", "apellido": "SAS", "tipo_registro": "empresa", "numero_identificacion": 789, "correo": "empresaA@mail.com"},
    {"id_usuario": 4, "nombre": "Maria", "apellido": "Gomez", "tipo_registro": "usuario", "numero_identificacion": 321, "correo": "maria@mail.com"},
    {"id_usuario": 5, "nombre": "Carlos", "apellido": "Ruiz", "tipo_registro": "trabajador", "numero_identificacion": 654, "correo": "carlos@mail.com"}
]

db_cursos = [
    {"id_curso": 1, "nombre_curso": "Trabajador Autorizado", "intensidad_horaria": 32},
    {"id_curso": 2, "nombre_curso": "Reentrenamiento", "intensidad_horaria": 8},
    {"id_curso": 3, "nombre_curso": "Coordinador", "intensidad_horaria": 80},
    {"id_curso": 4, "nombre_curso": "Avanzado", "intensidad_horaria": 40},
    {"id_curso": 5, "nombre_curso": "Básico", "intensidad_horaria": 16}
]

db_facturas = [
    {"id_factura": 1, "id_empresa": 3, "fecha": date(2023, 2, 16), "total": 500000.0},
    {"id_factura": 2, "id_empresa": 3, "fecha": date(2023, 3, 10), "total": 250000.0},
    {"id_factura": 3, "id_empresa": 1, "fecha": date(2023, 4, 5), "total": 120000.0},
    {"id_factura": 4, "id_empresa": 2, "fecha": date(2023, 5, 20), "total": 80000.0},
    {"id_factura": 5, "id_empresa": 3, "fecha": date(2023, 6, 15), "total": 1000000.0}
]

db_pagos = [{"id_pago": i, "id_factura": i, "monto": 1000.0 * i, "metodo": "Efectivo"} for i in range(1, 6)]
db_certificados = [{"id_certificado": i, "codigo": f"CERT-{i}", "id_usuario": i, "id_curso": 1} for i in range(1, 6)]
db_accidentes = [{"id_accidente": i, "id_trabajador": i, "fecha": date.today(), "descripcion": "Incidente menor"} for i in range(1, 6)]
db_alertas = [{"id_alerta": i, "id_usuario": i, "estado": "pendiente"} for i in range(1, 6)]

# --- RUTAS CRUD (USUARIOS) ---
@app.get("/usuarios")
def listar_usuarios():
    return db_usuarios

@app.post("/usuarios")
def crear_usuario(usuario):
    db_usuarios.append(usuario.dict())
    return {"mensaje": "Usuario registrado", "usuario": usuario}

@app.put("/usuarios/{id_usuario}")
def actualizar_usuario(id_usuario: int, usuario_upd):
    for index, u in enumerate(db_usuarios):
        if u["id_usuario"] == id_usuario:
            db_usuarios[index] = usuario_upd.dict()
            return {"mensaje": "Usuario actualizado"}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@app.delete("/usuarios/{id_usuario}")
def eliminar_usuario(id_usuario: int):
    for index, u in enumerate(db_usuarios):
        if u["id_usuario"] == id_usuario:
            db_usuarios.pop(index)
            return {"mensaje": "Usuario eliminado"}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

# --- RUTAS CRUD (CURSOS) ---
@app.get("/cursos")
def listar_cursos():
    return db_cursos

@app.post("/cursos")
def crear_curso(curso):
    db_cursos.append(curso.dict())
    return {"mensaje": "Curso registrado"}

@app.put("/cursos/{id_curso}")
def actualizar_curso(id_curso: int, curso_upd):
    for index, c in enumerate(db_cursos):
        if c["id_curso"] == id_curso:
            db_cursos[index] = curso_upd.dict()
            return {"mensaje": "Curso actualizado"}
    raise HTTPException(status_code=404, detail="Curso no encontrado")

@app.delete("/cursos/{id_curso}")
def eliminar_curso(id_curso: int):
    for index, c in enumerate(db_cursos):
        if c["id_curso"] == id_curso:
            db_cursos.pop(index)
            return {"mensaje": "Curso eliminado"}
    raise HTTPException(status_code=404, detail="Curso no encontrado")

# --- RUTAS CRUD (FACTURAS) ---
@app.get("/facturas")
def listar_facturas():
    return db_facturas

@app.post("/facturas")
def crear_factura(factura):
    db_facturas.append(factura.dict())
    return {"mensaje": "Factura registrada"}

# --- RUTAS CRUD (PAGOS) ---
@app.get("/pagos")
def listar_pagos():
    return db_pagos

@app.post("/pagos")
def crear_pago(pago):
    db_pagos.append(pago.dict())
    return {"mensaje": "Pago registrado"}

# --- RUTAS CRUD (CERTIFICADOS) ---
@app.get("/certificados")
def listar_certificados():
    return db_certificados

@app.post("/certificados")
def crear_certificado(cert):
    db_certificados.append(cert.dict())
    return {"mensaje": "Certificado registrado"}

# --- RUTAS CRUD (ACCIDENTES) ---
@app.get("/accidentes")
def listar_accidentes():
    return db_accidentes

@app.put("/accidentes/{id_accidente}")
def actualizar_accidente(id_accidente: int, acc_upd):
    for index, a in enumerate(db_accidentes):
        if a["id_accidente"] == id_accidente:
            db_accidentes[index] = acc_upd.dict()
            return {"mensaje": "Reporte de accidente actualizado"}
    raise HTTPException(status_code=404, detail="Accidente no encontrado")

# --- RUTAS CRUD (ALERTAS) ---
@app.get("/alertas")
def listar_alertas():
    return db_alertas

@app.put("/alertas/{id_alerta}")
def actualizar_alerta(id_alerta: int, alerta_upd):
    for index, al in enumerate(db_alertas):
        if al["id_alerta"] == id_alerta:
            db_alertas[index] = alerta_upd.dict()
            return {"mensaje": "Alerta actualizada"}
    raise HTTPException(status_code=404, detail="Alerta no encontrada")

@app.delete("/alertas/{id_alerta}")
def eliminar_alerta(id_alerta: int):
    for index, al in enumerate(db_alertas):
        if al["id_alerta"] == id_alerta:
            db_alertas.pop(index)
            return {"mensaje": "Alerta eliminada"}
    raise HTTPException(status_code=404, detail="Alerta no encontrada")