from application.model.model import db, User, Category, UserCategoryAccess,Role,Company, Scheme

from flask_restful import Resource
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from application.apis.helper_fun import get_all_the_dates

class CategoryOverviewAccessData(Resource):
    @jwt_required()
    def get(self):
        current_user =  get_jwt_identity()
        current_user_id = current_user


        user_cat_access = UserCategoryAccess.query.filter_by(user_id = current_user_id).all()
        user_category_ids =[]
        for cat in user_cat_access:
            user_category_ids.append(cat.category_id)
        
        
        subtype_type_categ_mapping ={}
        
        schemes = Scheme.query.all()
        for scheme in schemes:
            if scheme.category_id in user_category_ids:
                if scheme.subtype not in subtype_type_categ_mapping.keys():
                    subtype_type_categ_mapping[scheme.subtype] = {}
                if scheme.type not in subtype_type_categ_mapping[scheme.subtype].keys():
                    subtype_type_categ_mapping[scheme.subtype][scheme.type] = []
                    
                category = Category.query.filter_by(id = scheme.category_id).first()
                if category.name not in subtype_type_categ_mapping[scheme.subtype][scheme.type]:
                    subtype_type_categ_mapping[scheme.subtype][scheme.type].append(category.name)

        data ={
            "subtype_type_categ_mapping": subtype_type_categ_mapping,
            "all_dates":get_all_the_dates()
        }
        return {"status": "success", "data": data}, 200
