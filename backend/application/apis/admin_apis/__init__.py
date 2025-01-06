import jwt
from flask import Blueprint, abort, request
from flask import current_app as app
from flask_restful import Api


from application.apis.admin_apis.user_register import UserRegister
from application.apis.admin_apis.all_role_names import AllRoleNames
from application.apis.admin_apis.all_category_names import AllCategoryName
from application.apis.admin_apis.edit_user_category_access import UserRoleAndCategoryAccessChange
from application.apis.admin_apis.edit_user_password import UserPasswordChange
from application.apis.admin_apis.all_user import AllUser
from application.apis.admin_apis.all_permission_name import AllPermissionName
from application.apis.admin_apis.make_user_inactive import MakeUserInactive
from application.apis.admin_apis.add_role_and_acces import RolePermissionAPI
from application.apis.admin_apis.all_role_permission import AllRolePermissionAPI
from application.apis.admin_apis.edit_role_page_access import EditRolePageAccess
from application.apis.admin_apis.all_amc_names import AllAmcNames
from application.apis.admin_apis.type_category_amc_mapping import TypeCategoryAmcMappingAPI
from application.apis.admin_apis.create_custom_peerset import CreateCustomPeerRistSet
from application.apis.admin_apis.all_cutomise_risk_set import CategoryCustomRiskSetAPI
from application.apis.admin_apis.all_fund_manager_details import FundManagersDetails
from application.apis.admin_apis.edit_fund_manager import UpdateFundManagerDetailsApi
from application.apis.admin_apis.all_dates import AllDates
from application.apis.admin_apis.all_users_activity import AllUserActivity
from application.apis.admin_apis.delete_data_by_date import DeleteData
from application.apis.admin_apis.user_active_status_update import UserActiveStatus

admin_api_bp = Blueprint('admin_api', __name__)
admin_api = Api(admin_api_bp, prefix='/admin/api')


GPPP = ["GET", "POST", "PUT", "PATCH"]
admin_api.add_resource(UserRegister,'/register', methods=["POST"])
admin_api.add_resource(AllRoleNames,'/role_list', methods=["GET"])
admin_api.add_resource(AllCategoryName,'/category_list', methods=["GET"])
admin_api.add_resource(UserRoleAndCategoryAccessChange, "/user_role_category_access_change", methods=["POST"])
admin_api.add_resource(UserPasswordChange, "/user_password_change", methods = ["POST"])
admin_api.add_resource(AllUser, "/all_users", methods = ["GET"])
admin_api.add_resource(AllPermissionName, "/permission_list", methods = ["GET"])
admin_api.add_resource(MakeUserInactive,"/make_user_inactive", methods=["POST"])
admin_api.add_resource(RolePermissionAPI, "/role_permission", methods=["POST"])
admin_api.add_resource(AllRolePermissionAPI, "/all_role_permission", methods=["GET"])
admin_api.add_resource(EditRolePageAccess, "/edit_role_page_access", methods = ["POST"])
admin_api.add_resource(AllAmcNames, "/all_amc_names", methods=["GET"])
admin_api.add_resource(TypeCategoryAmcMappingAPI, "/type_category_amc_mapping", methods =["GET"])
admin_api.add_resource(CreateCustomPeerRistSet,"/create_custom_peer_set", methods = ["POST"])
admin_api.add_resource(CategoryCustomRiskSetAPI, "/category_risk_sets", methods=["GET"])
admin_api.add_resource(FundManagersDetails, "/all_fund_managers_details", methods=["GET"])
admin_api.add_resource(UpdateFundManagerDetailsApi, "/edit_fund_manager_details", methods=["POST"])
admin_api.add_resource(AllDates, "/all_dates", methods=["GET"])
admin_api.add_resource(AllUserActivity, "/all_users_activity", methods=["GET"])
admin_api.add_resource(DeleteData, "/delete_data", methods = ["POST"])
admin_api.add_resource(UserActiveStatus,"/update_user_active_status", methods=["PATCH"])