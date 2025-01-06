import os
import pandas as pd
import numpy as np
import json


from application.model.model import db,Benchmark,BenchmarkConfig,BenchmarkData, Category
from application.helper import replace_nan_with_placeholder


def populate_benchmark(current_dir,new_date,first_col):
    all_equity_benchmark = os.listdir(current_dir+'/default//Equity_benchmark_values')
    equity_benchmark = pd.DataFrame(columns=['date','benchmark_name','benchmark_type','benchmark_category','YTD','one_d','seven_d','fourteen_d','thirty_d','sixty_d','ninety_d','oneeighty_d','twoseventy_d','one_y','two_y','three_y','four_y','five_y','seven_y','ten_y','twelve_y','fifteen_y'])
    
    for i in all_equity_benchmark :
        bdf = pd.read_csv(current_dir+'/default//Equity_benchmark_values//'+i)
        benchmark_table=pd.DataFrame(columns=['date','benchmark_name','benchmark_type','benchmark_category','YTD','one_d','seven_d','fourteen_d','thirty_d','sixty_d','ninety_d','oneeighty_d','twoseventy_d','one_y','two_y','three_y','four_y','five_y','seven_y','ten_y','twelve_y','fifteen_y'])
    # year-month-date
    
        benchmark_table['date']= [new_date]*bdf.iloc[3:]['Unnamed: 2'].shape[0]
        benchmark_table['benchmark_name']=list(bdf.iloc[3:][first_col])
        benchmark_table['benchmark_type']=['Equity']*(bdf.iloc[3:]['Unnamed: 2'].shape[0])
        benchmark_table['benchmark_category'] = [bdf.iloc[0, 0]] * (bdf.iloc[3:, bdf.columns.get_loc('Unnamed: 2')].shape[0])
        benchmark_table['YTD']=list(bdf.iloc[3:]['Unnamed: 38'])
        benchmark_table['one_d']=([np.nan]*(bdf.iloc[3:]['Unnamed: 2'].shape[0]))
        benchmark_table['seven_d']=list(bdf.iloc[3:]['Unnamed: 2'])
        benchmark_table['fourteen_d']=list(bdf.iloc[3:]['Unnamed: 4'])
        benchmark_table['thirty_d']=list(bdf.iloc[3:]['Unnamed: 6'])
        benchmark_table['sixty_d']=list(bdf.iloc[3:]['Unnamed: 8'])
        benchmark_table['ninety_d']=list(bdf.iloc[3:]['Unnamed: 10'])
        benchmark_table['oneeighty_d']=list(bdf.iloc[3:]['Unnamed: 12'])
        benchmark_table['twoseventy_d']=list(bdf.iloc[3:]['Unnamed: 14'])
        benchmark_table['one_y']=list(bdf.iloc[3:]['Unnamed: 18'])
        benchmark_table['two_y']=list(bdf.iloc[3:]['Unnamed: 20'])
        benchmark_table['three_y']=list(bdf.iloc[3:]['Unnamed: 22'])
        benchmark_table['four_y']=([np.nan]*(bdf.iloc[3:]['Unnamed: 2'].shape[0]))
        benchmark_table['five_y']=list(bdf.iloc[3:]['Unnamed: 24'])
        benchmark_table['seven_y']=list(bdf.iloc[3:]['Unnamed: 26'])
        benchmark_table['ten_y']=list(bdf.iloc[3:]['Unnamed: 28'])
        benchmark_table['twelve_y']=list(bdf.iloc[3:]['Unnamed: 30'])
        benchmark_table['fifteen_y']=list(bdf.iloc[3:]['Unnamed: 32'])
        benchmark_table['twenty_y']=list(bdf.iloc[3:]['Unnamed: 34'])
        if not benchmark_table.empty and not benchmark_table.isna().all().all():
            equity_benchmark = pd.concat([equity_benchmark, benchmark_table], axis=0)
    
    all_debt_category = os.listdir(current_dir+'/default//Debt_benchmark_values')
    debt_benchmark = pd.DataFrame(columns=['date','benchmark_name','benchmark_type','benchmark_category','YTD','one_d','seven_d','fourteen_d','thirty_d','sixty_d','ninety_d','oneeighty_d','twoseventy_d','one_y','two_y','three_y','four_y','five_y','seven_y','ten_y','twelve_y','fifteen_y'])
    
    for i in all_debt_category :
        bdf = pd.read_csv(current_dir+'/default//Debt_benchmark_values//'+i)
        benchmark_table=pd.DataFrame(columns=['date','benchmark_name','benchmark_type','benchmark_category','YTD','one_d','seven_d','fourteen_d','thirty_d','sixty_d','ninety_d','oneeighty_d','twoseventy_d','one_y','two_y','three_y','four_y','five_y','seven_y','ten_y','twelve_y','fifteen_y'])
        benchmark_table['date']= [new_date]*bdf.iloc[3:]['Unnamed: 2'].shape[0]
        benchmark_table['benchmark_name']=list(bdf.iloc[3:][first_col])
        benchmark_table['benchmark_type']=['Debt']*(bdf.iloc[3:]['Unnamed: 2'].shape[0])
        benchmark_table['benchmark_category'] = [bdf.iloc[0, 0]] * (bdf.iloc[3:, bdf.columns.get_loc('Unnamed: 2')].shape[0])
        benchmark_table['YTD']=([np.nan]*(bdf.iloc[3:]['Unnamed: 2'].shape[0]))
        benchmark_table['one_d']=list(bdf.iloc[3:]['Unnamed: 2'])
        benchmark_table['seven_d']=list(bdf.iloc[3:]['Unnamed: 4'])
        benchmark_table['fourteen_d']=list(bdf.iloc[3:]['Unnamed: 6'])
        benchmark_table['thirty_d']=list(bdf.iloc[3:]['Unnamed: 8'])
        benchmark_table['sixty_d']=list(bdf.iloc[3:]['Unnamed: 10'])
        benchmark_table['ninety_d']=list(bdf.iloc[3:]['Unnamed: 12'])
        benchmark_table['oneeighty_d']=list(bdf.iloc[3:]['Unnamed: 14'])
        benchmark_table['twoseventy_d']=list(bdf.iloc[3:]['Unnamed: 16'])
        benchmark_table['one_y']=list(bdf.iloc[3:]['Unnamed: 18'])
        benchmark_table['two_y']=list(bdf.iloc[3:]['Unnamed: 20'])
        benchmark_table['three_y']=list(bdf.iloc[3:]['Unnamed: 22'])
        benchmark_table['four_y']=list(bdf.iloc[3:]['Unnamed: 24'])
        benchmark_table['five_y']=list(bdf.iloc[3:]['Unnamed: 26'])
        benchmark_table['seven_y']=list(bdf.iloc[3:]['Unnamed: 28'])
        benchmark_table['ten_y']=list(bdf.iloc[3:]['Unnamed: 30'])
        benchmark_table['twelve_y']=([np.nan]*(bdf.iloc[3:]['Unnamed: 2'].shape[0]))
        benchmark_table['fifteen_y']=([np.nan]*(bdf.iloc[3:]['Unnamed: 2'].shape[0]))
        benchmark_table['twenty_y']=([np.nan]*(bdf.iloc[3:]['Unnamed: 2'].shape[0]))
        debt_benchmark = pd.concat([debt_benchmark,benchmark_table], axis=0)  

    benchmark_data = pd.concat([equity_benchmark,debt_benchmark], axis=0)

    all_etf_benchmark = os.listdir(current_dir+'/default/ETF_benchmark_values')
    etf_default_benchmark = pd.DataFrame(columns=['date','benchmark_name','benchmark_type','benchmark_category','YTD','one_d','seven_d','fourteen_d','thirty_d','sixty_d','ninety_d','oneeighty_d','twoseventy_d','one_y','two_y','three_y','four_y','five_y','seven_y','ten_y','twelve_y','fifteen_y'])
 
    for i in all_etf_benchmark :
        bdf = pd.read_csv(current_dir+'/default/ETF_benchmark_values//'+i)
 
        benchmark_table=pd.DataFrame(columns=['date','benchmark_name','benchmark_type','benchmark_category','YTD','one_d','seven_d','fourteen_d','thirty_d','sixty_d','ninety_d','oneeighty_d','twoseventy_d','one_y','two_y','three_y','four_y','five_y','seven_y','ten_y','twelve_y','fifteen_y'])
    # year-month-date
        benchmark_table['date']= [new_date]*bdf.iloc[3:]['Unnamed: 2'].shape[0]
        benchmark_table['benchmark_name']=list(bdf.iloc[3:][first_col])
        benchmark_table['benchmark_type']=['ETF']*(bdf.iloc[3:]['Unnamed: 2'].shape[0])
        benchmark_table['benchmark_category'] = [bdf.iloc[0, 0]] * (bdf.iloc[3:, bdf.columns.get_loc('Unnamed: 2')].shape[0])
        benchmark_table['YTD']=list(bdf.iloc[3:]['Unnamed: 34'])
        benchmark_table['one_d']=([np.nan]*(bdf.iloc[3:]['Unnamed: 2'].shape[0]))
        benchmark_table['seven_d']=([np.nan]*(bdf.iloc[3:]['Unnamed: 2'].shape[0]))
        benchmark_table['fourteen_d']=list(bdf.iloc[3:]['Unnamed: 2'])
        benchmark_table['thirty_d']=list(bdf.iloc[3:]['Unnamed: 4'])
        benchmark_table['sixty_d']=list(bdf.iloc[3:]['Unnamed: 6'])
        benchmark_table['ninety_d']=list(bdf.iloc[3:]['Unnamed: 8'])
        benchmark_table['oneeighty_d']=list(bdf.iloc[3:]['Unnamed: 10'])
        benchmark_table['twoseventy_d']=list(bdf.iloc[3:]['Unnamed: 12'])
        benchmark_table['one_y']=list(bdf.iloc[3:]['Unnamed: 18'])
        benchmark_table['two_y']=list(bdf.iloc[3:]['Unnamed: 20'])
        benchmark_table['three_y']=list(bdf.iloc[3:]['Unnamed: 22'])
        benchmark_table['four_y']=([np.nan]*(bdf.iloc[3:]['Unnamed: 2'].shape[0]))
        benchmark_table['five_y']=list(bdf.iloc[3:]['Unnamed: 24'])
        benchmark_table['seven_y']=list(bdf.iloc[3:]['Unnamed: 26'])
        benchmark_table['ten_y']=list(bdf.iloc[3:]['Unnamed: 28'])
        benchmark_table['twelve_y']=list(bdf.iloc[3:]['Unnamed: 30'])
        benchmark_table['fifteen_y']=list(bdf.iloc[3:]['Unnamed: 32'])
        benchmark_table['twenty_y']=([np.nan]*(bdf.iloc[3:]['Unnamed: 2'].shape[0]))
        etf_default_benchmark = pd.concat([etf_default_benchmark,benchmark_table], axis=0)
 
    all_index_benchmark = os.listdir(current_dir+'/default/Index_benchmark_values')
    
    
    # etf_default_benchmark = pd.DataFrame(columns=['benchmark_id','date','benchmark_name','benchmark_type','benchmark_category','YTD','one_d','seven_d','fourteen_d','thirty_d','sixty_d','ninety_d','oneeighty_d','twoseventy_d','one_y','two_y','three_y','four_y','five_y','seven_y','ten_y','twelve_y','fifteen_y'])
 
    for i in all_index_benchmark :
        bdf = pd.read_csv(current_dir+'/default/Index_benchmark_values/'+i)
 
        benchmark_table=pd.DataFrame(columns=['date','benchmark_name','benchmark_type','benchmark_category','YTD','one_d','seven_d','fourteen_d','thirty_d','sixty_d','ninety_d','oneeighty_d','twoseventy_d','one_y','two_y','three_y','four_y','five_y','seven_y','ten_y','twelve_y','fifteen_y'])
    # year-month-date
        benchmark_table['date']= [new_date]*bdf.iloc[3:]['Unnamed: 2'].shape[0]
        benchmark_table['benchmark_name']=list(bdf.iloc[3:][first_col])
        benchmark_table['benchmark_type']=['Index']*(bdf.iloc[3:]['Unnamed: 2'].shape[0])
        benchmark_table['benchmark_category'] = [bdf.iloc[0, 0]] * (bdf.iloc[3:]['Unnamed: 2'].shape[0])
        benchmark_table['YTD']=list(bdf.iloc[3:]['Unnamed: 34'])
        benchmark_table['one_d']=([np.nan]*(bdf.iloc[3:]['Unnamed: 2'].shape[0]))
        benchmark_table['seven_d']=([np.nan]*(bdf.iloc[3:]['Unnamed: 2'].shape[0]))
        benchmark_table['fourteen_d']=list(bdf.iloc[3:]['Unnamed: 2'])
        benchmark_table['thirty_d']=list(bdf.iloc[3:]['Unnamed: 4'])
        benchmark_table['sixty_d']=list(bdf.iloc[3:]['Unnamed: 6'])
        benchmark_table['ninety_d']=list(bdf.iloc[3:]['Unnamed: 8'])
        benchmark_table['oneeighty_d']=list(bdf.iloc[3:]['Unnamed: 10'])
        benchmark_table['twoseventy_d']=list(bdf.iloc[3:]['Unnamed: 12'])
        benchmark_table['one_y']=list(bdf.iloc[3:]['Unnamed: 18'])
        benchmark_table['two_y']=list(bdf.iloc[3:]['Unnamed: 20'])
        benchmark_table['three_y']=list(bdf.iloc[3:]['Unnamed: 22'])
        benchmark_table['four_y']=([np.nan]*(bdf.iloc[3:]['Unnamed: 2'].shape[0]))
        benchmark_table['five_y']=list(bdf.iloc[3:]['Unnamed: 24'])
        benchmark_table['seven_y']=list(bdf.iloc[3:]['Unnamed: 26'])
        benchmark_table['ten_y']=list(bdf.iloc[3:]['Unnamed: 28'])
        benchmark_table['twelve_y']=list(bdf.iloc[3:]['Unnamed: 30'])
        benchmark_table['fifteen_y']=list(bdf.iloc[3:]['Unnamed: 32'])
        benchmark_table['twenty_y']=([np.nan]*(bdf.iloc[3:]['Unnamed: 2'].shape[0]))
        etf_default_benchmark = pd.concat([etf_default_benchmark,benchmark_table], axis=0)
    
    new_category=[]
    new_benchmark=[]
    for i in range(benchmark_data.shape[0]):
        flag=0
        if(benchmark_data.iloc[i]['benchmark_type']=='Equity'):
            if(benchmark_data.iloc[i]['benchmark_category']=='Gennext'):
                new_category.append("Consumption Funds")
            elif(benchmark_data.iloc[i]['benchmark_category']=='Aggressive Hybrid Fund'):
                new_category.append("Aggressive Hybrid")
            elif(benchmark_data.iloc[i]['benchmark_category']=='ELSS Schemes'):
                new_category.append("ELSS")
            elif(benchmark_data.iloc[i]['benchmark_category']=='Focused Funds'):
                new_category.append("Focused Equity")
            elif(benchmark_data.iloc[i]['benchmark_category']=='Large & Mid Cap Funds'):
                new_category.append("Large and Midcap")
            elif(benchmark_data.iloc[i]['benchmark_category']=='Midcap Funds'):
                new_category.append("Mid Cap")
            elif(benchmark_data.iloc[i]['benchmark_category']=='Make in India'):
                new_category.append("Manufacturing Funds")
            elif(benchmark_data.iloc[i]['benchmark_category']=='Sector-MNC Schemes'):
                new_category.append("MNC Fund")
            elif(benchmark_data.iloc[i]['benchmark_category']=='Pharma & Healthcare Fund'):
                new_category.append("Pharma and Healthcare")
            elif(benchmark_data.iloc[i]['benchmark_category']=='Value Funds'):
                new_category.append("Pure Value")
            elif(benchmark_data.iloc[i]['benchmark_category']=='Special Opportunities'):
                new_category.append("Special Opportunities Fund")
            elif(benchmark_data.iloc[i]['benchmark_category']=='Digital Funds'):
                new_category.append("Technology")
            elif(benchmark_data.iloc[i]['benchmark_category']=='Retirement Fund 30'):
                new_category.append("Retirement Equity")
            elif(benchmark_data.iloc[i]['benchmark_category']=='Bal Bhavishya'):
                new_category.append("Children Equity")
            elif(benchmark_data.iloc[i]['benchmark_category']=='Transportation & Logistics'):
                new_category.append("Transportation and Logistics")
            elif(benchmark_data.iloc[i]['benchmark_category']=='Banking & Financial Services'):
                new_category.append("Banking and Financial Services")
            elif(benchmark_data.iloc[i]['benchmark_category']=='Dividend Yield Fund'):
                new_category.append("Dividend Yield")
            elif(benchmark_data.iloc[i]['benchmark_category']=='Flexi Cap Funds'):
                new_category.append("Flexi Cap")
            elif(benchmark_data.iloc[i]['benchmark_category']=='Infrastructure Funds'):
                new_category.append("Infrastructure")
            elif(benchmark_data.iloc[i]['benchmark_category']=='Large Cap Funds'):
                new_category.append("Large Cap")
            elif(benchmark_data.iloc[i]['benchmark_category']=='Small Cap Funds'):
                new_category.append("Small Cap")
            else:
                new_category.append(benchmark_data.iloc[i]['benchmark_category'])
    
        elif(benchmark_data.iloc[i]['benchmark_type']=='Debt'):
            if(benchmark_data.iloc[i]['benchmark_category']=='Credit Risk Fund'):
                new_category.append("Credit Risk Funds")
            elif(benchmark_data.iloc[i]['benchmark_category']=='Long Duration Fund'):
                new_category.append("Long Duration")
            elif(benchmark_data.iloc[i]['benchmark_category']=='Dynamic Bond Funds'):
                new_category.append("Dynamic Funds")
            elif((benchmark_data.iloc[i]['benchmark_category']=='Short Duration') & ( benchmark_data.iloc[i]['benchmark_name']=='NIFTY Short Duration Debt Index B-II')):
                new_benchmark.append("Nifty Short Duration Debt Index B-II")
                new_category.append("Short Duration")
                flag=1
            else:
                new_category.append(benchmark_data.iloc[i]['benchmark_category'])
        if(flag!=1):
            new_benchmark.append(benchmark_data.iloc[i]['benchmark_name'])
    benchmark_data['benchmark_category']=new_category
    benchmark_data['benchmark_name']=new_benchmark
    # benchmark_data['benchmark_id']=[i for i in range(benchmark_data.shape[0])]
   #return benchmark_data
    if not etf_default_benchmark.empty and not etf_default_benchmark.isna().all().all():
        benchmark_data = pd.concat([benchmark_data, etf_default_benchmark], axis=0)
    
    for index, row in benchmark_data.iterrows():
        if " (" in row['benchmark_name']:
            break_benchmark_name = ((row['benchmark_name']).split(" ("))[0]
            
            exist_in_benchmark_config = BenchmarkConfig.query.filter_by(benchmark_name = break_benchmark_name).first()
            print("adding previous date bench",exist_in_benchmark_config)
        else:
            exist_in_benchmark_config = BenchmarkConfig.query.filter_by(benchmark_name = row["benchmark_name"]).first()
            
        
        if exist_in_benchmark_config:
            new_benchmark_name = exist_in_benchmark_config.benchmark_name
            add_new_benchmark(new_benchmark_name)
            bechmark_existing = Benchmark.query.filter_by(name=new_benchmark_name).first()
            if bechmark_existing:
                check_benchmark_today_data = BenchmarkData.query.filter_by(benchmark_id = bechmark_existing.id).filter_by(date = row["date"]).first()
                if check_benchmark_today_data is None:
                    data = row.drop(labels=["date","benchmark_name"])
                    data_dict = replace_nan_with_placeholder(data.to_dict())
                    for key, value in data_dict.items():
                        try:
                            # Attempt to convert the value to a float
                            data_dict[key] = float(value)
                        except ValueError:
                            # If conversion fails, leave the value as is
                            pass

                    data_json = json.dumps(data_dict)
                    add_benchmark_data = BenchmarkData(benchmark_id = bechmark_existing.id, date = row["date"],data = data_json )
                    try:
                        db.session.add(add_benchmark_data)
                        db.session.commit()
                    except Exception as e:
                        print(e)
                        db.session.rollback()
    return
        
        



def add_new_benchmark(benchmark_name):
    is_benchmark_exist = Benchmark.query.filter_by(name = benchmark_name).first()
    if is_benchmark_exist is None:
        new_benchmark = Benchmark(name = benchmark_name)
        try:
            db.session.add(new_benchmark)
            db.session.commit()
        except Exception as e:
            print("unable to add new entry in benchmark table",e)
            db.session.rollback()
    pass
            