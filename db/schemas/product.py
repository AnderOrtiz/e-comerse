def product_schemas(product) -> dict:
    return {"id": str(product["_id"]),
            "name": product["name"],
            "price": product["price"],
            "detail": product["detail"],
            "car": product["car"],
            }



def products_schemas(users) -> list:
    return [product_schemas(user) for user in users]