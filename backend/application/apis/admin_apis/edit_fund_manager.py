from flask_restful import Resource,reqparse
from flask import request, jsonify
from flask_jwt_extended import jwt_required,get_jwt_identity
from application.model.model import db, Category,FundManagerCategoryConfig
from application.apis.helper_fun import schemes_data_func,categ_data



category_get_args = reqparse.RequestParser()
category_get_args.add_argument(
    "category_name", type=str, required=True, help="Category name is required",
)
category_get_args.add_argument(
    "manager_name", type=str, required=True, help="Manager name is required",
)
category_get_args.add_argument(
    "deputy_name", type=str, required=True, help="Deputy name is required",
)

class UpdateFundManagerDetailsApi(Resource):
    @jwt_required()
    def post(self):
        args = category_get_args.parse_args()
        category_name = args["category_name"]
        manager_name = args['manager_name']
        deputy_name = args['deputy_name']

        # Query to extract the category ID from the Category table based on the category_name
        category = Category.query.filter_by(name=category_name).first()

        # Extract the category_id
        category_id = category.id

        fund_manager_config = FundManagerCategoryConfig.query.filter_by(category_id=category_id).first()
        if fund_manager_config:
            fund_manager_config.fund_manager = manager_name
            fund_manager_config.deupty_fund_managers = deputy_name
        else:
            new_fund_manager_config = FundManagerCategoryConfig(category_id=category_id ,fund_manager=manager_name,deupty_fund_managers=deputy_name)
            db.session.add(new_fund_manager_config)
        try:
            
            db.session.commit()
            return {"status": "success", "message": "FM created"}, 200
        except Exception as e:
            print(e)
            return {"status": "failed", "message": "Unable to update the Fund Manager"}, 200


