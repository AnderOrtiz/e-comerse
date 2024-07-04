def user_schemas(user) -> dict:
    return {"id": str(user["_id"]),
            "name": user["name"],
            "last_name": user["last_name"],
            "email": user["email"],
            "password": user["password"],
            "gender": user["gender"],
            "age": user["age"],
            }



def users_schemas(users) -> list:
    return [user_schemas(user) for user in users]