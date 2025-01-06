from flask_restful import Resource,reqparse
from flask import request, jsonify
import json
from flask_jwt_extended import jwt_required,get_jwt_identity
from application.model.model import UserCategoryAccess,Company, DailySchemePerformanceParamenter as Performance, Category,Scheme
from application.apis.helper_fun import schemes_data_func,categ_data


category_get_args = reqparse.RequestParser()
category_get_args.add_argument(
    "subtype", type=str, required=True, help="Subtype is required",
)
category_get_args.add_argument(
    "type", type=str, required=True, help="Type is required",
)
category_get_args.add_argument(
    "date", type=str, required=True, help="Date is required",
)
category_get_args.add_argument(
    "categ", type=str, required=True, help="Category is required",
)
category_get_args.add_argument(
    "period", type=str, required=True, help="Period is required",
)



class CustomCategoryAPI(Resource):
    @jwt_required()
    def post(self):
        args = category_get_args.parse_args()
        directRegular = args.get('subtype')
        type = args.get('type')
        date = args.get('date')[:10]
        categ = args.get('categ')
        curr_horz = args.get('period')
        
        default_amc = 'ABSL'
        current_user =  get_jwt_identity()
        current_user_id = current_user

        user_cat_access = UserCategoryAccess.query.filter_by(user_id = current_user_id).all()
        user_category_ids =[]
        for cat in user_cat_access:
            user_category_ids.append(cat.category_id)
            
        
       
                    
        q1_schem_data,q2_schem_data,q3_schem_data,q4_schem_data,schem_comparison= [],[],[],[],[]
        category_data,performance_data,kpi_data,nfo_schemes = categ_data(directRegular,type,date,categ,curr_horz,default_amc,user_category_ids)
        
        companys = Company.query.all()
        for company in companys:
            category = Category.query.filter_by(name = categ).first()
            if category:
                perf = Performance.query.join(Scheme, Performance.scheme_id == Scheme.id).filter(Scheme.subtype==directRegular).filter(Scheme.type==type).filter(Performance.performance_date==date).filter(Scheme.category_id==category.id).filter(Scheme.company_id == company.id).add_columns(Scheme.name, Performance.data).first()
                if perf is None:
                    continue
                data = json.loads(perf[2])
                schem_comparison.append({"company_name":company.name,"amc":perf[1],'aum':round(data['scheme_aum'],2),'1m': data['thirty_d_return'], '3m': data['ninety_d_return'],
                                '6m': data['oneeighty_d_return'], '9m': data['twoseventy_d_return'], '1yr': data['one_y_return'],
                                '2yr': data['two_y_return'], '3yr': data['three_y_return'], '4yr': data['four_y_return'],
                                '5yr': data['five_y_return']
                                        })
        
        aum_quar = {period: {'q1': {'aum': 0, 'count': 0,},
                            'q2': {'aum': 0, 'count': 0},
                            'q3': {'aum': 0, 'count': 0},
                            'q4': {'aum': 0, 'count': 0}}
                    for period in ['1m', '3m', '6m', '9m', '1yr', '2yr', '3yr', '5yr']}
    
        quartile_schem_name = {period: {'q1': [],
                            'q2': [],
                            'q3': [],
                            'q4': []}
                    for period in ['1m', '3m', '6m', '9m', '1yr', '2yr', '3yr', '5yr']}
    

    
        for scheme_name, scheme_data in category_data.items():
            qr_range = int(len(list(category_data.keys())) / 4)
            for period in ['1m', '3m', '6m', '9m', '1yr', '2yr', '3yr', '5yr']:
                rank_value = scheme_data['rank'][period]
                if rank_value != '--':
                    value = float(rank_value)
                    if value <= qr_range:
                        aum_quar[period]['q1']['aum'] += scheme_data['performance']['aum']
                        quartile_schem_name[period]['q1'].append(scheme_name)
                        aum_quar[period]['q1']['count'] += 1
                    elif value <= 2 * qr_range:
                        aum_quar[period]['q2']['aum'] += scheme_data['performance']['aum']
                        quartile_schem_name[period]['q2'].append(scheme_name)
                        aum_quar[period]['q2']['count'] += 1
                    elif value <= 3 * qr_range:
                        aum_quar[period]['q3']['aum'] += scheme_data['performance']['aum']
                        quartile_schem_name[period]['q3'].append(scheme_name)
                        aum_quar[period]['q3']['count'] += 1
                    else:
                        aum_quar[period]['q4']['aum'] += scheme_data['performance']['aum']
                        quartile_schem_name[period]['q4'].append(scheme_name)
                        aum_quar[period]['q4']['count'] += 1
    
    
        for scheme_name, scheme_data in category_data.items():
            if scheme_name in quartile_schem_name[curr_horz.lower()]['q1']:
                q1_schem_data.append({'scheme':scheme_name,'aum':round(scheme_data['performance']['aum'],2),
                                        'return':scheme_data['performance'][curr_horz.lower()]})
            elif scheme_name in quartile_schem_name[curr_horz.lower()]['q2']:
                q2_schem_data.append({'scheme':scheme_name,'aum':round(scheme_data['performance']['aum'],2),
                                        'return':scheme_data['performance'][curr_horz.lower()]})
            elif scheme_name in quartile_schem_name[curr_horz.lower()]['q3']:
    
                q3_schem_data.append({'scheme':scheme_name,'aum':round(scheme_data['performance']['aum'],2),
                                        'return':scheme_data['performance'][curr_horz.lower()]})
            else:
                q4_schem_data.append({'scheme':scheme_name,'aum':round(scheme_data['performance']['aum'],2),
                                        'return':scheme_data['performance'][curr_horz.lower()]})
        amc_options = []
        category_ = Category.query.filter_by(name = categ).first()
        schemes = Scheme.query.filter_by(category_id = category_.id).all()
        amc_options = set()
        for scheme in schemes:
            name_ = Company.query.filter_by(id = scheme.company_id).first().name
            amc_options.add(name_)
        data = {
            'q1_data':q1_schem_data,
            'q2_data':q2_schem_data,
            'q3_data':q3_schem_data,
            'q4_data':q4_schem_data,
            'amc_options': sorted(amc_options),
            'performanceData':performance_data,
            'kpi_data':kpi_data,
            'scheme_comparison':schem_comparison,
            'nfo_schemes':nfo_schemes
        }
        return jsonify(data)