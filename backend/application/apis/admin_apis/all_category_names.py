from application.model.model import db, Category
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from application.apis.helper_fun import is_admin

class AllCategoryName(Resource):
    @jwt_required()
    def get(self):
        logined_user_id = get_jwt_identity()
        if is_admin(logined_user_id) == False:
            return {"status":"failed","message":"Only admin can access this"},200
        categorys = Category.query.all()
        category_names = []
        for category in categorys:
            category_names.append(category.name)
            
        return {"status": "success", "data": category_names}, 200