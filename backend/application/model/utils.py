from datetime import datetime
from flask_restful import reqparse
import ast
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.types import PickleType



def recursive_parser(data):
    if isinstance(data, dict):
        return {key: recursive_parser(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [recursive_parser(value) for value in data]
    elif data.__class__.__name__ in ["int","float","str","bool","NoneType"]:
        return data
    else:
        return str(data)
    
def to_dict(model_instance):
    if not hasattr(model_instance, '__dict__'):
        raise ValueError(f"Expected a model instance, got {type(model_instance).__name__}")
    
    if model_instance and model_instance._sa_instance_state.expired:
        model_instance.id
    return {key: value for key, value in model_instance.__dict__.items() if not key.startswith("_")}


def find_column_type(column):
    try:
        if column.type.__class__.__name__ == "Time":
            return lambda x: datetime.strptime(x, "%H:%M:%S").time()
        if column.type.__class__.__name__ == "Date":
            return lambda x: datetime.strptime(x, "%Y-%m-%d").date()
        if isinstance(column.type, PickleType) and isinstance(column.type.impl, MutableList):
            return lambda x: ast.literal_eval(x) if isinstance(x, str) else x
        return column.type.python_type
    except:
        return str

def parser_from_model(model, exclude=None, method="POST"):
    parser = reqparse.RequestParser(bundle_errors=True)
    for column in model.__table__.columns:
        if exclude and column.name in exclude:
            continue
        if method == "POST" and column.primary_key:
            continue
        if column.name in ["created_at", "updated_at", "is_deleted"]:
            continue
        parser.add_argument(column.name, 
                            type=find_column_type(column),
                            required=(
                                False
                                if (method == "PATCH" and column.name != "id" or column.default)
                                else column.primary_key or not column.nullable
                            ),
                            location=("data",))
    return parser