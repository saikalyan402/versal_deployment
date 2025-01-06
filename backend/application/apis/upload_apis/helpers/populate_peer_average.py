import os
import pandas as pd
import numpy as np

from application.model.model import db, CategoryRiskSet,Category,Scheme, Company
from application.helper import replace_nan_with_placeholder
import json

def populate_peer(current_dir,new_date,first_col):
    Debt_direct = os.listdir(current_dir+"/default//Schemes//Debt")
    Equity_regular = os.listdir(current_dir+"/default//Schemes//Equity")
    Debt_regular = os.listdir(current_dir+"/undefault//Schemes//Debt")
    Equity_direct = os.listdir(current_dir+"/undefault//Schemes//Equity")
    Etf = os.listdir(current_dir+"/default//Schemes//ETF")
    Indx = os.listdir(current_dir+"/default//Schemes//Index")
    filetype = [Debt_direct,Equity_regular,Debt_regular,Equity_direct]

    peer_avg_table = pd.DataFrame(columns=['date','peer_category','peer_type','peer_subtype','YTD','one_d','seven_d',
                                            'fourteen_d','thirty_d','sixty_d','ninety_d','oneeighty_d','twoseventy_d','one_y','two_y',
                                            'three_y','four_y','five_y','seven_y','ten_y','twelve_y','fifteen_y','inception'])
    for files in filetype:
        if files==Debt_direct:
            file_path = current_dir+"/default//Schemes//Debt//"
        elif files==Equity_regular:
            file_path = current_dir+"/default//Schemes//Equity//"
        elif files==Debt_regular:
            file_path = current_dir+"/undefault//Schemes//Debt//"
        else:
            file_path = current_dir+"/undefault//Schemes//Equity//"
        for file in files:
            peer_avg = pd.DataFrame(columns=['date','peer_category','peer_type','peer_subtype','YTD','one_d','seven_d',
                                                    'fourteen_d','thirty_d','sixty_d','ninety_d','oneeighty_d','twoseventy_d','one_y','two_y',
                                                    'three_y','four_y','five_y','seven_y','ten_y','twelve_y','fifteen_y','inception'])
            if file!='MasterSheet.csv':
                df = pd.read_csv(file_path+file)
                df.columns = df.iloc[1].values
                if 'Source :- ICRA Analytics Limited' in list(df.iloc[df.shape[0]-3]):
                    df.columns = df.iloc[4].values
                    df = df.iloc[5:df.shape[0]-11]
                if 'Corpus (In crs.)' not in df.columns:
                    continue
                else:
                    df = df.iloc[2:]
                    df = df.iloc[[-2]]
                
                
                df_category = (file).split(".")[0]
                try:
                    df_category = (df_category).split("- ")[1]
                except Exception as e:
                    pass
                df_category = df_category.strip()
                
                peer_avg['date'] = [new_date]
                peer_avg['peer_category'] = [df_category]
                if files==Debt_direct:
                    peer_avg['peer_type'] = 'Debt'
                    peer_avg['peer_subtype'] = 'Direct'
                elif files==Equity_regular:
                    peer_avg['peer_type'] = 'Equity'
                    peer_avg['peer_subtype'] = 'Regular'
                elif files==Debt_regular:
                    peer_avg['peer_type'] = 'Debt'
                    peer_avg['peer_subtype'] = 'Regular'
                else:
                    peer_avg['peer_type'] = 'Equity'
                    peer_avg['peer_subtype'] = 'Direct'
                if files==Debt_direct or files==Debt_regular:
                    peer_avg['YTD'] = '--'
                else:
                    peer_avg['YTD'] = (df.iloc[0]['YTD'])
                if files==Debt_direct or files==Debt_regular:
                    try:
                        peer_avg['one_d'] = (df.iloc[0]['1 Day'])
                    except:
                        peer_avg['one_d'] = '--'
                else:
                    peer_avg['one_d'] = '--'
                peer_avg['seven_d'] = (df.iloc[0]['1 Week'])
                peer_avg['fourteen_d'] = (df.iloc[0]['2 Weeks'])
                peer_avg['thirty_d'] = (df.iloc[0]['1 Month'])
                peer_avg['sixty_d'] = (df.iloc[0]['2 Months'])
                peer_avg['ninety_d'] = (df.iloc[0]['3 Months'])
                peer_avg['oneeighty_d'] = (df.iloc[0]['6 Months'])
                peer_avg['twoseventy_d'] = (df.iloc[0]['9 months'])
                peer_avg['one_y'] = (df.iloc[0]['1 Year'])
                peer_avg['two_y'] = (df.iloc[0]['2 Years'])
                peer_avg['three_y'] = (df.iloc[0]['3 Years'])
                if files==Debt_direct or files==Debt_regular:
                    try:
                        peer_avg['four_y'] = (df.iloc[0]['4 year '])
                    except:
                        peer_avg['four_y'] = '--'
                else:
                    peer_avg['four_y'] = '--'
                peer_avg['five_y'] = (df.iloc[0]['5 Years'])
                peer_avg['seven_y'] = (df.iloc[0]['7 Year'])
                peer_avg['ten_y'] = (df.iloc[0]['10 Years'])
                if files==Debt_direct or files==Debt_regular:
                    peer_avg['twelve_y'] = '--'
                    peer_avg['fifteen_y'] = '--'
                else:
                    peer_avg['twelve_y'] = (df.iloc[0]['12 years'])
                    peer_avg['fifteen_y'] = (df.iloc[0]['15 years'])
                peer_avg['inception'] = (df.iloc[0]['Since Inception'])
                peer_avg_table = pd.concat([peer_avg_table,peer_avg], axis=0)
    #return(Debt_peer_avg)
    
    for files in [Etf,Indx] :
        for filename in files:
            peer_avg = pd.DataFrame(columns=['date','peer_category','peer_type','peer_subtype','YTD','one_d','seven_d',
                                                    'fourteen_d','thirty_d','sixty_d','ninety_d','oneeighty_d','twoseventy_d','one_y','two_y',
                                                    'three_y','four_y','five_y','seven_y','ten_y','twelve_y','fifteen_y','inception'])
            if files==Etf:
                temp_df = pd.read_csv(current_dir+'/default/ETF_benchmark_values/'+filename)
            else:
                temp_df = pd.read_csv(current_dir+'/default/Index_benchmark_values/'+filename)
            df_category = filename.split(".")[0]
            df_category = df_category.strip()
            peer_avg['date'] = [new_date]
            peer_avg['peer_category'] = [df_category]
            if files==Etf:
                peer_avg['peer_type'] = 'ETF'
            else:
                peer_avg['peer_type'] = 'Index'
            peer_avg['peer_subtype'] = 'Regular'
            peer_avg['YTD'] = temp_df.iloc[2]['Unnamed: 34']
            peer_avg['one_d'] = '--'
            peer_avg['seven_d'] = temp_df.iloc[2]['Unnamed: 36']
            peer_avg['fourteen_d'] = temp_df.iloc[2]['Unnamed: 2']
            peer_avg['thirty_d'] = temp_df.iloc[2]['Unnamed: 4']
            peer_avg['sixty_d'] = temp_df.iloc[2]['Unnamed: 6']
            peer_avg['ninety_d'] = temp_df.iloc[2]['Unnamed: 8']
            peer_avg['oneeighty_d'] = temp_df.iloc[2]['Unnamed: 10']
            peer_avg['twoseventy_d'] = temp_df.iloc[2]['Unnamed: 12']
            peer_avg['one_y'] = temp_df.iloc[2]['Unnamed: 18']
            peer_avg['two_y'] = temp_df.iloc[2]['Unnamed: 20']
            peer_avg['three_y'] = temp_df.iloc[2]['Unnamed: 22']
            peer_avg['four_y'] = '--'
            peer_avg['five_y'] = temp_df.iloc[2]['Unnamed: 24']
            peer_avg['seven_y'] = temp_df.iloc[2]['Unnamed: 26']
            peer_avg['ten_y'] = temp_df.iloc[2]['Unnamed: 28']
            peer_avg['twelve_y'] = temp_df.iloc[2]['Unnamed: 30']
            peer_avg['fifteen_y'] = temp_df.iloc[2]['Unnamed: 32']
            peer_avg['inception'] = temp_df.iloc[2]['Unnamed: 16']
            peer_avg_table = pd.concat([peer_avg_table,peer_avg], axis=0)

    regular_equity_peers = os.listdir(current_dir+'/default//Equity_peer_set')
    direct_debt_peers = os.listdir(current_dir+'/default//Debt_peer_set')
    direct_equity_peers = os.listdir(current_dir+'/undefault//Equity_peer_set')
    regular_debt_peers = os.listdir(current_dir+'/undefault//Debt_peer_set')
    etf_peers = os.listdir(current_dir+'/default//Schemes//ETF')
    index_peers = os.listdir(current_dir+'/default//Schemes//Index')

    total_peer_set = pd.DataFrame(columns=['peer_category','peer_type','peer_subtype','peer_set'])
    for file in regular_equity_peers:
        bdf = pd.read_csv(current_dir+'/default//Equity_peer_set//'+file)
        peer = pd.DataFrame(columns=['peer_category','peer_type','peer_subtype','peer_set'])
        peer['peer_category'] = [file.split('.')[0]]
        peer['peer_type'] = 'Equity'
        peer['peer_subtype'] = 'Regular'
        peer_l = list(bdf[first_col].iloc[1:])
        peer['peer_set'] = [peer_l]
        total_peer_set = pd.concat([total_peer_set,peer], axis=0)
    for file in regular_debt_peers:
        bdf = pd.read_csv(current_dir+'/undefault//Debt_peer_set//'+file)
        peer = pd.DataFrame(columns=['peer_category','peer_type','peer_subtype','peer_set'])
        peer['peer_category'] = [file.split('.')[0]]
        peer['peer_type'] = 'Debt'
        peer['peer_subtype'] = 'Regular'
        peer_l = list(bdf[first_col].iloc[1:])
        peer['peer_set'] = [peer_l]
        total_peer_set = pd.concat([total_peer_set,peer], axis=0)
    for file in direct_debt_peers:
        bdf = pd.read_csv(current_dir+'/default//Debt_peer_set//'+file)
        peer = pd.DataFrame(columns=['peer_category','peer_type','peer_subtype','peer_set'])
        peer['peer_category'] = [file.split('.')[0]]
        peer['peer_type'] = 'Debt'
        peer['peer_subtype'] = 'Direct'
        peer_l = list(bdf[first_col].iloc[1:])
        peer['peer_set'] = [peer_l]
        total_peer_set = pd.concat([total_peer_set,peer], axis=0)
    for file in direct_equity_peers:
        bdf = pd.read_csv(current_dir+'/undefault//Equity_peer_set//'+file)
        peer = pd.DataFrame(columns=['peer_category','peer_type','peer_subtype','peer_set'])
        peer['peer_category'] = [file.split('.')[0]]
        peer['peer_type'] = 'Equity'
        peer['peer_subtype'] = 'Direct'
        peer_l = list(bdf[first_col].iloc[1:])
        peer['peer_set'] = [peer_l]
        total_peer_set = pd.concat([total_peer_set,peer], axis=0)
    for file in etf_peers:
        bdf = pd.read_csv(current_dir+'/default//Schemes//ETF//'+file)
        peer = pd.DataFrame(columns=['peer_category','peer_type','peer_subtype','peer_set'])
        peer['peer_category'] = [file.split('.')[0]]
        peer['peer_type'] = 'ETF'
        peer['peer_subtype'] = 'Regular'
        peer_l = list(bdf[first_col].iloc[1:])
        peer['peer_set'] = [peer_l]
        total_peer_set = pd.concat([total_peer_set,peer], axis=0)
    for file in index_peers:
        bdf = pd.read_csv(current_dir+'/default//Schemes//Index//'+file)
        peer = pd.DataFrame(columns=['peer_category','peer_type','peer_subtype','peer_set'])
        peer['peer_category'] = [file.split('.')[0]]
        peer['peer_type'] = 'Index'
        peer['peer_subtype'] = 'Regular'
        peer_l = list(bdf[first_col].iloc[1:])
        peer['peer_set'] = [peer_l]
        total_peer_set = pd.concat([total_peer_set,peer], axis=0)

    new_category=[]
    for i in range(total_peer_set.shape[0]):
        if(total_peer_set.iloc[i]['peer_type']=='Equity'):
            if(total_peer_set.iloc[i]['peer_category']=='Gennext'):
                new_category.append("Consumption Funds")
            elif(total_peer_set.iloc[i]['peer_category']=='Aggressive Hybrid Fund'):
                new_category.append("Aggressive Hybrid")
            elif(total_peer_set.iloc[i]['peer_category']=='ELSS Schemes'):
                new_category.append("ELSS")
            elif(total_peer_set.iloc[i]['peer_category']=='Focused Funds'):
                new_category.append("Focused Equity")
            elif(total_peer_set.iloc[i]['peer_category']=='Large & Mid Cap Funds'):
                new_category.append("Large and Midcap")
            elif(total_peer_set.iloc[i]['peer_category']=='Midcap Funds'):
                new_category.append("Mid Cap")
            elif(total_peer_set.iloc[i]['peer_category']=='Make in India'):
                new_category.append("Manufacturing Funds")
            elif(total_peer_set.iloc[i]['peer_category']=='Sector-MNC Schemes'):
                new_category.append("MNC Fund")
            elif(total_peer_set.iloc[i]['peer_category']=='Pharma & Healthcare Fund'):
                new_category.append("Pharma and Healthcare")
            elif(total_peer_set.iloc[i]['peer_category']=='Value Funds'):
                new_category.append("Pure Value")
            elif(total_peer_set.iloc[i]['peer_category']=='Special Opportunities'):
                new_category.append("Special Opportunities Fund")
            elif(total_peer_set.iloc[i]['peer_category']=='Digital Funds'):
                new_category.append("Technology")
            elif(total_peer_set.iloc[i]['peer_category']=='Retirement Fund 30'):
                new_category.append("Retirement Equity")
            elif(total_peer_set.iloc[i]['peer_category']=='Bal Bhavishya'):
                new_category.append("Children Equity")
            elif(total_peer_set.iloc[i]['peer_category']=='Transportation & Logistics'):
                new_category.append("Transportation and Logistics")
            elif(total_peer_set.iloc[i]['peer_category']=='Banking & Financial Services'):
                new_category.append("Banking and Financial Services")
            elif(total_peer_set.iloc[i]['peer_category']=='Dividend Yield Fund'):
                new_category.append("Dividend Yield")
            elif(total_peer_set.iloc[i]['peer_category']=='Flexi Cap Funds'):
                new_category.append("Flexi Cap")
            elif(total_peer_set.iloc[i]['peer_category']=='Infrastructure Funds'):
                new_category.append("Infrastructure")
            elif(total_peer_set.iloc[i]['peer_category']=='Large Cap Funds'):
                new_category.append("Large Cap")
            elif(total_peer_set.iloc[i]['peer_category']=='Small Cap Funds'):
                new_category.append("Small Cap")
            else:
                new_category.append(total_peer_set.iloc[i]['peer_category'])
    
        elif(total_peer_set.iloc[i]['peer_type']=='Debt'):
            if(total_peer_set.iloc[i]['peer_category']=='Credit Risk Fund'):
                new_category.append("Credit Risk Funds")
            elif(total_peer_set.iloc[i]['peer_category']=='Corporate Bond Fund'):
                new_category.append("Corporate Bond Funds")
            elif(total_peer_set.iloc[i]['peer_category']=='Corporate Bond'):
                new_category.append("Corporate Bond Funds")
            elif(total_peer_set.iloc[i]['peer_category']=='Long Duration Fund'):
                new_category.append("Long Duration")
            elif(total_peer_set.iloc[i]['peer_category']=='Dynamic Bond Funds'):
                new_category.append("Dynamic Funds")
            else:
                new_category.append(total_peer_set.iloc[i]['peer_category'])
        else:
            new_category.append(total_peer_set.iloc[i]['peer_category'])
    total_peer_set['peer_category']=new_category
    
    new_category=[]
    for i in range(peer_avg_table.shape[0]):
        if(peer_avg_table.iloc[i]['peer_category']=='Banking and PSU'):
            new_category.append("Banking & PSU")
        elif(peer_avg_table.iloc[i]['peer_category']=='Children Plan'):
            new_category.append("Children Equity")
        elif(peer_avg_table.iloc[i]['peer_category']=='Credit Risk Fund'):
            new_category.append("Credit Risk Funds")
        elif(peer_avg_table.iloc[i]['peer_category']=='Dynamic Bond Fund'):
            new_category.append("Dynamic Funds")
        elif(peer_avg_table.iloc[i]['peer_category']=='Corporate Bond Fund'):
            new_category.append("Corporate Bond Funds")
        elif(peer_avg_table.iloc[i]['peer_category']=='Corporate Bond'):
            new_category.append("Corporate Bond Funds")
        elif(peer_avg_table.iloc[i]['peer_category']=='Floater Fund'):
            new_category.append("Floater")
        elif(peer_avg_table.iloc[i]['peer_category']=='Money Market Fund'):
            new_category.append("Money Manager")
        elif(peer_avg_table.iloc[i]['peer_category']=='Regular Savings'):
            new_category.append("Conservative Hybrid")
        elif(peer_avg_table.iloc[i]['peer_category']=='Short Duration Fund'):
            new_category.append("Short Duration")
        elif(peer_avg_table.iloc[i]['peer_category']=='MNC Funds'):
            new_category.append("MNC Fund")
        elif(peer_avg_table.iloc[i]['peer_category']=='Transport and Logistics'):
            new_category.append("Transportation and Logistics")
        else:
            new_category.append(peer_avg_table.iloc[i]['peer_category'])
    peer_avg_table['peer_category']=new_category
    
    risk_peer_set=[]
    for i in range(peer_avg_table.shape[0]):
        peer_category = peer_avg_table['peer_category'].iloc[i]
        peer_type = peer_avg_table['peer_type'].iloc[i]
        peer_subtype = peer_avg_table['peer_subtype'].iloc[i]
        peer_set = list(total_peer_set.loc[(total_peer_set['peer_category']==peer_category) &(total_peer_set['peer_type']==peer_type )
                                          & (total_peer_set['peer_subtype']==peer_subtype )]['peer_set'])
        if(len(peer_set)==0):
            risk_peer_set.extend([["No Risk Set"]])
        else:
            risk_peer_set.extend(peer_set)

    risk_amc_set = []
    for i in range(len(risk_peer_set)):
        if risk_peer_set[i][0]=='No Risk Set':
            risk_amc_set.append(risk_peer_set[i])
        else:
            risk_amc = []
            for j in range(len(risk_peer_set[i])):
                first_word = risk_peer_set[i][j].split(" ")[0]
                if(first_word=='Aditya'):
                    risk_amc.append('ABSL')
                elif(first_word=='Bank'):
                    risk_amc.append('BOI')
                elif(first_word=='360'):
                    risk_amc.append('360 One')
                elif(first_word=='Parag'):
                    risk_amc.append("PPFAS")
                elif((first_word=='TATA')):
                    risk_amc.append("Tata")
                elif(first_word=='Old'):
                    risk_amc.append("Old Bridge")
                elif(first_word=='Templeton'):
                    risk_amc.append("Franklin")
                else:
                    risk_amc.append(first_word)
            risk_amc_set.append(risk_amc)
    
    risk_id = []
    risk_categories=list(peer_avg_table['peer_category'])
    risk_type=list(peer_avg_table['peer_type'])
    risk_subtype=list(peer_avg_table['peer_subtype'])
    pop = None
    for i in range(len(risk_amc_set)):
        if risk_amc_set[i][0]=='No Risk Set':
            risk_id.append([])
        else:
            risk_scheme_id = []
            for j in range(len(risk_amc_set[i])):
                
                scheme = Scheme.query.join(Company,Scheme.company_id == Company.id).join(Category,Scheme.category_id == Category.id).filter(Company.name==risk_amc_set[i][j],Category.name==risk_categories[i],Scheme.type==risk_type[i],Scheme.subtype==risk_subtype[i]).first()
                
                if scheme is None:
                    print("scheme not found")
                    pass
                else:
                    risk_scheme_id.append(scheme.id)
            risk_id.append(risk_scheme_id)
    peer_avg_table['risk_set'] = risk_id
    
    
    
    for index, row in peer_avg_table.iterrows():
        category = Category.query.filter_by(name=row["peer_category"]).first()
        
        if category:
            already_exists_risk_peer = CategoryRiskSet.query.filter_by(category_id = category.id, subtype = row["peer_subtype"], type = row["peer_type"]).filter_by(date = row["date"]).first()
            if already_exists_risk_peer is None:
                data = row.drop(labels=["date","peer_category","risk_set"])
                data_dict = replace_nan_with_placeholder(data.to_dict())
                for key, value in data_dict.items():
                    try:
                        # Attempt to convert the value to a float
                        data_dict[key] = float(value)
                    except ValueError:
                        # If conversion fails, leave the value as is
                        pass

                data_json = json.dumps(data_dict)
                new_category_risk_set = CategoryRiskSet(category_id = category.id, date = row["date"],subtype = row["peer_subtype"], type = row["peer_type"], risk_set = row["risk_set"],data=data_json)  
                try:
                    db.session.add(new_category_risk_set)
                    db.session.commit()
                except Exception as e:
                    print(e)
                    print("unable to add peer_avg")    
             
    return