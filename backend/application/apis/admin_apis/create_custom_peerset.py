from flask import jsonify

from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from application.model.model import db, Scheme, Category, Company
from application.apis.helper_fun import is_admin
from flask import jsonify


create_custom_peer = reqparse.RequestParser()
create_custom_peer.add_argument(
    "type",
    type=str,
    required=True,
    help="Type is required",
)
create_custom_peer.add_argument(
    "category",
    type=str,
    required=True,
    help="category is required",
)
create_custom_peer.add_argument(
    "amcs",
    type=list,
    location="json",
    required=True,
    help="amcs list is required"
)


class CreateCustomPeerRistSet(Resource):
    @jwt_required()
    def post(self):
        logined_user_id = get_jwt_identity()
        if is_admin(logined_user_id) == False:
            return {"status": "failed", "message": "Only admin can access this"}

        args = create_custom_peer.parse_args()
        type = args.get("type")
        category = args.get("category")
        amcs = args.get("amcs")


        category = Category.query.filter_by(name=category).first()

        if category is None:
            return {"status": "failed", "message": "category not found"}

        rist_set = []

        for amc in amcs:
            company = Company.query.filter_by(name=amc).first()
            if company:
                rist_set.append(company.id)

        category.customised_risk_set = rist_set
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            return {"status": "failed", "message": "error while adding"}

        return {"status": "success", "message": "PeerSet Created"}
