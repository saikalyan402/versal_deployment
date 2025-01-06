from flask_restful import reqparse, Resource

from application.model.model import (
    db,
    User,
    UserRole,
    Role,
    UserCategoryAccess,
    Category,
)
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity
from application.apis.helper_fun import is_admin
from datetime import datetime


# Define the argument parser
user_post_args = reqparse.RequestParser()
user_post_args.add_argument(
    "name", type=str, required=True, help="User name is required"
)
user_post_args.add_argument(
    "email", type=str, required=True, help="User mail is required"
)
user_post_args.add_argument(
    "password", type=str, required=True, help="Password is required"
)
user_post_args.add_argument("role", type=str, required=True, help="Role is required")
user_post_args.add_argument(
    "category_access",
    type=list,
    location="json",
    required=True,
    help="Category access is required",
)


class UserRegister(Resource):
    @jwt_required()
    def post(self):
        logined_user_id = get_jwt_identity()
        if is_admin(logined_user_id) == False:
            return {"status":"failed","message":"Only admin can access this"}
        args = user_post_args.parse_args()
        name = args.get("name")
        email = args.get("email")
        password = args.get("password")
        role_code = args.get("role")
        category_access_list = args.get("category_access")
        if email == '':
            return {"status":"failed","message": "Email cannot be empty"},200
        
        if '@' not in email:
            return {"status":"failed","message": "Email is invalid"},200
        
        email = email.lower()
        email_sufix = email.split('@')[1]
        if email_sufix != 'adityabirlacapital.com':
            return {"status":"failed","message": "Only adityabirlacapital mail is allowed"},200
        
        if password == '':
            return {"status":"failed","message": "Password cannot be empty"},200
        if password == 'password':
            return {"status":"failed","message": "Password cannot be password"},200
        if len(password) < 8:
            return {"status":"failed","message": "Password must be atleast 8 characters long"},200
        if not any(char.isdigit() for char in password):
            return {"status":"failed","message": "Password must have atleast one digit"},200
        if not any(char.isupper() for char in password):
            return {"status":"failed","message": "Password must have atleast one uppercase letter"},200
        if not any(char.islower() for char in password):
            return {"status":"failed","message": "Password must have atleast one lowercase letter"},200
        
        
        if not isinstance(category_access_list, list) or not all(
            isinstance(item, str) for item in category_access_list
        ):
            return {"status":"failed","message": "category_access must be a list of strings"}, 200
        user = User.query.filter_by(email=email).first()
        if user:
            return {"status":"failed","message": "Mail is already registered !!"},200
        role = Role.query.filter_by(code=role_code).first()
        if role is None:
            return {"status":"failed","message": "role doesn't exist"},200
        user_role = (
            UserRole.query.join(User, UserRole.user_id == User.id)
            .join(Role, UserRole.role_id == Role.id)
            .filter(User.email == email)
            .filter(Role.code == role_code)
            .first()
        )
        
        if user_role:
            return {"status":"failed","message":"User already has this role"},200

        for category_access in category_access_list:
            category = Category.query.filter_by(name=category_access).first()
            if category is None:
                return {"status":"failed","message": f"category is doesn't exist {category_access}"},200
        hash_password = generate_password_hash(password)
        new_user = User(name=name,email=email, password=hash_password, last_login_at = datetime.now())

        try:
            with db.session.begin_nested():
                db.session.add(new_user)
                db.session.flush()  # Ensure new_user.id is available

                new_user_role = UserRole(user_id=new_user.id, role_id=role.id)
                db.session.add(new_user_role)

                for category_access in category_access_list:
                    category = Category.query.filter_by(name=category_access).first()
                    user_category_access = UserCategoryAccess(user_id=new_user.id, category_id=category.id)
                    db.session.add(user_category_access)

            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return {"status":"failed","message": "Encountered an error while adding user and related data"},200

        return {
            "status": "success",
            "message": "User Added Successfully"
        },200