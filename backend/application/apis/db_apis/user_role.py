from flask import request
from flask_restful import Resource, reqparse

from sqlalchemy.exc import IntegrityError

from application.model.model import db, UserRole,User,Role
from application.model.utils import parser_from_model,recursive_parser,to_dict


root_parser = reqparse.RequestParser(bundle_errors=True)
root_parser.add_argument("meta", type=dict)
root_parser.add_argument("data", type=dict)

get_id_parser = reqparse.RequestParser(bundle_errors=True)
get_id_parser.add_argument("id", type=int, required=True, location=("data",))


parser = parser_from_model(UserRole)
put_parser = parser_from_model(UserRole, method="PUT")
patch_parser = parser_from_model(UserRole, method="PATCH")


class UserRoleResource(Resource):
    def get(self):
        args = get_id_parser.parse_args(req=root_parser.parse_args())
        user_role_id = args.pop("id")
        user_role = UserRole.query.get(user_role_id)

        if not user_role:
            return {
                "meta": {"version": "v1", "status": "error"},
                "data": {"message": "UserRole not found"},
            }, 404

        user = User.query.get(user_role.user_id)
        role = Role.query.get(user_role.role_id)

        return {
            "meta": {"version": "v1", "status": "success"},
            "data": recursive_parser(
                {
                    **to_dict(user_role),
                    "related_entities": {
                        "user": [to_dict(user)],
                        "role": [to_dict(role)],
                    },
                }
            ),
        }
        
        
            
    def post(self):
        args = parser.parse_args(req=root_parser.parse_args())
        user_role = UserRole(**args)

        user = User.query.get(user_role.user_id)
        if user is None:
            return {
                "meta": {"version": "v1", "status": "error"},
                "data": {"message": "User not found"},
            }, 404

        role = Role.query.get(user_role.role_id)
        if role is None:
            return {
                "meta": {"version": "v1", "status": "error"},
                "data": {"message": "Role not found"},
            }, 404

        if UserRole.query.filter_by(
            user_id=user_role.user_id, role_id=user_role.role_id
        ).first():
            return {
                "meta": {"version": "v1", "status": "error"},
                "data": {"message": "UserRole already exists"},
            }, 409

        try:
            db.session.add(user_role)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return {
                "data": {"message": "UserRole not created"},
            }, 500

        return {
            "meta": {"version": "v1", "status": "success"},
            "data": recursive_parser(
                {
                    **to_dict(user_role),
                    "related_entities": {
                        "user": [to_dict(user)],
                        "role": [to_dict(role)],
                    },
                }
            ),
        }, 201

    def put(self):
        args = put_parser.parse_args(req=root_parser.parse_args())
        user_role_id = args.get("id")
        user_role = UserRole.query.get(user_role_id)
        if not user_role:
            return {
                "meta": {"version": "v1", "status": "error"},
                "data": {"message": "UserRole not found"},
            }, 404
            
        if args.get("user_id"):
            user = User.query.get(user_role.user_id)
            if user is None:
                return {
                    "meta": {"version": "v1", "status": "error"},
                    "data": {"message": "User not found"},
                }, 404
        if args.get("role_id"):
            role = Role.query.get(user_role.role_id)
            if role is None:
                return {
                    "meta": {"version": "v1", "status": "error"},
                    "data": {"message": "Role not found"},
                }, 404

        if UserRole.query.filter_by(
            user_id=user_role.user_id, role_id=user_role.role_id
        ).first():
            return {
                "meta": {"version": "v1", "status": "error"},
                "data": {"message": "UserRole already exists"},
            }, 409

        user = User.query.get(user_role.user_id)
        role = Role.query.get(user_role.role_id)

        for key, value in args.items():
            setattr(user_role, key, value)

        try:
            db.session.commit()

        except Exception as e:
            print(e)
            db.session.rollback()
            return {
                "data": {"message":"user not updated"},
            }
            

        return {
            "meta": {"version": "v1", "status": "success"},
            "data": recursive_parser(
                {
                    **to_dict(user_role),
                    "related_entities": {
                        "user": [to_dict(user)],
                        "role": [to_dict(role)],
                    },
                }
            ),
        }

    def patch(self):
        args = patch_parser.parse_args(req=root_parser.parse_args())
        user_role_id = args.pop("id")
        user_role = UserRole.query.get(user_role_id)

        if not user_role:
            return {
                "meta": {"version": "v1", "status": "error"},
                "data": {"message": "UserRole not found"},
            }, 404

        if user := User.query.get(user_role.user_id) is None:
            return {
                "meta": {"version": "v1", "status": "error"},
                "data": {"message": "User not found"},
            }, 404

        if role := Role.query.get(user_role.role_id) is None:
            return {
                "meta": {"version": "v1", "status": "error"},
                "data": {"message": "Role not found"},
            }, 404

        for key, value in args.items():
            if value is not None:
                setattr(user_role, key, value)

        try:
            db.session.commit()

        except Exception as e:
            print(e)
            db.session.rollback()
            return {
                "data": {"message":"user not updated"},
            }
            

        return {
            "meta": {"version": "v1", "status": "success"},
            "data": recursive_parser(
                {
                    **to_dict(user_role),
                    "related_entities": {
                        "user": [to_dict(user)],
                        "role": [to_dict(role)],
                    },
                }
            ),
        }


class UserRolesResource(Resource):
    def get(self):
        query = UserRole.query
        for key, value in request.args.items():
            if hasattr(UserRole, key):
                query = query.filter(getattr(UserRole, key) == value)
        user_roles = query.paginate()
        return {
            "meta": {"version": "v1", "status": "success"},
            "data": {
                "items": [
                    recursive_parser(to_dict(user_role)) for user_role in user_roles
                ]
            },
        }
