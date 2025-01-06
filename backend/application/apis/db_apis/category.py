import ast
from flask import request
from flask_restful import Resource, reqparse

from application.model.model import db, Category
from application.model.utils import parser_from_model,recursive_parser,to_dict

root_parser = reqparse.RequestParser(bundle_errors=True)
root_parser.add_argument("data", type=dict)

get_id_parser = reqparse.RequestParser(bundle_errors=True)
get_id_parser.add_argument("id", type=int, required=True, location=("data",))


parser = parser_from_model(Category)
put_parser = parser_from_model(Category, method="PUT")
patch_parser = parser_from_model(Category, method="PATCH")

class CategoryResource(Resource):
    def get(self):
        args = get_id_parser.parse_args(req=root_parser.parse_args())
        category_id = args.pop("id")
        category = Category.query.get(category_id)
        
        if not category:
            return {"message": "Category not found"}, 404
        
        return {
            "data": recursive_parser(to_dict(category))
        },200
        
    def post(self):
        args = parser.parse_args(req=root_parser.parse_args())
        category = Category(**args)
        
        try:
            db.session.add(category)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return {
                "data": {"message":"category not created"},
            }
        return {
            "data": recursive_parser(to_dict(category))
        },201
        
    
    def put(self):
        request_data = request.get_json()
        data = request_data.get('data', {})

        if 'customised_risk_set' in data and not isinstance(data['customised_risk_set'], list):
            try:
                data['customised_risk_set'] = ast.literal_eval(data['customised_risk_set'])
            except (ValueError, SyntaxError):
                return {
                "data": {"message":"category not found"}
            },400

        try:
            category = Category.query.get(data['id'])
            if not category:
                return {
                "data": {"message":"category not found"}
            },404

            for key, value in data.items():
                setattr(category, key, value)

            db.session.commit()
            return {
                "data": recursive_parser(to_dict(category))
            },200
        except Exception as e:
            db.session.rollback()
            return {
                "data": {"message":"category not updated"}
            }
            
           
        
    def patch(self):
        request_data = request.get_json()
        data = request_data.get('data', {})
        if 'customised_risk_set' in data and not isinstance(data['customised_risk_set'], list):
            try:
                data['customised_risk_set'] = ast.literal_eval(data['customised_risk_set'])
            except (ValueError, SyntaxError):
                return {
                "data": {"message":"category not found"}
            },400

        try:
            category = Category.query.get(data['id'])
            if not category:
                return {
                "data": {"message":"category not found"}
            },404

            for key, value in data.items():
                if value is not None:
                    setattr(category, key, value)

            db.session.commit()
            return {
                "data": recursive_parser(to_dict(category))
            },200
        except Exception as e:
            db.session.rollback()
            return {
                "data": {"message":"category not updated"}
            }
        
       
        
        
class CategorysResource(Resource):
    def get(self):
        categorys = Category.query.all()
        return {
            "data": [recursive_parser(to_dict(category)) for category in categorys]
        },200