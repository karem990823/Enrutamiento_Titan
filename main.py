
from fastapi import FastAPI, HTTPException, Path, Query
from typing import List, Optional
from datetime import date

class Cliente(BaseModel):
    id: int = Field(
        gt=0,
        description="ID mayor a 0"
    )

    nombre: str = Field(
        min_length=3,
        max_length=50,
        description="Mínimo 3 caracteres"
    )

    email: EmailStr = Field(
        description="Correo electrónico válido"
    )

    telefono: str = Field(
        min_length=7,
        max_length=15,
        pattern=r'^\+?[0-9]+$',
        description="Teléfono entre 7-15 dígitos"
    )

    edad: int = Field(
        gt=0,
        lt=120,
        description="Edad entre 1 y 119 años"
    )




class Producto(BaseModel):
    id: int = Field(
        gt=0,
        description="ID mayor a 0"
    )

    nombre: str = Field(
        min_length=3,
        max_length=100,
        description="Mínimo 3 caracteres"
    )

    precio: float = Field(
        gt=0,
        description="Precio mayor a 0"
    )

    stock: int = Field(
        ge=0,
        description="Stock mayor o igual a 0"
    )

    categoria: str = Field(
        min_length=3,
        max_length=50,
        description="Mínimo 3 caracteres"
    )

class Empleado(BaseModel):
    id: int = Field(
        gt=0,
        description="ID mayor a 0"
    )

    nombre: str = Field(
        min_length=3,
        max_length=50,
        description="Mínimo 3 caracteres"
    )

    email: EmailStr = Field(
        description="Correo electrónico válido"
    )

    cargo: str = Field(
        min_length=3,
        max_length=50,
        description="Mínimo 3 caracteres"
    )

    salario: float = Field(
        gt=0,
        description="Salario mayor a 0"
    )

    fecha_contratacion: date = Field(
        description="Fecha en formato YYYY-MM-DD"
    )

class Proveedor(BaseModel):
    id: int = Field(
        gt=0,
        description="ID mayor a 0"
    )

    nombre: str = Field(
        min_length=3,
        max_length=100,
        description="Mínimo 3 caracteres"
    )

    ruc: str = Field(
        min_length=8,
        max_length=11,
        pattern=r'^[0-9]+$',
        description="RUC entre 8-11 dígitos"
    )

    telefono: str = Field(
        min_length=7,
        max_length=15,
        pattern=r'^\+?[0-9]+$',
        description="Teléfono entre 7-15 dígitos"
    )

    direccion: str = Field(
        min_length=5,
        max_length=150,
        description="Mínimo 5 caracteres"
    )

    email: EmailStr = Field(
        description="Correo electrónico válido"
    )
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

@app.get("/usuarios")
def listar_usuarios(
    tipo: Optional[str] = Query(None, description="Filtrar por tipo de registro"),
    nombre_search: Optional[str] = Query(None, min_length=3)
):
    """Obtiene la lista de usuarios. Permite filtrar por tipo y buscar por nombre."""
    resultado = db_usuarios
    if tipo:
        resultado = [u for u in resultado if u["tipo_registro"] == tipo]
    if nombre_search:
        resultado = [u for u in resultado if nombre_search.lower() in u["nombre"].lower()]
    return resultado


@app.get("/usuarios/{id_usuario}/{correo_verif}")
def buscar_usuario_especifico(
    id_usuario: int = Path(..., gt=0),
    correo_verif: str = Path(...)
):
    """Busca un usuario por su ID y verifica si su correo coincide."""
    for u in db_usuarios:
        if u["id_usuario"] == id_usuario and u["correo"] == correo_verif:
            return u
    raise HTTPException(status_code=404, detail="Usuario no encontrado o correo no coincide")


@app.get("/cursos")
def filtrar_cursos(
    min_h: int = Query(0, ge=0),
    max_h: int = Query(200, le=200)
):
    """Lista cursos filtrando por un rango de intensidad horaria."""
    return [c for c in db_cursos if min_h <= c["intensidad_horaria"] <= max_h]

@app.get("/cursos/{id_curso}/{nombre_slug}")
def detalle_curso(
    id_curso: int = Path(..., ge=1),
    nombre_slug: str = Path(...)
):
    """Obtiene detalles de un curso usando su ID y un nombre simplificado (slug)."""
    for c in db_cursos:
        if c["id_curso"] == id_curso:
            return c
    raise HTTPException(status_code=404, detail="Curso no encontrado")



@app.put("/alertas/{id_alerta}")
def modificar_alerta(
    id_alerta: int = Path(..., title="ID de la alerta"),
    nuevo_estado: str = Query(..., regex="^(pendiente|enviada|vencida)$")
):
    """Actualiza el estado de una alerta mediante su ID y un estado válido por query."""
    for al in db_alertas:
        if al["id_alerta"] == id_alerta:
            al["estado"] = nuevo_estado
            return {"mensaje": "Alerta actualizada", "alerta": al}
    raise HTTPException(status_code=404, detail="Alerta no encontrada")


@app.post("/usuarios")
def crear_usuario(usuario: Usuario):
    """Registra un nuevo usuario validando los campos del modelo."""
    db_usuarios.append(usuario.dict())
    return {"mensaje": "Usuario registrado", "usuario": usuario}

@app.delete("/usuarios/{id_usuario}")
def eliminar_usuario(id_usuario: int = Path(..., gt=0)):
    """Elimina un usuario por su ID dinámico."""
    for index, u in enumerate(db_usuarios):
        if u["id_usuario"] == id_usuario:
            db_usuarios.pop(index)
            return {"mensaje": "Usuario eliminado"}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")
