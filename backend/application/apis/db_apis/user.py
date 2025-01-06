from flask import request
from flask_restful import Resource, reqparse

from application.model.model import db, User
from application.model.utils import parser_from_model,recursive_parser,to_dict

root_parser = reqparse.RequestParser(bundle_errors=True)
root_parser.add_argument("data", type=dict)

get_id_parser = reqparse.RequestParser(bundle_errors=True)
get_id_parser.add_argument("id", type=int, required=True, location=("data",))


parser = parser_from_model(User)
put_parser = parser_from_model(User, method="PUT")
patch_parser = parser_from_model(User, method="PATCH")

class UserResource(Resource):
    def get(self):
        args = get_id_parser.parse_args(req=root_parser.parse_args())
        user_id = args.pop("id")
        user = User.query.get(user_id)
        
        if not user:
            return {"message": "User not found"}, 404
        
        return {
            "data": recursive_parser(to_dict(user))
        },200
        
    def post(self):
        args = parser.parse_args(req=root_parser.parse_args())
        user = User(**args)
        
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return {
                "data": {"message":"user not created"},
            }
        return {
            "data": recursive_parser(to_dict(user))
        },201
        
    
    def put(self):
        args = put_parser.parse_args(req=root_parser.parse_args())
        user_id = args.pop("id",None)
        if user_id is None:
            return {"message": "User id is required"}, 400
        
        user = User.query.filter_by(id=user_id).first()
        
        if not user:
            return {"message": "User not found"}, 404
        
        for key, value in args.items():
            setattr(user, key, value)
            
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return{
                "data": {"message":"user not updated"}
            }
        
        
        
        return {
            "data": recursive_parser(to_dict(user))
        },200
        
        
    def patch(self):
        args = patch_parser.parse_args(req=root_parser.parse_args())
        user_id = args.pop("id")
        user = User.query.get(user_id)
        
        if not user:
            return {"message": "User not found"}, 404
        
        for key, value in args.items():
            if value is not None:
                setattr(user, key, value)
        
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return{
                "data": {"message":"user not updated"}
            }
        
        return {
            "data": recursive_parser(to_dict(user))
        },200        
        
        
        
class UsersResource(Resource):
    def get(self):
        users = User.query.all()
        return {
            "data": [recursive_parser(to_dict(user)) for user in users]
        },200