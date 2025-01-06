from application.model.model import db, Scheme, Company, DailySchemePerformanceParamenter
from application.apis.helper_fun import get_all_the_dates

from flask_jwt_extended import jwt_required
from flask_restful import Resource

class HomeInitialData(Resource):
    @jwt_required()
    def get(self):
        schemes = Scheme.query.all()
        subtype_type_amc_mapping = {}
        for scheme in schemes:
            amc_name = Company.query.filter_by(id = scheme.company_id).first().name
            if scheme.subtype not in subtype_type_amc_mapping.keys():
                subtype_type_amc_mapping[scheme.subtype] = {}
            if scheme.type not in subtype_type_amc_mapping[scheme.subtype].keys():
                subtype_type_amc_mapping[scheme.subtype][scheme.type] = []
            if amc_name not in subtype_type_amc_mapping[scheme.subtype][scheme.type]:
                subtype_type_amc_mapping[scheme.subtype][scheme.type].append(amc_name)
            
            
        return {"status": "success", "subtype_type_amc_mapping": subtype_type_amc_mapping, "all_dates":get_all_the_dates()}, 200