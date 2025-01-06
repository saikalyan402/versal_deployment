from application.model.model import FundManagerCategoryConfig, Category
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from application.apis.helper_fun import is_admin

class FundManagersDetails(Resource):
    @jwt_required()
    def get(self):
        logined_user_id = get_jwt_identity()
        if is_admin(logined_user_id) == False:
            return {"status":"failed","message":"Only admin can access this"},200
        fund_manger_data = FundManagerCategoryConfig.query.all()
        data_list = []
        for fundmanager in fund_manger_data:
            data_dict ={}
            category_name = Category.query.filter_by(id=fundmanager.category_id).first().name
            manager_name = fundmanager.fund_manager
            deupty_manager_name = fundmanager.deupty_fund_managers
            data_dict["category_name"] = category_name
            data_dict["manager_name"] = manager_name
            data_dict["deupty_manager_name"] = deupty_manager_name
            data_list.append(data_dict)

        data = data_list
        return {"status": "success", "data": data}, 200