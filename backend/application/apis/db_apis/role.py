from flask import request
from flask_restful import Resource, reqparse

from application.model.model import db, Role
from application.model.utils import parser_from_model,recursive_parser,to_dict

root_parser = reqparse.RequestParser(bundle_errors=True)
root_parser.add_argument("data", type=dict)

get_id_parser = reqparse.RequestParser(bundle_errors=True)
get_id_parser.add_argument("id", type=int, required=True, location=("data",))


parser = parser_from_model(Role)
put_parser = parser_from_model(Role, method="PUT")
patch_parser = parser_from_model(Role, method="PATCH")

class RoleResource(Resource):
    def get(self):
        args = get_id_parser.parse_args(req=root_parser.parse_args())
        role_id = args.pop("id")
        role = Role.query.get(role_id)
        
        if not role:
            return {"message": "Role not found"}, 404
        
        return {
            "data": recursive_parser(to_dict(role))
        },200
        
    def post(self):
        args = parser.parse_args(req=root_parser.parse_args())
        role = Role(**args)
        
        try:
            db.session.add(role)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {
                "data": {"message":"role not created"},
            }
        return {
            "data": recursive_parser(to_dict(role))
        },201
        
    
    def put(self):
        args = put_parser.parse_args(req=root_parser.parse_args())
        role_id = args.pop("id",None)
        if role_id is None:
            return {"message": "Role id is required"}, 400
        
        role = Role.query.filter_by(id=role_id).first()
        
        if not role:
            return {"message": "Role not found"}, 404
        
        for key, value in args.items():
            setattr(role, key, value)
            
        try:
            db.session.commit()  
        except Exception as e:
            print(e)
            db.session.rollback()
            return {
                "data": {"message":"role not updated"}
            }
            
        
        
        
        return {
            "data": recursive_parser(to_dict(role))
        },200
        
        
    def patch(self):
        args = patch_parser.parse_args(req=root_parser.parse_args())
        role_id = args.pop("id")
        role = Role.query.get(role_id)
        
        if not role:
            return {"message": "Role not found"}, 404
        
        for key, value in args.items():
            if value is not None:
                setattr(role, key, value)
        
        try:
            db.session.commit()  
        except Exception as e:
            print(e)
            db.session.rollback()
            return {
                "data": {"message":"role not updated"}
            }
        
        return {
            "data": recursive_parser(to_dict(role))
        },200        
        
        
        
class RolesResource(Resource):
    def get(self):
        roles = Role.query.all()
        return {
            "data": [recursive_parser(to_dict(role)) for role in roles]
        },200