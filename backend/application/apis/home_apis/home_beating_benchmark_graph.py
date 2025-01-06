from flask_restful import Resource, reqparse
from flask import jsonify
from flask_jwt_extended import jwt_required
from application.apis.helper_fun import schemes_data_func
from application.model.model import DailySchemePerformanceParamenter as Performance

chart_get_args = reqparse.RequestParser()
chart_get_args.add_argument(
    "subtype", type=str, required=True, help="Subtype is required",
)
chart_get_args.add_argument(
    "type", type=str, required=True, help="Type is required",
)
chart_get_args.add_argument(
    "current_date", type=str, required=True, help="Date is required",
)
chart_get_args.add_argument(
    "previous_date", type=str, required=True, help="Previous Date is required",
)
chart_get_args.add_argument(
    "amc", type=str, required=True, help="AMC is required",
)

from bisect import bisect_left
def find_previous_date(current_date):
    all_records = Performance.query.all()
    unique_dates = sorted({str(record.performance_date) for record in all_records})
    pos = bisect_left(unique_dates, current_date)
    if pos == 0:
        return current_date  # No previous date available
    return unique_dates[pos - 1]

class HomeBenchBeatChart(Resource):
    @jwt_required()
    def post(self):
        args = chart_get_args.parse_args()
        subtype = args.get("subtype")
        type = args.get("type")
        current_date = args.get("current_date")[:10]
        previous_date = args.get("previous_date")[:10]
        amc = args.get("amc")
        if current_date == '':
            current_date = str(Performance.query.order_by(Performance.performance_date.desc()).first().performance_date)
        
        if previous_date == '':
            previous_date = find_previous_date(current_date)

        
        
        compare_chart = [{'name':period, 'previous':0,'current':0} for period in ['1M', '3M', '6M', '9M', '1Yr', '2Yr', '3Yr', '5Yr']]
        counter = 0
        curr_scheme_dict,curr_category_dict, curr_total_aum = schemes_data_func(amc,subtype,type,str(current_date),user_category_ids=[])
        prev_scheme_dict,prev_category_dict,prev_total_aum = schemes_data_func(amc,subtype,type,str(previous_date),user_category_ids=[])

        for dictionary in [curr_scheme_dict, prev_scheme_dict]:
            if counter ==0:
                status = 'current'
            else:
                status = 'previous'
            aum_quar = {period: {'count':0}
                for period in ['1m', '3m', '6m', '9m', '1yr', '2yr', '3yr', '5yr']}
            for scheme_name, scheme_data in dictionary.items():
                for period in ['1M', '3M', '6M', '9M', '1Yr', '2Yr', '3Yr', '5Yr']:
                    performance = scheme_data['performance'][period.lower()]
                    benchmark = scheme_data['benchmark'][period.lower()]
                    if (performance!='--' and benchmark!='--')and (float(performance)>float(benchmark)):
                        aum_quar[period.lower()]['count']+=1
            
            for chart_entry in compare_chart:
                period = chart_entry['name'].lower()
                if aum_quar[period]['count']>=0 and curr_total_aum>0:
                    if counter==0:
                        chart_entry[status] = round((aum_quar[period]['count']/len(curr_scheme_dict))*100,2)
                    else:
                        chart_entry[status] = round((aum_quar[period]['count']/len(prev_scheme_dict))*100,2)

            counter+=1
        data = {
            "compare_chart": compare_chart,
            "previous_date": previous_date
        }
        return jsonify(data)