from flask import request
from flask_restful import Resource, reqparse

from application.model.model import db, Permission
from application.model.utils import parser_from_model,recursive_parser,to_dict

root_parser = reqparse.RequestParser(bundle_errors=True)
root_parser.add_argument("data", type=dict)

get_id_parser = reqparse.RequestParser(bundle_errors=True)
get_id_parser.add_argument("id", type=int, required=True, location=("data",))


parser = parser_from_model(Permission)
put_parser = parser_from_model(Permission, method="PUT")
patch_parser = parser_from_model(Permission, method="PATCH")

class PermissionResource(Resource):
    def get(self):
        args = get_id_parser.parse_args(req=root_parser.parse_args())
        permission_id = args.pop("id")
        permission = Permission.query.get(permission_id)
        
        if not permission:
            return {"message": "Permission not found"}, 404
        
        return {
            "data": recursive_parser(to_dict(permission))
        },200
        
    def post(self):
        args = parser.parse_args(req=root_parser.parse_args())
        permission = Permission(**args)
        
        try:
            db.session.add(permission)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {
                "data": {"message":"permission not created"},
            }
        return {
            "data": recursive_parser(to_dict(permission))
        },201
        
    
    def put(self):
        args = put_parser.parse_args(req=root_parser.parse_args())
        permission_id = args.pop("id",None)
        if permission_id is None:
            return {"message": "Permission id is required"}, 400
        
        permission = Permission.query.filter_by(id=permission_id).first()
        
        if not permission:
            return {"message": "Permission not found"}, 404
        
        for key, value in args.items():
            setattr(permission, key, value)
            
        try:
            db.session.commit()  
        except Exception as e:
            print(e)
            db.session.rollback()
            return {
                "data": {"message":"permission not updated"}
            }
            
        
        
        
        return {
            "data": recursive_parser(to_dict(permission))
        },200
        
        
    def patch(self):
        args = patch_parser.parse_args(req=root_parser.parse_args())
        permission_id = args.pop("id")
        permission = Permission.query.get(permission_id)
        
        if not permission:
            return {"message": "Permission not found"}, 404
        
        for key, value in args.items():
            if value is not None:
                setattr(permission, key, value)
        
        try:
            db.session.commit()  
        except Exception as e:
            print(e)
            db.session.rollback()
            return {
                "data": {"message":"permission not updated"}
            }
        
        return {
            "data": recursive_parser(to_dict(permission))
        },200        
        
        
        
class PermissionsResource(Resource):
    def get(self):
        permissions = Permission.query.all()
        return {
            "data": [recursive_parser(to_dict(permission)) for permission in permissions]
        },200