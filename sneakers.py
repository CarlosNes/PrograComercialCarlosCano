import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

class SolicitudSneaker(BaseModel):
    modelo: str
    talla: float
    marca: str

@app.post('/sneakers/')
def registrar_sneaker(solicitud: SolicitudSneaker):
    try:
        with open('inventario.json', 'r') as f:
            inventario = json.load(f)
    except FileNotFoundError:
        inventario = {}

    marca = solicitud.marca
    modelo = solicitud.modelo
    talla = str(solicitud.talla)

    if marca not in inventario:
        inventario[marca] = {}
    if modelo not in inventario[marca]:
        inventario[marca][modelo] = {}
    if talla not in inventario[marca][modelo]:
        inventario[marca][modelo][talla] = 0

    inventario[marca][modelo][talla] += 1

    with open('inventario.json', 'w') as f:
        json.dump(inventario, f)

    return {"mensaje": "Sneaker registrado exitosamente"}

@app.get('/sneakers/')
def consultar_disponibilidad(marca: str, modelo: str, talla: float):
    try:
        with open('inventario.json', 'r') as f:
            inventario = json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=400, detail="No hay inventario disponible")

    talla = str(talla)

    if marca not in inventario:
        raise HTTPException(status_code=400, detail="La marca no es válida")
    
    if modelo not in inventario[marca]:
        raise HTTPException(status_code=400, detail="El modelo no es válido para la marca especificada")

    if talla not in inventario[marca][modelo]:
        raise HTTPException(status_code=400, detail="La talla no está disponible para el modelo especificado")

    cantidad = inventario[marca][modelo][talla]
    
    return {"modelo": modelo, "talla": talla, "marca": marca, "cantidad_disponible": cantidad}

@app.get('/sneakers/todos/')
def mostrar_todos_sneakers():
    try:
        with open('inventario.json', 'r') as f:
            inventario = json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=400, detail="No hay inventario disponible")

    return inventario

# uvicorn sneakers:app --reload
