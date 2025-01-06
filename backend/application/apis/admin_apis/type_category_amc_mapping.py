from application.model.model import db, User, Category, UserCategoryAccess,Role,Company, Scheme

from flask_restful import Resource
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from application.apis.helper_fun import is_admin


class TypeCategoryAmcMappingAPI(Resource):
    @jwt_required()
    def get(self):
        current_user_id =  get_jwt_identity()
        if is_admin(current_user_id) == False:
            return {"status":"failed","message":"Only admin can access this"},200
        


        user_cat_access = UserCategoryAccess.query.filter_by(user_id = current_user_id).all()
        user_category_ids =[]
        for cat in user_cat_access:
            user_category_ids.append(cat.category_id)
        
        
        type_category_amc_mapping = {}
        
        schemes = Scheme.query.all()
        for scheme in schemes:
            if scheme.category_id in user_category_ids:
                if scheme.type not in type_category_amc_mapping.keys():
                    type_category_amc_mapping[scheme.type] = {}
                category_name = Category.query.filter_by(id = scheme.category_id).first().name
                if category_name not in type_category_amc_mapping[scheme.type]:
                    type_category_amc_mapping[scheme.type][category_name] = []
                company_name = Company.query.filter_by(id = scheme.company_id).first().name
                if (company_name not in type_category_amc_mapping[scheme.type][category_name]) and (company_name != "ABSL") :
                    type_category_amc_mapping[scheme.type][category_name].append(company_name)

            
        data ={
            "type_category_amc_mapping":type_category_amc_mapping,
        }
        return {"status": "success", "data": data}, 200
