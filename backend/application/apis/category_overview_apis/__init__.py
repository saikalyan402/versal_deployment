import jwt
from flask import Blueprint, abort, request
from flask import current_app as app
from flask_restful import Api

from application.apis.category_overview_apis.custom_category import CustomCategoryAPI
from application.apis.category_overview_apis.category_overview_page_access_data import CategoryOverviewAccessData



category_overview_api_bp = Blueprint('category_overview_api', __name__)
category_overview_api = Api(category_overview_api_bp, prefix='/category_overview/api')


category_overview_api.add_resource(CustomCategoryAPI, '/category', methods=["POST"])
category_overview_api.add_resource(CategoryOverviewAccessData,'/category_page_data_access',methods = ["GET"])