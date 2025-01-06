from flask import request
from flask_restful import Resource, reqparse

from application.model.model import db, Company
from application.model.utils import parser_from_model,recursive_parser,to_dict

root_parser = reqparse.RequestParser(bundle_errors=True)
root_parser.add_argument("data", type=dict)

get_id_parser = reqparse.RequestParser(bundle_errors=True)
get_id_parser.add_argument("id", type=int, required=True, location=("data",))


parser = parser_from_model(Company)
put_parser = parser_from_model(Company, method="PUT")
patch_parser = parser_from_model(Company, method="PATCH")

class CompanyResource(Resource):
    def get(self):
        args = get_id_parser.parse_args(req=root_parser.parse_args())
        company_id = args.pop("id")
        company = Company.query.get(company_id)
        
        if not company:
            return {"message": "Company not found"}, 404
        
        return {
            "data": recursive_parser(to_dict(company))
        },200
        
    def post(self):
        args = parser.parse_args(req=root_parser.parse_args())
        company = Company(**args)
        
        try:
            db.session.add(company)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return {
                "data": {"message":"company not created"},
            }
        return {
            "data": recursive_parser(to_dict(company))
        },201
        
    
    def put(self):
        args = put_parser.parse_args(req=root_parser.parse_args())
        company_id = args.pop("id",None)
        if company_id is None:
            return {"message": "Company id is required"}, 400
        
        company = Company.query.filter_by(id=company_id).first()
        
        if not company:
            return {"message": "Company not found"}, 404
        
        for key, value in args.items():
            setattr(company, key, value)
            
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return{
                "data": {"message":"company not updated"}
            }
        
        
        
        return {
            "data": recursive_parser(to_dict(company))
        },200
        
        
    def patch(self):
        args = patch_parser.parse_args(req=root_parser.parse_args())
        company_id = args.pop("id")
        company = Company.query.get(company_id)
        
        if not company:
            return {"message": "Company not found"}, 404
        
        for key, value in args.items():
            if value is not None:
                setattr(company, key, value)
        
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return{
                "data": {"message":"company not updated"}
            }
        
        return {
            "data": recursive_parser(to_dict(company))
        },200        
        
        
        
class CompanysResource(Resource):
    def get(self):
        companys = Company.query.all()
        return {
            "data": [recursive_parser(to_dict(company)) for company in companys]
        },200