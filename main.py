import uvicorn
from fastapi import FastAPI
from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from typing import List, Optional

app = FastAPI()

# Definir un diccionario vacío para almacenar los usuarios
users_db = {}

@app.get("/")
def hello_world():
    return {"message": "Hecho por Manuel y Emiliano"}

class UserCreate(BaseModel):
    user_name: str
    user_id: int
    user_email: str
    age: Optional[int] = None
    recommendations: List[str] = []
    ZIP: Optional[str] = None

# Endpoint para crear un usuario
@app.post("/create_user")
async def create_user(user: UserCreate):
    user_id = user.user_id

    # Verificar si el usuario ya existe en la base de datos
    if user_id in users_db:
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    # Agregar el usuario al diccionario
    users_db[user_id] = user.dict()

    return {"message": "Usuario creado exitosamente", "user_id": user_id}


# Endpoint para actualizar un usuario por ID
@app.put("/update_user/{user_id}")
async def update_user(user_id: int, updated_user: UserCreate):
    # Verificar si el usuario existe en la base de datos
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Actualizar la información del usuario
    users_db[user_id] = updated_user.dict()

    return {"message": "Usuario actualizado exitosamente", "user_id": user_id}


# Endpoint para obtener la información de un usuario por ID
@app.get("/get_user/{user_id}")
async def get_user(user_id: int):
    # Verificar si el usuario existe en la base de datos
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Obtener la información del usuario
    user_info = users_db[user_id]

    return user_info


# Endpoint para eliminar un usuario por ID
@app.delete("/delete_user/{user_id}")
async def delete_user(user_id: int):
    # Verificar si el usuario existe en la base de datos
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Eliminar al usuario de la base de datos
    del users_db[user_id]

    return {"message": "Usuario eliminado exitosamente", "user_id": user_id}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5031, log_level="info", reload=False)
