from application.model.model import (
    db,
    Scheme,
    Company,
    Category,
    DailySchemePerformanceParamenter as Performance,
    CategoryRiskSet,
    Benchmark,
    BenchmarkData,
    BenchmarkConfig,
    Role,
    UserRole,
    User
)
import json
from datetime import datetime, timedelta
import heapq

def get_all_the_dates():
    all_records = Performance.query.all()
    unique_dates = sorted({str(record.performance_date) for record in all_records})
    return unique_dates


def schemes_data_func(amc, subtype, type, date,user_category_ids=[]):
    scheme_dict = {}
    category_dict = {}
    total_aum = 0

    formatted_date = datetime.strptime(date, "%Y-%m-%d").date()
    if amc == "":
        amc = "ABSL"
    company = Company.query.filter_by(name=amc).first()
    schemes_all = []
    for category_id in user_category_ids:
        schemes_perfs = Scheme.query.join(Performance, Scheme.id == Performance.scheme_id).filter(Performance.performance_date == formatted_date, Scheme.company_id==company.id, Scheme.subtype==subtype, Scheme.type==type, Scheme.category_id==category_id).all()
       
        for product in schemes_perfs:
            schemes_all.append(product)
            
    if user_category_ids == []:
        schemes_all = Scheme.query.join(Performance, Scheme.id == Performance.scheme_id).filter(Performance.performance_date == formatted_date,Scheme.company_id==company.id, Scheme.subtype==subtype, Scheme.type==type).all()
    for scheme in schemes_all:
        
        performance = Performance.query.filter_by(scheme_id=scheme.id, performance_date=formatted_date).first()
        if performance:
            perf = json.loads(performance.data)
        if scheme.name not in scheme_dict:
            peer_avg = (
                CategoryRiskSet.query.filter_by(
                    category_id=scheme.category_id, date=formatted_date
                )
                .first()
                .data
            )
            peer_avg_data = json.loads(peer_avg)
            category_name = Category.query.filter_by(id=scheme.category_id).first().name
            benchmark = (
                BenchmarkConfig.query.filter_by(category_id=scheme.category_id)
                .first()
            )
            if benchmark:
                benchmark_id = Benchmark.query.filter_by(name=benchmark.benchmark_name).first().id
                bench_data = (
                    BenchmarkData.query.filter_by(benchmark_id=benchmark_id).first().data
                )
                bench = json.loads(bench_data)
                category_name = Category.query.filter_by(id=scheme.category_id).first().name
                if isinstance(perf['scheme_aum'], str) and  "(" in perf['scheme_aum']:
                    perf["scheme_aum"] = int(float(perf["scheme_aum"].split("(")[0]))  # Convert to float first, then to int

                scheme_dict[scheme.name] = {
                    "category": category_name,
                    "performance": {
                        "aum": perf["scheme_aum"],
                        "1m": perf["thirty_d_return"],
                        "3m": perf["ninety_d_return"],
                        "6m": perf["oneeighty_d_return"],
                        "9m": perf["twoseventy_d_return"],
                        "1yr": perf["one_y_return"],
                        "2yr": perf["two_y_return"],
                        "3yr": perf["three_y_return"],
                        "4yr": perf["four_y_return"],
                        "5yr": perf["five_y_return"],
                    },
                    "rank": {
                        "aum": perf["scheme_aum"],
                        "1m": perf["thirty_d_rank"],
                        "3m": perf["ninety_d_rank"],
                        "6m": perf["oneeighty_d_rank"],
                        "9m": perf["twoseventy_d_rank"],
                        "1yr": perf["one_y_rank"],
                        "2yr": perf["two_y_rank"],
                        "3yr": perf["three_y_rank"],
                        "4yr": perf["four_y_rank"],
                        "5yr": perf["five_y_rank"],
                    },
                    "benchmark": {
                        "1m": bench["thirty_d"],
                        "3m": bench["ninety_d"],
                        "6m": bench["oneeighty_d"],
                        "9m": bench["twoseventy_d"],
                        "1yr": bench["one_y"],
                        "2yr": bench["two_y"],
                        "3yr": bench["three_y"],
                        "4yr": bench["four_y"],
                        "5yr": bench["five_y"],
                    },
                    "peer_avg": {
                        "1m": peer_avg_data["thirty_d"],
                        "3m": peer_avg_data["ninety_d"],
                        "6m": peer_avg_data["oneeighty_d"],
                        "9m": peer_avg_data["twoseventy_d"],
                        "1yr": peer_avg_data["one_y"],
                        "2yr": peer_avg_data["two_y"],
                        "3yr": peer_avg_data["three_y"],
                        "4yr": peer_avg_data["four_y"],
                        "5yr": peer_avg_data["five_y"],
                    },
                }

        category_name = Category.query.filter_by(id = scheme.category_id).first().name
        if category_name not in category_dict:
            category_id = Category.query.filter_by(name = category_name).first().id
            count_scheme = Scheme.query.filter_by(category_id = category_id, subtype = scheme.subtype, type = scheme.type).count()
            category_dict[category_name] = count_scheme
        if isinstance(perf['scheme_aum'], str) and  "(" in perf['scheme_aum']:
            perf["scheme_aum"] = int(float(perf["scheme_aum"].split("(")[0]))  # Convert to float first, then to int

        total_aum += int(perf["scheme_aum"])
        
 

    return scheme_dict, category_dict, total_aum

def landing_peer(amc,subtype,type,date,user_category_ids=[]):
    # date = '2024-07-03'
    formatted_date = datetime.strptime(date, "%Y-%m-%d").date()

    # companys = Company.query.all()
    peer_chartdata = []
    amcOptions = ['360 One', 'ABSL','Axis', 'BOI', 'Bajaj', 'Bandhan', 'Baroda', 'Canara', 'DSP',
                   'Edelweiss', 'Franklin', 'Groww', 'HDFC', 'HSBC', 'Helios', 'ICICI', 'ITI', 'Invesco',
                   'JM', 'Kotak', 'LIC', 'Mahindra', 'Mirae', 'Motilal', 'NJ', 'Navi', 'Nippon', 'Old Bridge',
                   'PGIM', 'PPFAS', 'Quant', 'Quantum', 'SBI', 'Samco', 'Shriram', 'Sundaram', 'TRUSTMF', 'Tata',
                     'Taurus', 'UTI', 'Union', 'WhiteOak']
    for amc in amcOptions:
        scheme_dict, category_dict = {}, {}
        aum_quar = {period: {'q1': {'aum': 0, 'count': 0},
                        'q2': {'aum': 0, 'count': 0},
                        'q3': {'aum': 0, 'count': 0},
                        'q4': {'aum': 0, 'count': 0}}
            for period in ['1m', '3m', '6m', '9m', '1yr', '2yr', '3yr', '5yr']}  
       
        if amc not in peer_chartdata:
            amc_dict = {'name':amc}
            for period in ['1M', '3M', '6M', '9M', '1Yr', '2Yr', '3Yr', '5Yr']:
                amc_dict[period]={'Q1':0,'Q2':0,'Q1Q2':0}
            peer_chartdata.append(amc_dict)
 
        total_aum = 0
        company = Company.query.filter_by(name=amc).first()

        schemes_all = []
        for category_id in user_category_ids:
            schemes_perfs = Scheme.query.join(Performance, Scheme.id == Performance.scheme_id).filter(Performance.performance_date == formatted_date, Scheme.company_id==company.id, Scheme.subtype==subtype, Scheme.type==type, Scheme.category_id==category_id).all()
       
            for product in schemes_perfs:
                schemes_all.append(product)
                
        if user_category_ids == []:
            schemes_all = Scheme.query.join(Performance, Scheme.id == Performance.scheme_id).filter(Performance.performance_date == formatted_date,Scheme.company_id==company.id, Scheme.subtype==subtype, Scheme.type==type).all()
        for scheme in schemes_all:
            performance = Performance.query.filter_by(scheme_id=scheme.id, performance_date=formatted_date).first()
            if performance:
                perf = json.loads(performance.data)
            if scheme.name not in scheme_dict:
                peer_avg = (
                    CategoryRiskSet.query.filter_by(
                        category_id=scheme.category_id, date=formatted_date
                    )
                    .first()
                    .data
                )
                peer_avg_data = json.loads(peer_avg)
                category_name = Category.query.filter_by(id=scheme.category_id).first().name
                benchmark = (
                    BenchmarkConfig.query.filter_by(category_id=scheme.category_id)
                    .first()
                )
                if benchmark:
                    benchmark_id = Benchmark.query.filter_by(name=benchmark.benchmark_name).first().id
                    bench_data = (
                        BenchmarkData.query.filter_by(benchmark_id=benchmark_id).first().data
                    )
                    bench = json.loads(bench_data)
                    category_name = Category.query.filter_by(id=scheme.category_id).first().name
                    if isinstance(perf['scheme_aum'], str) and  "(" in perf['scheme_aum']:
                        perf["scheme_aum"] = int(float(perf["scheme_aum"].split("(")[0]))  # Convert to float first, then to int

                    scheme_dict[scheme.name] = {
                        "category": category_name,
                        "performance": {
                            "aum": perf["scheme_aum"],
                            "1m": perf["thirty_d_return"],
                            "3m": perf["ninety_d_return"],
                            "6m": perf["oneeighty_d_return"],
                            "9m": perf["twoseventy_d_return"],
                            "1yr": perf["one_y_return"],
                            "2yr": perf["two_y_return"],
                            "3yr": perf["three_y_return"],
                            "4yr": perf["four_y_return"],
                            "5yr": perf["five_y_return"],
                        },
                        "rank": {
                            "aum": perf["scheme_aum"],
                            "1m": perf["thirty_d_rank"],
                            "3m": perf["ninety_d_rank"],
                            "6m": perf["oneeighty_d_rank"],
                            "9m": perf["twoseventy_d_rank"],
                            "1yr": perf["one_y_rank"],
                            "2yr": perf["two_y_rank"],
                            "3yr": perf["three_y_rank"],
                            "4yr": perf["four_y_rank"],
                            "5yr": perf["five_y_rank"],
                        },
                        "benchmark": {
                            "1m": bench["thirty_d"],
                            "3m": bench["ninety_d"],
                            "6m": bench["oneeighty_d"],
                            "9m": bench["twoseventy_d"],
                            "1yr": bench["one_y"],
                            "2yr": bench["two_y"],
                            "3yr": bench["three_y"],
                            "4yr": bench["four_y"],
                            "5yr": bench["five_y"],
                        },
                        "peer_avg": {
                            "1m": peer_avg_data["thirty_d"],
                            "3m": peer_avg_data["ninety_d"],
                            "6m": peer_avg_data["oneeighty_d"],
                            "9m": peer_avg_data["twoseventy_d"],
                            "1yr": peer_avg_data["one_y"],
                            "2yr": peer_avg_data["two_y"],
                            "3yr": peer_avg_data["three_y"],
                            "4yr": peer_avg_data["four_y"],
                            "5yr": peer_avg_data["five_y"],
                        },
                    }

            category_name = Category.query.filter_by(id = scheme.category_id).first().name
            if category_name not in category_dict:
                category_id = Category.query.filter_by(name = category_name).first().id
                count_scheme = Scheme.query.filter_by(category_id = category_id, subtype = scheme.subtype, type = scheme.type).count()
                category_dict[category_name] = count_scheme
            if isinstance(perf['scheme_aum'], str) and  "(" in perf['scheme_aum']:
                perf["scheme_aum"] = int(float(perf["scheme_aum"].split("(")[0]))  # Convert to float first, then to int

            total_aum += perf["scheme_aum"]
        for scheme_name, scheme_data in scheme_dict.items():

            qr_range = int(category_dict[scheme_data['category']] / 4)
 
            for period in ['1m', '3m', '6m', '9m', '1yr', '2yr', '3yr', '5yr']:
                rank_value = scheme_data['rank'][period]
                if rank_value != '--':
                    value = float(rank_value)
                    if value <= qr_range:
                        aum_quar[period]['q1']['aum'] += scheme_data['performance']['aum']
                        aum_quar[period]['q1']['count'] += 1
                    elif value <= 2 * qr_range:
                        aum_quar[period]['q2']['aum'] += scheme_data['performance']['aum']
                        aum_quar[period]['q2']['count'] += 1
                    elif value <= 3 * qr_range:
                        aum_quar[period]['q3']['aum'] += scheme_data['performance']['aum']
                        aum_quar[period]['q3']['count'] += 1
                    else:
                        aum_quar[period]['q4']['aum'] += scheme_data['performance']['aum']
                        aum_quar[period]['q4']['count'] += 1
        for chart_entry in peer_chartdata:
            for period in chart_entry.keys():
                if period!='name' and chart_entry['name']==amc:
                    if total_aum >= 0 and (aum_quar[period.lower()]['q1']['aum'] or aum_quar[period.lower()]['q2']['aum']) :
                        chart_entry[period]['Q1'] = round((aum_quar[period.lower()]['q1']['aum']/total_aum)*100,2)
                        chart_entry[period]['Q2'] = round((aum_quar[period.lower()]['q2']['aum']/total_aum)*100,2)
                        chart_entry[period]['Q1Q2'] = chart_entry[period]['Q1'] + chart_entry[period]['Q2']
                       

 
    return(peer_chartdata)


def landing_scheme_beat_new(scheme_dict,curr_horz):
    peer_beat_count = 0
    aum_sum = 0
    peer_aumsum = 0
    beat_bench = {}
    
   
    aum_quar = {period: {'aum':0} for period in ['1m', '3m', '6m', '9m', '1yr', '2yr', '3yr', '5yr']}
    for scheme_name, scheme_data in scheme_dict.items():
        for period in ['1m', '3m', '6m', '9m', '1yr', '2yr', '3yr', '5yr']:
            performance = scheme_data['performance'][period]
            benchmark = scheme_data['benchmark'][period]
            peeravg = scheme_data['peer_avg'][period]
            if (performance!='--' and benchmark!='--')and (float(performance)>float(benchmark)):
                if curr_horz.lower()==period:                    
                    diff = diff_bench_perf(scheme_data['performance'], scheme_data["benchmark"])
                    beat_bench[scheme_name] = {'performance':diff}
                    aum_sum+=scheme_data['performance']['aum']
                aum_quar[period]['aum']+=scheme_data['performance']['aum']
            if (performance!='--' and benchmark!='--')and (float(performance)>float(peeravg)):
                if curr_horz.lower()==period: # this is wrong
                    peer_beat_count+=1
                    peer_aumsum+=scheme_data['performance']['aum']

 
    
 
    return (beat_bench,peer_beat_count,aum_sum,peer_aumsum)


def landing_scheme_beat(amc,subtype,type,scheme_dict,total_aum_curr,date_prev,curr_horz,date,user_category_ids=[]):
    compare_chart = [{'name':period, 'previous':0,'current':0} for period in ['1M', '3M', '6M', '9M', '1Yr', '2Yr', '3Yr', '5Yr']]
    schemes_prev,category,total_aum_prev = schemes_data_func(amc,subtype,type,str(date_prev),user_category_ids)
    counter = 0
    peer_beat_count = 0
    aum_sum = 0
    peer_aumsum = 0
    beat_bench = {}
    
    for scheme in [scheme_dict, schemes_prev]:
        if counter ==0:
            status = 'current'
        else:
            status = 'previous'
        aum_quar = {period: {'aum':0}
                for period in ['1m', '3m', '6m', '9m', '1yr', '2yr', '3yr', '5yr']}
        for scheme_name, scheme_data in scheme.items():
            for period in ['1M', '3M', '6M', '9M', '1Yr', '2Yr', '3Yr', '5Yr']:
                performance = scheme_data['performance'][period.lower()]
                benchmark = scheme_data['benchmark'][period.lower()]
                peeravg = scheme_data['peer_avg'][period.lower()]
                if (performance!='--' and benchmark!='--')and (float(performance)>float(benchmark)):
                    if curr_horz.lower()==period.lower():
                        
                        diff = diff_bench_perf(scheme_data['performance'], scheme_data["benchmark"])
                        beat_bench[scheme_name] = {'performance':diff}
                        aum_sum+=scheme_data['performance']['aum']
                    aum_quar[period.lower()]['aum']+=scheme_data['performance']['aum']
                if (performance!='--' and benchmark!='--')and (float(performance)>float(peeravg)):
                    if curr_horz.lower()==period.lower() and status =='current':
                        peer_beat_count+=1
                        peer_aumsum+=scheme_data['performance']['aum']
 
        for chart_entry in compare_chart:
            period = chart_entry['name'].lower()
            if aum_quar[period]['aum']>=0 and total_aum_curr>0:
                if counter==0:
                    chart_entry[status] = round((aum_quar[period]['aum']/total_aum_curr)*100,2)
                else:
                    chart_entry[status] = round((aum_quar[period]['aum']/total_aum_prev)*100,2)
 
        counter+=1
 
    return (compare_chart,beat_bench,peer_beat_count,aum_sum,peer_aumsum)

def diff_bench_perf(perf, bech):

    diff ={
        '1m': round(float(perf['1m']) - float(bech['1m']),2) if perf['1m'] != "--" else "--",
        '3m': round(float(perf['3m']) - float(bech['3m']),2) if perf['3m'] != "--" else "--", 
        '6m': round(float(perf['6m']) - float(bech['6m']),2) if perf['6m'] != "--" else "--", 
        '9m': round(float(perf['9m']) - float(bech['9m']),2) if perf['9m'] != "--" else "--",
        '1yr': round(float(perf['1yr']) - float(bech['1yr']),2) if perf['1yr'] != "--" else "--",
        '2yr': round(float(perf['2yr']) - float(bech['2yr']),2) if perf['2yr'] != "--" else "--",
        '3yr': round(float(perf['3yr']) - float(bech['3yr']),2) if perf['3yr'] != "--" else "--",
        '5yr': round(float(perf['5yr']) - float(bech['5yr']),2) if perf['5yr'] != "--" else "--"
        
    }
    return diff



def aum_sorting(rows):
    heap_list = []
    for schemes in rows:
        schem_row = Scheme.query.filter_by(id=schemes.scheme_id).first()
        name = schem_row.name
        heap_list.append((float(json.loads(schemes.data)["scheme_aum"] * -1), name))
    heapq.heapify(heap_list)

    rank = 1
    schem_dict = {}
    while heap_list:
        aum, name = heapq.heappop(heap_list)
        schem_dict[name] = rank
        rank += 1
    
    name_keys = list(schem_dict.keys())
    
    # Initialize bottom_rank_list with a default empty list
    bottom_list = []
    if len(name_keys) >= 3:
        bottom_list = [schem_dict[name_keys[-1]], schem_dict[name_keys[-2]], schem_dict[name_keys[-3]]]

    return schem_dict, bottom_list



def fun_sorting(rows):
    heap_list = []
    for schemes in rows:
        schem_row = Scheme.query.filter_by(id=schemes.scheme_id).first()
        name = schem_row.name
        heap_list.append((float(json.loads(schemes.data)["scheme_aum"] * -1), name))
    heapq.heapify(heap_list)

    rank = 1
    schem_dict = {}
    while heap_list:
        aum, name = heapq.heappop(heap_list)
        schem_dict[name] = rank
        rank += 1
   
    name_keys = list(schem_dict.keys())
    
    # Initialize bottom_rank_list with a default empty list
    bottom_rank_list = []
    top_rank_list = []
    
    if len(name_keys) > 5:
        bottom_rank_list = [name_keys[-1], name_keys[-2], name_keys[-3]]
        top_rank_list = [name_keys[0], name_keys[1], name_keys[2]]
    elif len(name_keys) == 1 or len(name_keys) == 2 or len(name_keys) == 3:
        bottom_rank_list = []
        if len(name_keys) == 3:
            top_rank_list = [name_keys[0], name_keys[1], name_keys[2]]
        if len(name_keys) == 2:
            top_rank_list = [name_keys[0], name_keys[1]]
        else:
            top_rank_list = [name_keys[0]]
    else:
        top_rank_list = [name_keys[0], name_keys[1], name_keys[2]]
        if len(name_keys) == 4:
            bottom_rank_list = [name_keys[-1]]
        else:
            bottom_rank_list = [name_keys[-1], name_keys[-2]]
 
    return bottom_rank_list, top_rank_list
    
    





def safe_float(value):
    return float(value) if value != '--' else None

def difference_calc(main_list,second_list):
    difference = []
    for perf_val, bench_val in zip(main_list,second_list):
            perf_float = safe_float(perf_val)
            bench_float = safe_float(bench_val)
            
            if perf_float is None or bench_float is None:
                difference.append('--')
            else:
                difference.append(round(perf_float - bench_float, 2)) 
    return difference


def performers_avg(schemes, date):
    formatted_date = datetime.strptime(date, "%Y-%m-%d").date()
    return_list = []

    for schemename in schemes:

        scheme = Scheme.query.filter_by(name=schemename).first()
        
        # Initialize temp as an empty list before checking if scheme_performance exists
        temp = []

        if scheme:
            # If scheme is found, retrieve its performance
            scheme_performance = Performance.query.filter_by(scheme_id=scheme.id, performance_date=formatted_date).first()

            if scheme_performance:
                performance = json.loads(scheme_performance.data)
                perf = ["one_y_return", "two_y_return", "three_y_return", "five_y_return", "seven_y_return", "ten_y_return",
                        "twelve_y_return", "fifteen_y_return"]
                for i in perf:
                    if performance[i] == '--':
                        temp.append(0)
                    else:
                        temp.append(performance[i])
            else:
                # If no scheme_performance found, append a default value (e.g., a list of zeros)
                temp = [0] * 8
        else:
            # If no scheme is found, append a default value (e.g., a list of zeros)
            temp = [0] * 8

        # Append the temp list to return_list
        return_list.append(temp)
 
    if len(return_list)==0:
        return ['--']*8
   
   
    avg_arr = []
    for i in range(8):
        avg_arr.append(0)
    for i in range(len(return_list)):
        for j in range(8):
            avg_arr[j] += return_list[i][j]
    for i in range(8):
        avg_arr[i] = round(avg_arr[i]/len(return_list), 2)
    avg_list = avg_arr
   
    return avg_list



def categ_data(directRegular, type, date, categ, period, default_amc, user_category_ids):
    formatted_date = datetime.strptime(date, "%Y-%m-%d").date()
    scheme_dict, kpi_data, rank_1_data, rank_absl_data, rank_above_data, rank_below_data = {}, {}, {}, {}, {}, {}
    perf_data, top3_avg, bottom3_avg, absl_return, nfo_schemes = [], [], [], [], []
    best_count, worst_count, bottom_threshold, absl_rank, absl_aum = 0, 0, 0, 0,0
    
    category = Category.query.filter_by(name=categ).first()
    
    rows = Performance.query.join(Scheme, Performance.scheme_id == Scheme.id).filter(
        Scheme.subtype == directRegular).filter(Scheme.type == type).filter(
        Performance.performance_date == date).filter(Scheme.category_id == category.id).all()
        

    category_total_aum = sum(float(json.loads(row.data)["scheme_aum"]) for row in rows if row.data)
    scheme_rank_aum, bottom_list = aum_sorting(rows)
    bottom_rank_list, top_rank_list = fun_sorting(rows)

    seen_schemes = set()  # Set to track schemes already added to nfo_schemes

    schemes_all = Scheme.query.join(Performance, Scheme.id == Performance.scheme_id).filter(
        Performance.performance_date == formatted_date, Scheme.subtype == directRegular,
        Scheme.type == type, Scheme.category_id == category.id).all()

    for scheme in schemes_all:
        performance = Performance.query.filter_by(scheme_id=scheme.id, performance_date=formatted_date).first()
        if performance:
            perf = json.loads(performance.data)
        scheme_company = Company.query.filter_by(id=scheme.company_id).first()

        if scheme.name not in scheme_dict:
            # Try to fetch the benchmark, and if it doesn't exist, proceed with fallback logic
            benchmark = BenchmarkConfig.query.filter_by(category_id=scheme.category_id).first()

            # Fallback values in case there is no benchmark
            benchmark_data = {}
            if benchmark:
                benchmark_id = Benchmark.query.filter_by(name=benchmark.benchmark_name).first().id
                bench_data = BenchmarkData.query.filter_by(benchmark_id=benchmark_id).first().data
                benchmark_data = json.loads(bench_data)

            # Now we process the scheme data and handle the possibility of no benchmark data
            category_name = Category.query.filter_by(id=scheme.category_id).first().name


            scheme_dict[scheme.name] = {
                "category": category_name,
                "company": scheme_company.name,
                "performance": {
                    "aum": perf["scheme_aum"],
                    "1m": perf["thirty_d_return"],
                    "3m": perf["ninety_d_return"],
                    "6m": perf["oneeighty_d_return"],
                    "9m": perf["twoseventy_d_return"],
                    "1yr": perf["one_y_return"],
                    "2yr": perf["two_y_return"],
                    "3yr": perf["three_y_return"],
                    "4yr": perf["four_y_return"],
                    "5yr": perf["five_y_return"],
                },
                "rank": {
                    "aum": perf["scheme_aum"],
                    "1m": perf["thirty_d_rank"],
                    "3m": perf["ninety_d_rank"],
                    "6m": perf["oneeighty_d_rank"],
                    "9m": perf["twoseventy_d_rank"],
                    "1yr": perf["one_y_rank"],
                    "2yr": perf["two_y_rank"],
                    "3yr": perf["three_y_rank"],
                    "4yr": perf["four_y_rank"],
                    "5yr": perf["five_y_rank"],
                },
                "benchmark": {
                    "1m": benchmark_data.get("thirty_d", '--'),
                    "3m": benchmark_data.get("ninety_d", '--'),
                    "6m": benchmark_data.get("oneeighty_d", '--'),
                    "9m": benchmark_data.get("twoseventy_d", '--'),
                    "1yr": benchmark_data.get("one_y", '--'),
                    "2yr": benchmark_data.get("two_y", '--'),
                    "3yr": benchmark_data.get("three_y", '--'),
                    "4yr": benchmark_data.get("four_y", '--'),
                    "5yr": benchmark_data.get("five_y", '--'),
                },

            }

            # Process ABSL schemes with benchmark data as needed
            if scheme_company.name == 'ABSL':
                absl_return = [
                    perf["one_y_return"], perf["two_y_return"], perf["three_y_return"],
                    perf["five_y_return"], perf["seven_y_return"], perf["ten_y_return"],
                    perf["twelve_y_return"], perf["fifteen_y_return"]
                ]
                
                if benchmark_data:
                    bench_return = [
                        benchmark_data.get("one_y", '--'), benchmark_data.get("two_y", '--'),
                        benchmark_data.get("three_y", '--'), benchmark_data.get("five_y", '--'),
                        benchmark_data.get("seven_y", '--'), benchmark_data.get("ten_y", '--'),
                        benchmark_data.get("twelve_y", '--'), benchmark_data.get("fifteen_y", '--')
                    ]
                    diff = difference_calc(absl_return, bench_return)
                    

                    # Append the performance data for ABSL with benchmark
                    perf_data.append({'label': "ABSL Scheme Returns", 'values': absl_return})
                    perf_data.append({'label': "Benchmark", 'values': bench_return})
                    perf_data.append({'label': "Diff. from Benchmark", 'values': diff})

                    absl_rank = scheme_rank_aum[scheme.name]
                    absl_aum = scheme_dict[scheme.name]['rank']['aum']

                    rank_absl_data = {'scheme': scheme.name, 'rank': absl_rank, 'aum': absl_aum, 'gap': '--'}
                    if absl_rank <= 5:
                        value = "We're in TOP 5"
                    else:
                        value = "We're not in TOP 5"

                    kpi_data['left'] = [
                        {'label': "ABSL AUM", 'value': round(perf["scheme_aum"], 2)},
                        {'label': "ABSL AUM Rank", 'value': absl_rank},
                        {'label': "ABSL Market share", 'value': f'{round((float(perf["scheme_aum"]) / category_total_aum) * 100, 2)}%'},
                        {'label': value, 'value': ""}
                    ]
                    curr_rank = scheme_rank_aum[scheme.name]
                    curr_aum = scheme_dict[scheme.name]['rank']['aum']
                    if curr_rank == 1:
                        rank_1_data = {'scheme': scheme.name, 'rank': curr_rank,
                                    'aum': curr_aum, 'gap': round(int(curr_aum) - int(absl_aum), 2)}
                    elif curr_rank == (absl_rank - 1):
                        rank_above_data = {'scheme': scheme.name, 'rank': curr_rank,
                                        'aum': curr_aum, 'gap': round(int(curr_aum) - int(absl_aum), 2)}
                    elif curr_rank == (absl_rank + 1):
                        rank_below_data = {'scheme': scheme.name, 'rank': curr_rank,
                                        'aum': curr_aum, 'gap': '(' + str(round(int(curr_aum) - int(absl_aum), 2)) + ')'}

    
                else:
                    # If no benchmark data, set the KPI values to '--'
                    kpi_data['left'] = [
                        {'label': "ABSL AUM", 'value': round(perf["scheme_aum"], 2)},
                        {'label': "ABSL AUM Rank", 'value': '--'},
                        {'label': "ABSL Market share", 'value': '--'},
                        {'label': "Benchmark", 'value': '--'}
                    ]

            # Now append scheme data to nfo_schemes if it's not already added
            
            
            curr_rank = scheme_rank_aum[scheme.name]
            curr_aum = scheme_dict[scheme.name]['rank']['aum']
            if curr_rank == 1:
                rank_1_data = {'scheme': scheme.name, 'rank': curr_rank,
                                   'aum': curr_aum, 'gap': round(int(curr_aum) - int(absl_aum), 2)}
            elif curr_rank == (absl_rank - 1):
                rank_above_data = {'scheme': scheme.name, 'rank': curr_rank,
                                       'aum': curr_aum, 'gap': round(int(curr_aum) - int(absl_aum), 2)}
            elif curr_rank == (absl_rank + 1):
                rank_below_data = {'scheme': scheme.name, 'rank': curr_rank,
                                       'aum': curr_aum, 'gap': '(' + str(round(int(curr_aum) - int(absl_aum), 2)) + ')'}
    
            
            
            
            if scheme.name not in seen_schemes:
                nfo_schemes.append({
                    'amc': scheme.name,
                    "aum": perf["scheme_aum"],
                    "1m": perf["thirty_d_return"],
                    "3m": perf["ninety_d_return"],
                    "6m": perf["oneeighty_d_return"],
                    "9m": perf["twoseventy_d_return"],
                    "1yr": perf["one_y_return"],
                    "2yr": perf["two_y_return"],
                    # "3yr": perf["three_y_return"]
                })
                seen_schemes.add(scheme.name)


    top3_avg = performers_avg(top_rank_list, date)
    bottom3_avg = performers_avg(bottom_rank_list, date)

    



    perf_data.append({'label': "TOP 3", 'values': top3_avg})
    perf_data.append({'label': "Diff. from TOP 3", 'values': difference_calc(absl_return, top3_avg)})
    perf_data.append({'label': "BOTTOM 3", 'values': bottom3_avg})
    perf_data.append({'label': "Diff. from BOTTOM 3", 'values': difference_calc(absl_return, bottom3_avg)})

    kpi_data['right'] = [rank_1_data, rank_above_data, rank_absl_data, rank_below_data]
    return scheme_dict, perf_data, kpi_data, nfo_schemes

def is_admin(logined_user_id):
    admin_role_id = Role.query.filter_by(code = "ADMIN").first().id
    admin_user_role = UserRole.query.filter_by(user_id=logined_user_id).filter_by(role_id = admin_role_id).first()
    if admin_user_role is None:
        return False
    return True
 
 