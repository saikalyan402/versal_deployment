from application.model.model import db, Role, Permission, RolePermission, Category, Scheme, Company

from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from application.apis.helper_fun import is_admin

class CategoryCustomRiskSetAPI(Resource):
    @jwt_required()
    def get(self):
        logined_user_id = get_jwt_identity()
        if is_admin(logined_user_id) == False:
            return {"status":"failed","message":"Only admin can access this"},200
        
        
        categories = Category.query.all()
        
        category_risk_sets = []
        
        for category in categories:
            if category.customised_risk_set != []:
                risk_amc_name = []
                for risk_id in category.customised_risk_set:
                    company_name = Company.query.filter_by(id = risk_id).first().name
                    risk_amc_name.append(company_name)
                    
                category_risk_sets.append({
                    "category": category.name,
                    "risk_amc_name": risk_amc_name
                })
            else:
                category_risk_sets.append({
                    "category": category.name,
                    "risk_amc_name": "No custom"
                })
        return {"status": "success", "data": category_risk_sets}, 200
        