from bson import ObjectId


def convert_objectid(data):
    if isinstance(data, list):
        return [convert_objectid(item) for item in data]
    elif isinstance(data, dict):
        return {key: convert_objectid(value) for key, value in data.items()}
    elif isinstance(data, ObjectId):
        return str(data)
    else:
        return data


def order_schemas(order) -> dict:
    return {"id": order["_id"],
            "id_user": order["id_user"],
            "id_products": order["id_products"]
            }



def orders_schemas(orders) -> list:
    return [order_schemas(order) for order in orders]