from application.model.model import db, Company


from flask_jwt_extended import jwt_required,get_jwt_identity
from flask_restful import Resource
from application.apis.helper_fun import is_admin

class AllAmcNames(Resource):
    @jwt_required()
    def get(self):
        logined_user_id = get_jwt_identity()
        if is_admin(logined_user_id) == False:
            return {"status":"failed","message":"Only admin can access this"},200
        companys = Company.query.all()
        all_amc_names = []
        for company in companys:
            all_amc_names.append(company.name)
            
        return {"status": "success", "data": all_amc_names}, 200