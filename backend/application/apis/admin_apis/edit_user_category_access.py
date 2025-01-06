from application.model.model import db, User, Category, UserCategoryAccess,UserRole,Role

from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from application.apis.helper_fun import is_admin

user_category_access_post_args = reqparse.RequestParser()
user_category_access_post_args.add_argument(
    "email", type=str, required=True, help="User mail is required"
)
user_category_access_post_args.add_argument(
    "role",
    type=str,
    location="json",
    required=True,
    help="Role is required",
)
user_category_access_post_args.add_argument(
    "category_access",
    type=list,
    required=True,
    location="json",
    help="Category access is required",
)

class UserRoleAndCategoryAccessChange(Resource):
    @jwt_required()
    def post(self):
        logined_user_id = get_jwt_identity()
        if is_admin(logined_user_id) == False:
            return {"status":"failed","message":"Only admin can access this"},200
        args = user_category_access_post_args.parse_args()
        email = args.get("email")
        category_access_list = args.get("category_access")
        role = args.get("role")
        
        user = User.query.filter_by(email=email).first()
        if user is None:
            return {"status": "failed", "message": "User not found"}, 200
        
        
        role = Role.query.filter_by(code=role).first()
        
        if role is None:
            return ({"status": "failed", "message": "Role not found"}, 200)
        
        user_role = UserRole.query.filter_by(user_id = user.id).filter_by(role_id = role.id).first()
        role_change = False
        
        if user_role is None:
            alreay_has_role = UserRole.query.filter_by(user_id = user.id).first()
            if alreay_has_role:
                db.session.delete(alreay_has_role)
                try:
                    db.session.commit()
                except Exception as e:
                    return {"status": "failed", "message": "Not able to update role, See Logs"},200
            
            new_user_role = UserRole(user_id = user.id, role_id = role.id)
            try:
                db.session.add(new_user_role)
                db.session.commit()
                role_change = True
            except Exception as e:
                return {"status": "failed", "message": "Not able to update role, See Logs"},200
            
            
        
    
        users_category_access = UserCategoryAccess.query.filter_by(user_id = user.id).all()

        for access in users_category_access:
            db.session.delete(access)
            try:
                db.session.commit()
            except Exception as e:
                return {"status": "failed", "message": "Not able to update category access, See Logs"},200
        
            
        for category_name in category_access_list:
            category = Category.query.filter_by(name=category_name).first()
            if category is None:
                return {"status": "failed", "message": "Category not found"}, 200
            
            user_category_access = UserCategoryAccess(
                user_id=user.id, category_id=category.id
            )
            db.session.add(user_category_access)
        
        try:
            db.session.commit()
            if role_change:
                return {"status": "success", "message": "Role and Category access updated successfully"}, 200
            else:
                return {"status": "success", "message": "Category access updated successfully, Role not changed"}, 200
        except Exception as e:
            return {"status": "failed", "message": "Category access update failed"}, 200