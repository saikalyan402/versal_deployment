from application.model.model import db, User, Category, UserCategoryAccess,Role,UserRole


from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from application.apis.helper_fun import is_admin


class AllUser(Resource):
    @jwt_required()
    def get(self):
        logined_user_id = get_jwt_identity()
        if is_admin(logined_user_id) == False:
            return {"status":"failed","message":"Only admin can access this"},200
        users = User.query.filter_by(active = True).all()
        user_list = []
        for user in users:
            user_role = UserRole.query.filter_by(user_id=user.id).first()
            role = Role.query.filter_by(id=user_role.role_id).first()
            users_category_access = UserCategoryAccess.query.filter_by(user_id=user.id).all()
            categorys = []
            for access in users_category_access:
                category = Category.query.filter_by(id=access.category_id).first()
                categorys.append(category.name)
            user_list.append(
                {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "roles": role.code,
                    "category_access": categorys,
                }
            )
        return {"status": "success", "data": user_list}, 200