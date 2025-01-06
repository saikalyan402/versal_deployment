from flask_restful import Resource, reqparse
from flask import jsonify
from application.apis.helper_fun import schemes_data_func,landing_peer,landing_scheme_beat,landing_scheme_beat_new,get_all_the_dates
from datetime import datetime,timedelta
from application.model.model import DailySchemePerformanceParamenter as Performance, Scheme, Company
from flask_jwt_extended import jwt_required,get_jwt_identity



landing_get_args = reqparse.RequestParser()
landing_get_args.add_argument(
    "subtype", type=str, required=True, help="Subtype is required",
)
landing_get_args.add_argument(
    "type", type=str, required=True, help="Type is required",
)
landing_get_args.add_argument(
    "date", type=str, required=True, help="Date is required",
)
landing_get_args.add_argument(
    "amc1", type=str, required=True, help="AMC is required",
)
landing_get_args.add_argument(
    "selectedPeriod", type=str, required=True, help="Period is required",
)




class LandingAPI(Resource):
    @jwt_required()
    def post(self):
        args = landing_get_args.parse_args()
        subtype = args.get("subtype")
        type = args.get("type")
        date = args.get("date")[:10]  #2024-07-03
        if date == '':
            date = str(Performance.query.order_by(Performance.performance_date.desc()).first().performance_date)
            # date = datetime.strptime(date, "%Y-%m-%d").date()

        current_user =  get_jwt_identity()
        current_user_id = current_user


        amc = args.get("amc1")
        curr_horz = args.get("selectedPeriod")   # 1M, 3M, 6M, 1Y, 3Y, 5Y, 10Y, 15Y, 20Y, 25Y, 30Y
        
        if amc=="":
            amc="ABSL"
        if subtype == "":
            subtype = "Regular"
        if type == "":
            type = "Equity"


        
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
        
        chart_data = [{ 'name': period, 'green': 0, 'yellow': 0, 'orange': 0, 'red': 0 } for period in ['1M', '3M', '6M', '9M', '1Yr', '2Yr', '3Yr', '5Yr']]

        q1_schem_data,q2_schem_data,q3_schem_data,q4_schem_data = [],[],[],[]
        
        scheme_dict, category_dict, total_aum = schemes_data_func(amc,subtype,type,date)
        
        for scheme_name, scheme_data in scheme_dict.items():
            qr_range = int(category_dict[scheme_data['category']] / 4)
            
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
    
    
        for chart_entry in chart_data:
            period = chart_entry['name'].lower()
            chart_entry['green'] = aum_quar[period]['q1']['aum']
            chart_entry['yellow'] = aum_quar[period]['q2']['aum']
            chart_entry['orange'] = aum_quar[period]['q3']['aum']
            chart_entry['red'] = aum_quar[period]['q4']['aum']
    
        for scheme_name, scheme_data in scheme_dict.items():
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
    
    
        peer_chartdata = landing_peer(amc,subtype,type,date)
        beat_bench,peer_beat_count,aum_sum,peer_aumsum = landing_scheme_beat_new(scheme_dict,curr_horz)
        
        data = {
            'schemes_data':scheme_dict,
            'category': category_dict,
            'chart_data': chart_data,
            'peer_chartdata':peer_chartdata,
            'q1_data':q1_schem_data,
            'q2_data':q2_schem_data,
            'q3_data':q3_schem_data,
            'q4_data':q4_schem_data,
            'beat_bench':beat_bench,
            'beat_bench_count':len(beat_bench),
            'peer_beat_count':peer_beat_count,
            'schemes_count':len(scheme_dict),
            'aum_sum':aum_sum,
            'peer_aumsum':peer_aumsum,
            'total_aum':total_aum,
            'selected_date': date,
            'all_dates': get_all_the_dates()
        }
        return jsonify(data)