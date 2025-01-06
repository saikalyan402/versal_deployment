from application.model.model import db, User

from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity
from application.apis.helper_fun import is_admin

user_password_change_post_args = reqparse.RequestParser()
user_password_change_post_args.add_argument(
    "email", type=str, required=True, help="User mail is required"
)
user_password_change_post_args.add_argument(
    "password", type=str, required=True, help="Password is required"
)

class UserPasswordChange(Resource):
    @jwt_required()
    def post(self):
        logined_user_id = get_jwt_identity()
        if is_admin(logined_user_id) == False:
            return {"status":"failed","message":"Only admin can access this"},200
        args = user_password_change_post_args.parse_args()
        email = args.get("email")
        password = args.get("password")
        
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
        
        
        user = User.query.filter_by(email=email).first()
        if user is None:
            return {"status": "failed", "message": "User not found"}, 400
        hash_password = generate_password_hash(password)
        user.password = hash_password
        try:
            db.session.commit()
            return {"status": "success", "message": "Password updated successfully"}, 200
        except Exception as e:
            return {"status": "failed", "message": "Password update failed"}, 400