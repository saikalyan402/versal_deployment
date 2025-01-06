from flask import jsonify
from flask_restful import Resource, reqparse
from datetime import datetime
from flask_security import login_user
from flask_security.utils import verify_password, hash_password
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
)
from werkzeug.security import check_password_hash
from application.model.model import db, User, UserRole, Role, Permission, RolePermission

# from application.security import user_datastore
# -------------------------------
import json

parser = reqparse.RequestParser()
parser.add_argument("email", type=str, required=True, help="user_mail is required !!")
parser.add_argument("password", type=str, required=True, help="Password is required !!")


class UserLogin(Resource):
    def post(self):
        args = parser.parse_args()
        email = args.get("email")
        password = args.get("password")

        user = User.query.filter_by(email=email).first()

        if user is None:
            return jsonify({"status": "failed", "message": "User doesn't exist !!"})
        if not check_password_hash(user.password, password):
            return jsonify({"status": "failed", "message": "Invalid email or password"})
        if not user.active:
            return jsonify({"status": "failed", "message": "User is not active !!"})

        if user.is_deleted:
            return jsonify({"status": "failed", "message": "User is deleted !!"})

        access_token = create_access_token(identity=user.id)

        login_user(user)
        user_permissions = (
            User.query.join(UserRole, User.id == UserRole.user_id)
            .join(Role, UserRole.role_id == Role.id)
            .join(RolePermission, Role.id == RolePermission.role_id)
            .join(Permission, RolePermission.permission_id == Permission.id)
            .filter(User.id == user.id)
            .add_column(Permission.name)
            .all()
        )

        pages = []
        if user_permissions:
            for permission in user_permissions:
                pages.append(permission[1])
                
        try:
            user.last_login_at = datetime.now()
            if user.no_of_logins is None:
                user.no_of_logins = 0
            user.no_of_logins += 1
            db.session.commit()
        except Exception as e:
            print(e)
            return jsonify({"status": "failed", "message": "Error while updating user login details !!"})

        return jsonify(
            {
                "status": "success",
                "message": "Successfully logged in !!",
                "access_token": access_token,
                "email": user.email,
                "pages": pages,
                "username": user.name,
            }
        )


def page_url_mapping(pages):
    all_page_mapping = {
        "Home": "/home",
        "Scheme Comparison": "/schemeComp",
        "AMC Overview": "/amc_overview",
        "Category Overview": "/catOverview",
        "Admin Dashboard": "/ManageDashboard",
        "Edge" : "/edge"
    }
    user_page_mapping = {}
    for page in pages:
        user_page_mapping[page] = all_page_mapping[page]

    return user_page_mapping
