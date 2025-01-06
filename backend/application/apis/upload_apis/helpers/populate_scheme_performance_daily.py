import os
import pandas as pd
import numpy as np
import json
from datetime import date

from application.model.model import db, Scheme, DailySchemePerformanceParamenter
from application.helper import replace_nan_with_placeholder



def populate_perf(current_dir,new_date,first_col):
    performance_parameters = pd.DataFrame(columns=['date','scheme_name','scheme_type','scheme_subtype','scheme_category',
                                        'scheme_nav','scheme_aum','YTD_return','YTD_rank','one_d_return','one_d_rank','seven_d_return',
                                        'seven_d_rank','fourteen_d_return','fourteen_d_rank','thirty_d_return','thirty_d_rank','sixty_d_return',
                                        'sixty_d_rank','ninety_d_return','ninety_d_rank','oneeighty_d_return','oneeighty_d_rank',
                                        'twoseventy_d_return','twoseventy_d_rank','one_y_return','one_y_rank','two_y_return','two_y_rank',
                                        'three_y_return','three_y_rank','four_y_return','four_y_rank','five_y_return','five_y_rank',
                                        'seven_y_return','seven_y_rank','ten_y_return','ten_y_rank','twelve_y_return','twelve_y_rank',
                                        'fifteen_y_return','fifteen_y_rank','inception_return','inception_rank'])
    All_Debt_files=os.listdir(current_dir+"/default/Schemes/Debt")
    for i in All_Debt_files:
        if i!='MasterSheet.csv':
            df = pd.read_csv(current_dir+"/default/Schemes/Debt/"+i)
            df.columns = df.iloc[1].values
            if 'Source :- ICRA Analytics Limited' in list(df.iloc[df.shape[0]-3]):
                df.columns = df.iloc[4].values
                df = df.iloc[5:df.shape[0]-11]
            if 'Corpus (In crs.)' not in df.columns:
                continue
            else:
                df = df.iloc[2:df.shape[0]-5]
            df_category = (i).split(".")[0]
            try:
                df_category = (df_category).split("- ")[1]
            except Exception as e:
                pass
            df_category = df_category.strip()
            perf_p = pd.DataFrame(columns=['date','scheme_name','scheme_type','scheme_subtype','scheme_category',
                                        'scheme_nav','scheme_aum','YTD_return','YTD_rank','one_d_return','one_d_rank','seven_d_return',
                                        'seven_d_rank','fourteen_d_return','fourteen_d_rank','thirty_d_return','thirty_d_rank','sixty_d_return',
                                        'sixty_d_rank','ninety_d_return','ninety_d_rank','oneeighty_d_return','oneeighty_d_rank',
                                        'twoseventy_d_return','twoseventy_d_rank','one_y_return','one_y_rank','two_y_return','two_y_rank',
                                        'three_y_return','three_y_rank','four_y_return','four_y_rank','five_y_return','five_y_rank',
                                        'seven_y_return','seven_y_rank','ten_y_return','ten_y_rank','twelve_y_return','twelve_y_rank',
                                        'fifteen_y_return','fifteen_y_rank','inception_return','inception_rank'])
            perf_p['date'] = [new_date]*(df.shape[0])
            perf_p['scheme_name'] = list(df['Scheme Name'])
            perf_p['scheme_type'] = ['Debt']*(df.shape[0])
            perf_p['scheme_subtype'] = ['Direct']*(df.shape[0])
            perf_p['scheme_category'] = [df_category]*(df.shape[0])
            perf_p['scheme_nav'] = list(df['NAV'])
            perf_p['scheme_aum'] = list(df['Corpus (In crs.)'])
            perf_p['YTD_return'] = ['--']*(df.shape[0])
            perf_p['YTD_rank'] = ['--']*(df.shape[0])
            try:
                perf_p['one_d_return'] = list(df['1 Day'])
                perf_p['one_d_rank'] = list(df['1 Day Rank'])
            except:
                perf_p['one_d_return'] = ['--']*(df.shape[0])
                perf_p['one_d_rank'] = ['--']*(df.shape[0])
            perf_p['seven_d_return'] = list(df['1 Week'])
            perf_p['seven_d_rank'] = list(df['1 Week Rank'])
            perf_p['fourteen_d_return'] = list(df['2 Weeks'])
            perf_p['fourteen_d_rank'] = list(df['2 Weeks Rank'])
            perf_p['thirty_d_return'] = list(df['1 Month'])
            perf_p['thirty_d_rank'] = list(df['1 Month Rank'])
            perf_p['sixty_d_return'] = list(df['2 Months'])
            perf_p['sixty_d_rank'] = list(df['2 Months Rank'])
            perf_p['ninety_d_return'] = list(df['3 Months'])
            perf_p['ninety_d_rank'] = list(df['3 Months Rank'])
            perf_p['oneeighty_d_return'] = list(df['6 Months'])
            perf_p['oneeighty_d_rank'] = list(df['6 Months Rank'])
            perf_p['twoseventy_d_return'] = list(df['9 months'])
            perf_p['twoseventy_d_rank'] = list(df['9 months Rank'])
            perf_p['one_y_return'] = list(df['1 Year'])
            perf_p['one_y_rank'] = list(df['1 Year Rank'])
            perf_p['two_y_return'] = list(df['2 Years'])
            perf_p['two_y_rank'] = list(df['2 Years Rank'])
            perf_p['three_y_return'] = list(df['3 Years'])
            perf_p['three_y_rank'] = list(df['3 Years Rank'])
            try:
                perf_p['four_y_return'] = list(df['4 year '])
                perf_p['four_y_rank'] = list(df['4 year  Rank'])
            except:
                perf_p['four_y_return'] = ['--']*(df.shape[0])
                perf_p['four_y_rank'] = ['--']*(df.shape[0])
            perf_p['five_y_return'] = list(df['5 Years'])
            perf_p['five_y_rank'] = list(df['5 Years Rank'])
            perf_p['seven_y_return'] = list(df['7 Year'])
            perf_p['seven_y_rank'] = list(df['7 Year Rank'])
            perf_p['ten_y_return'] = list(df['10 Years'])
            perf_p['ten_y_rank'] = list(df['10 Years Rank'])
            perf_p['twelve_y_return'] = ['--']*(df.shape[0])
            perf_p['twelve_y_rank'] = ['--']*(df.shape[0])
            perf_p['fifteen_y_return'] = ['--']*(df.shape[0])
            perf_p['fifteen_y_rank'] = ['--']*(df.shape[0])
            perf_p['inception_return'] = list(df['Since Inception'])
            perf_p['inception_rank'] = list(df['Since Inception Rank'])
            performance_parameters = pd.concat([performance_parameters,perf_p], axis=0, ignore_index=True)

    All_Equity_files=os.listdir(current_dir+"/default/Schemes/Equity")
    for i in All_Equity_files:
        if i!='MasterSheet.csv':
            df = pd.read_csv(current_dir+"/default/Schemes/Equity/"+i)
            df.columns = df.iloc[1].values
            if 'Source :- ICRA Analytics Limited' in list(df.iloc[df.shape[0]-3]):
                df.columns = df.iloc[4].values
                df = df.iloc[5:df.shape[0]-11]
            if 'Corpus (In crs.)' not in df.columns:
                continue
            else:
                df = df.iloc[2:df.shape[0]-5]

            df_category = (i).split(".")[0]
            df_category = df_category.strip()
            perf_p = pd.DataFrame(columns=['date','scheme_name','scheme_type','scheme_subtype','scheme_category',
                                        'scheme_nav','scheme_aum','YTD_return','YTD_rank','one_d_return','one_d_rank','seven_d_return',
                                        'seven_d_rank','fourteen_d_return','fourteen_d_rank','thirty_d_return','thirty_d_rank','sixty_d_return',
                                        'sixty_d_rank','ninety_d_return','ninety_d_rank','oneeighty_d_return','oneeighty_d_rank',
                                        'twoseventy_d_return','twoseventy_d_rank','one_y_return','one_y_rank','two_y_return','two_y_rank',
                                        'three_y_return','three_y_rank','four_y_return','four_y_rank','five_y_return','five_y_rank',
                                        'seven_y_return','seven_y_rank','ten_y_return','ten_y_rank','twelve_y_return','twelve_y_rank',
                                        'fifteen_y_return','fifteen_y_rank','inception_return','inception_rank'])
            perf_p['date'] = [new_date]*(df.shape[0])
            perf_p['scheme_name'] = list(df['Scheme Name'])
            perf_p['scheme_type'] = ['Equity']*(df.shape[0])
            perf_p['scheme_subtype'] = ['Regular']*(df.shape[0])
            perf_p['scheme_category'] = [df_category]*(df.shape[0])
            perf_p['scheme_nav'] = list(df['NAV'])
            perf_p['scheme_aum'] = list(df['Corpus (In crs.)'])
            perf_p['YTD_return'] = list(df['YTD'])
            perf_p['YTD_rank'] = list(df['YTD Rank'])
            perf_p['one_d_return'] = ['--']*(df.shape[0])
            perf_p['one_d_rank'] = ['--']*(df.shape[0])
            perf_p['seven_d_return'] = list(df['1 Week'])
            perf_p['seven_d_rank'] = list(df['1 Week Rank'])
            perf_p['fourteen_d_return'] = list(df['2 Weeks'])
            perf_p['fourteen_d_rank'] = list(df['2 Weeks Rank'])
            perf_p['thirty_d_return'] = list(df['1 Month'])
            perf_p['thirty_d_rank'] = list(df['1 Month Rank'])
            perf_p['sixty_d_return'] = list(df['2 Months'])
            perf_p['sixty_d_rank'] = list(df['2 Months Rank'])
            perf_p['ninety_d_return'] = list(df['3 Months'])
            perf_p['ninety_d_rank'] = list(df['3 Months Rank'])
            perf_p['oneeighty_d_return'] = list(df['6 Months'])
            perf_p['oneeighty_d_rank'] = list(df['6 Months Rank'])
            perf_p['twoseventy_d_return'] = list(df['9 months'])
            perf_p['twoseventy_d_rank'] = list(df['9 months Rank'])
            perf_p['one_y_return'] = list(df['1 Year'])
            perf_p['one_y_rank'] = list(df['1 Year Rank'])
            perf_p['two_y_return'] = list(df['2 Years'])
            perf_p['two_y_rank'] = list(df['2 Years Rank'])
            perf_p['three_y_return'] = list(df['3 Years'])
            perf_p['three_y_rank'] = list(df['3 Years Rank'])
            perf_p['four_y_return'] = ['--']*(df.shape[0])
            perf_p['four_y_rank'] = ['--']*(df.shape[0])
            perf_p['five_y_return'] = list(df['5 Years'])
            perf_p['five_y_rank'] = list(df['5 Years Rank'])
            perf_p['seven_y_return'] = list(df['7 Year'])
            perf_p['seven_y_rank'] = list(df['7 Year Rank'])
            perf_p['ten_y_return'] = list(df['10 Years'])
            perf_p['ten_y_rank'] = list(df['10 Years Rank'])
            perf_p['twelve_y_return'] = list(df['12 years'])
            perf_p['twelve_y_rank'] = list(df['12 years Rank'])
            perf_p['fifteen_y_return'] = list(df['15 years'])
            perf_p['fifteen_y_rank'] = list(df['15 years Rank'])
            perf_p['inception_return'] = list(df['Since Inception'])
            perf_p['inception_rank'] = list(df['Since Inception Rank'])
            performance_parameters = pd.concat([performance_parameters,perf_p], axis=0, ignore_index=True)

    All_Debt_files=os.listdir(current_dir+"/undefault/Schemes/Debt")
    for i in All_Debt_files:
        if i!='MasterSheet.csv':
            df = pd.read_csv(current_dir+"/undefault/Schemes/Debt/"+i)
            df.columns = df.iloc[1].values
            if 'Source :- ICRA Analytics Limited' in list(df.iloc[df.shape[0]-3]):
                df.columns = df.iloc[4].values
                df = df.iloc[5:df.shape[0]-11]
            if 'Corpus (In crs.)' not in df.columns:
                continue
            else:
                df = df.iloc[2:df.shape[0]-5]

            df_category = (i).split(".")[0]
            try:
                df_category = (df_category).split("- ")[1]
            except Exception as e:
                pass
            df_category = df_category.strip()
            perf_p = pd.DataFrame(columns=['date','scheme_name','scheme_type','scheme_subtype','scheme_category',
                                        'scheme_nav','scheme_aum','YTD_return','YTD_rank','one_d_return','one_d_rank','seven_d_return',
                                        'seven_d_rank','fourteen_d_return','fourteen_d_rank','thirty_d_return','thirty_d_rank','sixty_d_return',
                                        'sixty_d_rank','ninety_d_return','ninety_d_rank','oneeighty_d_return','oneeighty_d_rank',
                                        'twoseventy_d_return','twoseventy_d_rank','one_y_return','one_y_rank','two_y_return','two_y_rank',
                                        'three_y_return','three_y_rank','four_y_return','four_y_rank','five_y_return','five_y_rank',
                                        'seven_y_return','seven_y_rank','ten_y_return','ten_y_rank','twelve_y_return','twelve_y_rank',
                                        'fifteen_y_return','fifteen_y_rank','inception_return','inception_rank'])
            perf_p['date'] = [new_date]*(df.shape[0])
            perf_p['scheme_name'] = list(df['Scheme Name'])
            perf_p['scheme_type'] = ['Debt']*(df.shape[0])
            perf_p['scheme_subtype'] = ['Regular']*(df.shape[0])
            perf_p['scheme_category'] = [df_category]*(df.shape[0])
            perf_p['scheme_nav'] = list(df['NAV'])
            perf_p['scheme_aum'] = list(df['Corpus (In crs.)'])
            perf_p['YTD_return'] = ['--']*(df.shape[0])
            perf_p['YTD_rank'] = ['--']*(df.shape[0])
            try:
                perf_p['one_d_return'] = list(df['1 Day'])
                perf_p['one_d_rank'] = list(df['1 Day Rank'])
            except:
                perf_p['one_d_return'] = ['--']*(df.shape[0])
                perf_p['one_d_rank'] = ['--']*(df.shape[0])
            perf_p['seven_d_return'] = list(df['1 Week'])
            perf_p['seven_d_rank'] = list(df['1 Week Rank'])
            perf_p['fourteen_d_return'] = list(df['2 Weeks'])
            perf_p['fourteen_d_rank'] = list(df['2 Weeks Rank'])
            perf_p['thirty_d_return'] = list(df['1 Month'])
            perf_p['thirty_d_rank'] = list(df['1 Month Rank'])
            perf_p['sixty_d_return'] = list(df['2 Months'])
            perf_p['sixty_d_rank'] = list(df['2 Months Rank'])
            perf_p['ninety_d_return'] = list(df['3 Months'])
            perf_p['ninety_d_rank'] = list(df['3 Months Rank'])
            perf_p['oneeighty_d_return'] = list(df['6 Months'])
            perf_p['oneeighty_d_rank'] = list(df['6 Months Rank'])
            perf_p['twoseventy_d_return'] = list(df['9 months'])
            perf_p['twoseventy_d_rank'] = list(df['9 months Rank'])
            perf_p['one_y_return'] = list(df['1 Year'])
            perf_p['one_y_rank'] = list(df['1 Year Rank'])
            perf_p['two_y_return'] = list(df['2 Years'])
            perf_p['two_y_rank'] = list(df['2 Years Rank'])
            perf_p['three_y_return'] = list(df['3 Years'])
            perf_p['three_y_rank'] = list(df['3 Years Rank'])
            perf_p['four_y_return'] = list(df['4 year '])
            perf_p['four_y_rank'] = list(df['4 year  Rank'])
            perf_p['five_y_return'] = list(df['5 Years'])
            perf_p['five_y_rank'] = list(df['5 Years Rank'])
            perf_p['seven_y_return'] = list(df['7 Year'])
            perf_p['seven_y_rank'] = list(df['7 Year Rank'])
            perf_p['ten_y_return'] = list(df['10 Years'])
            perf_p['ten_y_rank'] = list(df['10 Years Rank'])
            perf_p['twelve_y_return'] = ['--']*(df.shape[0])
            perf_p['twelve_y_rank'] = ['--']*(df.shape[0])
            perf_p['fifteen_y_return'] = ['--']*(df.shape[0])
            perf_p['fifteen_y_rank'] = ['--']*(df.shape[0])
            perf_p['inception_return'] = list(df['Since Inception'])
            perf_p['inception_rank'] = list(df['Since Inception Rank'])
            performance_parameters = pd.concat([performance_parameters,perf_p], axis=0, ignore_index=True)

    All_Equity_files=os.listdir(current_dir+"/undefault/Schemes/Equity")
    for i in All_Equity_files:
        if i!='MasterSheet.csv':
            df = pd.read_csv(current_dir+"/undefault/Schemes/Equity/"+i)
            df.columns = df.iloc[1].values
            if 'Source :- ICRA Analytics Limited' in list(df.iloc[df.shape[0]-3]):
                df.columns = df.iloc[4].values
                df = df.iloc[5:df.shape[0]-11]
            if 'Corpus (In crs.)' not in df.columns:
                continue
            else:
                df = df.iloc[2:df.shape[0]-5]

            df_category = (i).split(".")[0]
            df_category = df_category.strip()
            perf_p = pd.DataFrame(columns=['date','scheme_name','scheme_type','scheme_subtype','scheme_category',
                                        'scheme_nav','scheme_aum','YTD_return','YTD_rank','one_d_return','one_d_rank','seven_d_return',
                                        'seven_d_rank','fourteen_d_return','fourteen_d_rank','thirty_d_return','thirty_d_rank','sixty_d_return',
                                        'sixty_d_rank','ninety_d_return','ninety_d_rank','oneeighty_d_return','oneeighty_d_rank',
                                        'twoseventy_d_return','twoseventy_d_rank','one_y_return','one_y_rank','two_y_return','two_y_rank',
                                        'three_y_return','three_y_rank','four_y_return','four_y_rank','five_y_return','five_y_rank',
                                        'seven_y_return','seven_y_rank','ten_y_return','ten_y_rank','twelve_y_return','twelve_y_rank',
                                        'fifteen_y_return','fifteen_y_rank','inception_return','inception_rank'])
            perf_p['date'] = [new_date]*(df.shape[0])
            perf_p['scheme_name'] = list(df['Scheme Name'])
            perf_p['scheme_type'] = ['Equity']*(df.shape[0])
            perf_p['scheme_subtype'] = ['Direct']*(df.shape[0])
            perf_p['scheme_category'] = [df_category]*(df.shape[0])
            perf_p['scheme_nav'] = list(df['NAV'])
            perf_p['scheme_aum'] = list(df['Corpus (In crs.)'])
            perf_p['YTD_return'] = list(df['YTD'])
            perf_p['YTD_rank'] = list(df['YTD Rank'])
            perf_p['one_d_return'] = ['--']*(df.shape[0])
            perf_p['one_d_rank'] = ['--']*(df.shape[0])
            perf_p['seven_d_return'] = list(df['1 Week'])
            perf_p['seven_d_rank'] = list(df['1 Week Rank'])
            perf_p['fourteen_d_return'] = list(df['2 Weeks'])
            perf_p['fourteen_d_rank'] = list(df['2 Weeks Rank'])
            perf_p['thirty_d_return'] = list(df['1 Month'])
            perf_p['thirty_d_rank'] = list(df['1 Month Rank'])
            perf_p['sixty_d_return'] = list(df['2 Months'])
            perf_p['sixty_d_rank'] = list(df['2 Months Rank'])
            perf_p['ninety_d_return'] = list(df['3 Months'])
            perf_p['ninety_d_rank'] = list(df['3 Months Rank'])
            perf_p['oneeighty_d_return'] = list(df['6 Months'])
            perf_p['oneeighty_d_rank'] = list(df['6 Months Rank'])
            perf_p['twoseventy_d_return'] = list(df['9 months'])
            perf_p['twoseventy_d_rank'] = list(df['9 months Rank'])
            perf_p['one_y_return'] = list(df['1 Year'])
            perf_p['one_y_rank'] = list(df['1 Year Rank'])
            perf_p['two_y_return'] = list(df['2 Years'])
            perf_p['two_y_rank'] = list(df['2 Years Rank'])
            perf_p['three_y_return'] = list(df['3 Years'])
            perf_p['three_y_rank'] = list(df['3 Years Rank'])
            perf_p['four_y_return'] = ['--']*(df.shape[0])
            perf_p['four_y_rank'] = ['--']*(df.shape[0])
            perf_p['five_y_return'] = list(df['5 Years'])
            perf_p['five_y_rank'] = list(df['5 Years Rank'])
            perf_p['seven_y_return'] = list(df['7 Year'])
            perf_p['seven_y_rank'] = list(df['7 Year Rank'])
            perf_p['ten_y_return'] = list(df['10 Years'])
            perf_p['ten_y_rank'] = list(df['10 Years Rank'])
            perf_p['twelve_y_return'] = list(df['12 years'])
            perf_p['twelve_y_rank'] = list(df['12 years Rank'])
            perf_p['fifteen_y_return'] = list(df['15 years'])
            perf_p['fifteen_y_rank'] = list(df['15 years Rank'])
            perf_p['inception_return'] = list(df['Since Inception'])
            perf_p['inception_rank'] = list(df['Since Inception Rank'])
            performance_parameters = pd.concat([performance_parameters,perf_p], axis=0, ignore_index=True)

    All_Etf_files = os.listdir(current_dir+"/default/Schemes/ETF")
    All_Index_files = os.listdir(current_dir+"/default/Schemes/Index")
    filetype = [All_Etf_files,All_Index_files]
    for files in filetype:
        if files==All_Etf_files:
            filepath = current_dir+"/default/Schemes/ETF/"
        else:
            filepath = current_dir+"/default/Schemes/Index/"
        for file in files:
            etf_df = pd.DataFrame(columns=['scheme_name','date','scheme_type','scheme_subtype','scheme_category','scheme_nav','scheme_aum','YTD_return','YTD_rank','one_d_return','one_d_rank','seven_d_return',
                            'seven_d_rank','fourteen_d_return','fourteen_d_rank','thirty_d_return','thirty_d_rank','sixty_d_return','sixty_d_rank','ninety_d_return','ninety_d_rank',
                            'oneeighty_d_return','oneeighty_d_rank','twoseventy_d_return','twoseventy_d_rank','one_y_return','one_y_rank','two_y_return','two_y_rank','three_y_return',
                            'three_y_rank','four_y_return','four_y_rank','five_y_return','five_y_rank','seven_y_return','seven_y_rank','ten_y_return','ten_y_rank','twelve_y_return',
                            'twelve_y_rank','fifteen_y_return','fifteen_y_rank','inception_return','inception_rank'])
            temp_df = pd.read_csv(filepath+file)
            
            etf_df['scheme_name'] = list(temp_df.iloc[1:][first_col])
            etf_df['date'] = [new_date]*((temp_df.iloc[1:][first_col]).shape[0])
            if files==All_Etf_files:
                etf_df['scheme_type'] = ["ETF"]*((temp_df.iloc[1:][first_col]).shape[0])
            else:
                etf_df['scheme_type'] = ["Index"]*((temp_df.iloc[1:][first_col]).shape[0])   
            etf_df['scheme_subtype'] = ['Regular']*((temp_df.iloc[1:][first_col]).shape[0])
            etf_df['scheme_category'] = file.split('.')[0]
            etf_df['scheme_nav'] = ['--']*((temp_df.iloc[1:][first_col]).shape[0])
            etf_df['scheme_aum'] = list(temp_df.iloc[1:]['Unnamed: 1'])
            etf_df['YTD_return'] = list(temp_df.iloc[1:]['Unnamed: 34'])
            etf_df['YTD_rank'] = list(temp_df.iloc[1:]['Unnamed: 35'])
            etf_df['one_d_return'] = ['--']*((temp_df.iloc[1:][first_col]).shape[0])
            etf_df['one_d_rank'] = ['--']*((temp_df.iloc[1:][first_col]).shape[0])
            etf_df['seven_d_return'] = list(temp_df.iloc[1:]['Unnamed: 36'])
            etf_df['seven_d_rank'] = list(temp_df.iloc[1:]['Unnamed: 37'])
            etf_df['fourteen_d_return'] = list(temp_df.iloc[1:]['Unnamed: 2'])
            etf_df['fourteen_d_rank'] = list(temp_df.iloc[1:]['Unnamed: 3'])
            etf_df['thirty_d_return'] = list(temp_df.iloc[1:]['Unnamed: 4'])
            etf_df['thirty_d_rank'] = list(temp_df.iloc[1:]['Unnamed: 5'])
            etf_df['sixty_d_return'] = list(temp_df.iloc[1:]['Unnamed: 6'])
            etf_df['sixty_d_rank']= list(temp_df.iloc[1:]['Unnamed: 7'])
            etf_df['ninety_d_return'] = list(temp_df.iloc[1:]['Unnamed: 8'])
            etf_df['ninety_d_rank'] = list(temp_df.iloc[1:]['Unnamed: 9'])
            etf_df['oneeighty_d_return'] = list(temp_df.iloc[1:]['Unnamed: 10'])
            etf_df['oneeighty_d_rank'] = list(temp_df.iloc[1:]['Unnamed: 11'])
            etf_df['twoseventy_d_return'] = list(temp_df.iloc[1:]['Unnamed: 12'])
            etf_df['twoseventy_d_rank'] = list(temp_df.iloc[1:]['Unnamed: 13'])
            etf_df['one_y_return'] = list(temp_df.iloc[1:]['Unnamed: 18'])
            etf_df['one_y_rank'] = list(temp_df.iloc[1:]['Unnamed: 19'])
            etf_df['two_y_return'] = list(temp_df.iloc[1:]['Unnamed: 20'])
            etf_df['two_y_rank'] = list(temp_df.iloc[1:]['Unnamed: 21'])
            etf_df['three_y_return'] = list(temp_df.iloc[1:]['Unnamed: 22'])
            etf_df['three_y_rank'] = list(temp_df.iloc[1:]['Unnamed: 23'])
            etf_df['four_y_return'] = ['--']*((temp_df.iloc[1:][first_col]).shape[0])
            etf_df['four_y_rank'] = ['--']*((temp_df.iloc[1:][first_col]).shape[0])
            etf_df['five_y_return'] = list(temp_df.iloc[1:]['Unnamed: 24'])
            etf_df['five_y_rank'] = list(temp_df.iloc[1:]['Unnamed: 25'])
            etf_df['seven_y_return'] = list(temp_df.iloc[1:]['Unnamed: 26'])
            etf_df['seven_y_rank'] = list(temp_df.iloc[1:]['Unnamed: 27'])
            etf_df['ten_y_return'] = list(temp_df.iloc[1:]['Unnamed: 28'])
            etf_df['ten_y_rank'] = list(temp_df.iloc[1:]['Unnamed: 29'])
            etf_df['twelve_y_return'] = list(temp_df.iloc[1:]['Unnamed: 30'])
            etf_df['twelve_y_rank'] = list(temp_df.iloc[1:]['Unnamed: 31'])
            etf_df['fifteen_y_return'] = list(temp_df.iloc[1:]['Unnamed: 32'])
            etf_df['fifteen_y_rank'] = list(temp_df.iloc[1:]['Unnamed: 33'])
            etf_df['inception_return'] = list(temp_df.iloc[1:]['Unnamed: 16'])
            etf_df['inception_rank'] = list(temp_df.iloc[1:]['Unnamed: 17'])
            performance_parameters = pd.concat([performance_parameters,etf_df], axis=0)

    performance_parameters.drop(performance_parameters.loc[performance_parameters['scheme_name']=='IDBI Equity Advantage Fund - Reg - Growth'].index,inplace=True)
    new_category=[]
    for i in range(performance_parameters.shape[0]):
        if(performance_parameters.iloc[i]['scheme_category']=='Banking and PSU'):
            new_category.append("Banking & PSU")
        elif(performance_parameters.iloc[i]['scheme_category']=='Children Plan'):
            new_category.append("Children Equity")
        elif(performance_parameters.iloc[i]['scheme_category']=='Credit Risk Fund'):
            new_category.append("Credit Risk Funds")
        elif(performance_parameters.iloc[i]['scheme_category']=='Dynamic Bond Fund'):
            new_category.append("Dynamic Funds")
        elif(performance_parameters.iloc[i]['scheme_category']=='Corporate Bond Fund'):
            new_category.append("Corporate Bond Funds")
        elif(performance_parameters.iloc[i]['scheme_category']=='Corporate Bond'):
            new_category.append("Corporate Bond Funds")
        elif(performance_parameters.iloc[i]['scheme_category']=='Floater Fund'):
            new_category.append("Floater")
        elif(performance_parameters.iloc[i]['scheme_category']=='Money Market Fund'):
            new_category.append("Money Manager")
        elif(performance_parameters.iloc[i]['scheme_category']=='Regular Savings'):
            new_category.append("Conservative Hybrid")
        elif(performance_parameters.iloc[i]['scheme_category']=='Short Duration Fund'):
            new_category.append("Short Duration")
        elif(performance_parameters.iloc[i]['scheme_category']=='MNC Funds'):
            new_category.append("MNC Fund")
        elif(performance_parameters.iloc[i]['scheme_category']=='Transport and Logistics'):
            new_category.append("Transportation and Logistics")
        else:
            new_category.append(performance_parameters.iloc[i]['scheme_category'])
        
    performance_parameters['scheme_category']=new_category

    for i in range(performance_parameters.shape[0]):
        sc_name = performance_parameters.iloc[i]['scheme_name']
        scheme = Scheme.query.filter_by(name=sc_name).first()
        if scheme:
            scheme_id = scheme.id
            is_today_data_exists = DailySchemePerformanceParamenter.query.filter_by(scheme_id = scheme_id).filter_by(performance_date=performance_parameters.iloc[i]['date']).first()
            if is_today_data_exists is None:
                data_dict = performance_parameters.iloc[i].to_dict()
                data_dict = convert_dates_to_strings(data_dict)  # Convert dates to strings
                data_dict = replace_nan_with_placeholder(data_dict)
                for key, value in data_dict.items():
                    try:
                        # Attempt to convert the value to a float
                        data_dict[key] = float(value)
                    except ValueError:
                        # If conversion fails, leave the value as is
                        pass

                data_json = json.dumps(data_dict)

                today_scheme_params = DailySchemePerformanceParamenter(
                    scheme_id=scheme_id,
                    performance_date=performance_parameters.iloc[i]['date'],
                    data=data_json
                )
                
                try:
                    db.session.add(today_scheme_params)
                    db.session.commit()
                except Exception as e:
                    print(e)
                    db.session.rollback()


    return
    
    
def convert_dates_to_strings(data_dict):
    for key, value in data_dict.items():
        if isinstance(value, date):
            data_dict[key] = value.isoformat()
    return data_dict