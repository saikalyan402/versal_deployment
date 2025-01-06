from application.model.model import FundManagerCategoryConfig, Category
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from application.apis.helper_fun import is_admin, get_all_the_dates

class AllDates(Resource):
    @jwt_required()
    def get(self):
        logined_user_id = get_jwt_identity()
        if is_admin(logined_user_id) == False:
            return {"status":"failed","message":"Only admin can access this"},200
        all_dates = get_all_the_dates()
        return {"status": "success", "all_dates": all_dates}, 200