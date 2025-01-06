from flask_restful import Resource
from flask_jwt_extended import jwt_required
from application.model.model import FundManagerCategoryConfig,Category
from application.apis.helper_fun import get_all_the_dates


class EdgeInitialData(Resource):
    @jwt_required()
    def get(self):
        
        all_fund_managers = FundManagerCategoryConfig.query.all()
        fund_manager_deputy_category_mapping = {}
        
        for row in all_fund_managers:
            if row.fund_manager not in fund_manager_deputy_category_mapping:
                fund_manager_deputy_category_mapping[row.fund_manager] = []
            new_dict = {}
            new_dict['deputy'] = row.deupty_fund_managers
            category_name = Category.query.filter_by(id=row.category_id).first().name
            new_dict['category_name'] = category_name
            fund_manager_deputy_category_mapping[row.fund_manager].append(new_dict)

        data = {'fund_manager_deputy_category_mapping':fund_manager_deputy_category_mapping,"all_dates":get_all_the_dates()}

        return {"status":"success","data":data},200

            
