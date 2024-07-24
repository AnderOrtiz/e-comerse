from bson import ObjectId

def user_schemas(user) -> dict:
    if not user:
        raise ValueError("User is None")
    return {"id": str(user["_id"]),
            "name": user["name"],
            "last_name": user["last_name"],
            "email": user["email"],
            "gender": user["gender"],
            "age": user["age"],
            "car": list(user["car"]),  # Convertir ObjectId a string
            "password": user["password"],
            }

def users_schemas(users) -> list:
    return [user_schemas(user) for user in users]

def convert_objectid(data):
    if isinstance(data, list):
        return [convert_objectid(item) for item in data]
    elif isinstance(data, dict):
        return {key: convert_objectid(value) for key, value in data.items()}
    elif isinstance(data, ObjectId):
        return str(data)
    else:
        return data