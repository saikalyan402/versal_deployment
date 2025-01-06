import pandas as pd
from pandas import read_excel
import sqlite3
from datetime import date, timedelta
import numpy as np
import os
from datetime import datetime
import xlwings as xw
import openpyxl


def clean_all(current_dir):
        All_Debt_dB=os.listdir(current_dir+"/default//Debt_benchmark_values")
        All_Equity_dB=os.listdir(current_dir+"/default//Equity_benchmark_values")
        All_Debt_dP=os.listdir(current_dir+"/default//Debt_peer_set")
        All_Equity_dP=os.listdir(current_dir+"/default//Equity_peer_set")
        All_Debt_dS=os.listdir(current_dir+"/default//Schemes//Debt")
        All_Equity_dS=os.listdir(current_dir+"/default//Schemes//Equity")
        All_Etf_S=os.listdir(current_dir+"/default//Schemes//ETF")
        All_Index_S=os.listdir(current_dir+"/default//Schemes//Index")
        All_Etf_b=os.listdir(current_dir+"/default//ETF_benchmark_values")
        All_Index_b=os.listdir(current_dir+"/default//Index_benchmark_values")
        All_Debt_B=os.listdir(current_dir+"/undefault//Debt_benchmark_values")
        All_Equity_B=os.listdir(current_dir+"/undefault//Equity_benchmark_values")
        All_Debt_P=os.listdir(current_dir+"/undefault//Debt_peer_set")
        All_Equity_P=os.listdir(current_dir+"/undefault//Equity_peer_set")
        All_Debt_S=os.listdir(current_dir+"/undefault//Schemes//Debt")
        All_Equity_S=os.listdir(current_dir+"/undefault//Schemes//Equity")
        xyz = os.listdir(current_dir+"/Value_Research")
        for i in xyz:
            path = current_dir+"/Value_Research//"+i
            os.remove(path)
        for i in All_Etf_S:
            path = current_dir+"/default//Schemes//ETF//"+i
            os.remove(path)
        for i in All_Index_S:
            path = current_dir+"/default//Schemes//Index//"+i
            os.remove(path)
        for i in All_Etf_b:
            path = current_dir+"/default//ETF_benchmark_values//"+i
            os.remove(path)
        for i in All_Index_b:
            path = current_dir+"/default//Index_benchmark_values//"+i
            os.remove(path)
        for i in All_Debt_dB:
            path=current_dir+"/default//Debt_benchmark_values//"+i
            os.remove(path)
        for i in All_Debt_dP:
            path=current_dir+"/default//Debt_peer_set//"+i
            os.remove(path)
        for i in All_Equity_dB:
            path=current_dir+"/default//Equity_benchmark_values//"+i
            os.remove(path)
        for i in All_Equity_dP:
            path=current_dir+"/default//Equity_peer_set//"+i
            os.remove(path)
        for i in All_Equity_dS:
            path=current_dir+"/default//Schemes//Equity//"+i
            os.remove(path)
        for i in All_Debt_dS:
            path=current_dir+"/default//Schemes//Debt//"+i
            os.remove(path)
        for i in All_Debt_B:
            path=current_dir+"/undefault//Debt_benchmark_values//"+i
            os.remove(path)
        for i in All_Debt_P:
            path=current_dir+"/undefault//Debt_peer_set//"+i
            os.remove(path)
        for i in All_Equity_B:
            path=current_dir+"/undefault//Equity_benchmark_values//"+i
            os.remove(path)
        for i in All_Equity_P:
            path=current_dir+"/undefault//Equity_peer_set//"+i
            os.remove(path)
        for i in All_Equity_S:
            path=current_dir+"/undefault//Schemes//Equity//"+i
            os.remove(path)
        for i in All_Debt_S:
            path=current_dir+"/undefault//Schemes//Debt//"+i
            os.remove(path)
            
            
def unprotect_files(current_dir):
    
    try:
        xw.App(visible=False)
        print("xlwings engine initialized successfully.")
    except Exception as e:
        print(f"Error initializing xlwings engine: {e}")
        return

    # Path to the Excel file
    for i in os.listdir(current_dir+"/MFI"):
        file_path = current_dir+"/MFI//"+i
        password = ''  # Password for the protected sheets

        # Open the Excel application
        app = xw.App(visible=False)
        wb = app.books.open(file_path)

        try:
            # Loop through all sheets in the workbook
            for sheet in wb.sheets:
                try:
                    # Unprotect the sheet
                    sheet.api.Unprotect(Password=password)

                    print(f"Unprotected sheet: {sheet.name}")
                except Exception as e:
                    print(f"Failed to unprotect sheet {sheet.name}: {e}")

            # Save the changes
            wb.save()
            print("All sheets have been unprotected and saved.")

        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            # Close the workbook and quit the Excel application
            wb.close()
            app.quit()


def fun(current_dir):
    from datetime import date
    import os
    
    all_vr = os.listdir(current_dir + "/VR")
    fles = []
    first_col = None
    new_date = None
    
    for i in all_vr:
        day = i[10:12]
        month = i[12:14]
        year = i[14:18]
        
        if not (day.isdigit() and month.isdigit() and year.isdigit()):
            print(f"Skipping file {i} due to invalid date format.")
            continue
        
        mfi_debt_direct = current_dir + "/MFI/" + day + '-' + month + '-' + year + '-Debt.xlsx'
        mfi_equity_regular = current_dir + "/MFI/" + day + '-' + month + '-' + year + '-Equity.xlsx'
        mfi_debt_regular = current_dir + "/MFI/" + day + '-' + month + '-' + year + ' Debt regular.xlsx'
        mfi_equity_direct = current_dir + "/MFI/" + day + '-' + month + '-' + year + ' Equity direct.xlsx'
        vr_file = current_dir + "/VR/" + i
        
        fles.extend([mfi_debt_direct, mfi_equity_regular, mfi_debt_regular, mfi_equity_direct, vr_file])
        
        new_date = date(int(year), int(month), int(day))
        formatted_date = new_date.strftime('%d-%b-%y')
        first_col = 'Daily Competition Returns Comparison Report as of ' + str(formatted_date)
    
    return (fles, new_date, first_col)
    

def read_files(current_dir,fles,first_col):
    # Read Excel file
    for file in fles:
        xls_file = pd.ExcelFile(file) # Replace with your Excel file path
    
    # Iterate through each sheet and convert to CSV
        for sheet_name in xls_file.sheet_names:
            df = pd.read_excel(xls_file, sheet_name=sheet_name)
            if '-Debt' in file:
                df.to_csv(current_dir+'/default/Schemes/Debt/'+sheet_name+'.csv', index=False)
            elif '-Equity' in file:
                df.to_csv(current_dir+'/default/Schemes/Equity/'+sheet_name+'.csv', index=False)
            elif ' Debt regular' in file:
                df.to_csv(current_dir+'/undefault/Schemes/Debt/'+sheet_name+'.csv', index=False)
            elif ' Equity direct' in file:
                df.to_csv(current_dir+'/undefault/Schemes/Equity/'+sheet_name+'.csv', index=False)
            else:
                df.to_csv(current_dir+'/Value_Research/'+sheet_name+'.csv', index=False)

    print("MFI Sheets created")

    df = pd.read_csv(current_dir+'/Value_Research/Ret. Compr.(Debt) - Dir.csv')
    overnight_index=int(df.loc[df[first_col]=="Overnight Fund"].index[0])
    for i in range(overnight_index,overnight_index+20):
        value=str(df[first_col].iloc[i])
        if(value=="nan"):
            del_index=i
            break
    df = df.drop(del_index)
    idx = df[df[first_col]=='CRISIL IBX AAA Index – March 2024'].index[0]
    df = df.drop(df.index[idx-1:idx+5])
    
    df[first_col] = df[first_col].str.replace('–','_')
    df = df[~df.iloc[:,0].str.contains('Q1 cutoff',case=False,na=False)]
    df.to_csv(current_dir + '/Value_Research/Ret. Compr.(Debt) - Dir.csv', index=False)

    df = pd.read_csv(current_dir+'/Value_Research/Ret. Compr.(Debt) - Reg.csv')
    overnight_index=int(df.loc[df[first_col]=="Overnight Fund"].index[0])
    for i in range(overnight_index,overnight_index+20):
        value=str(df[first_col].iloc[i])
        if(value=="nan"):
            del_index=i
            break
    df = df.drop(del_index)
    idx = df[df[first_col]=='CRISIL IBX AAA Index – March 2024'].index[0]
    df = df.drop(df.index[idx-1:idx+5])
    
    df[first_col] = df[first_col].str.replace('–','_')
    df = df[~df.iloc[:,0].str.contains('Q1 cutoff',case=False,na=False)]
    df.to_csv(current_dir + '/Value_Research/Ret. Compr.(Debt) - Reg.csv', index=False)

    df = pd.read_csv(current_dir+'/Value_Research/Ret. Compr.(Equity) - Reg.csv')
    df = df[~df.iloc[:,0].str.contains('Q1 cutoff',case=False,na=False)]
    df.to_csv(current_dir + '/Value_Research/Ret. Compr.(Equity) - Reg.csv', index=False)

    df = pd.read_csv(current_dir+'/Value_Research/Ret. Compr.(Equity) - Dir.csv')
    df = df[~df.iloc[:,0].str.contains('Q1 cutoff',case=False,na=False)]
    df.to_csv(current_dir + '/Value_Research/Ret. Compr.(Equity) - Dir.csv', index=False)

    df = pd.read_csv(current_dir+'/Value_Research/Returns of ETFs and Index.csv')
    df = df[~df.iloc[:,0].str.contains('Q1 cutoff',case=False,na=False)]
    df = df[~df.iloc[:,0].str.contains('HDFC NIFTY 100 Equal Weight Index Fund - Regular Plan',case=False,na=False)]
    df.to_csv(current_dir + '/Value_Research/Returns of ETFs and Index.csv', index=False)

    
    for name in os.listdir(current_dir+'/Value_Research'):
        if (name=='Ret. Compr.(Equity) - Reg.csv' or name=='Ret. Compr.(Debt) - Dir.csv' or name=='Ret. Compr.(Equity) - Dir.csv' or name=='Ret. Compr.(Debt) - Reg.csv' or name=='Returns of ETFs and Index.csv'):
            df = pd.read_csv(current_dir+'/Value_Research//'+name)
            # df = df[~df.iloc[:,0].str.contains('cuttoff',case=False,na=False)]
            
            first_column = df.iloc[:, 0].notna()
            other_column = df.iloc[:, 1:].isna().all(axis=1)
            combined = first_column & other_column
            df[combined]
            indx = list(df.index[combined])
            if name=='Ret. Compr.(Debt) - Dir.csv':
                print(indx)

            for i in range(len(indx)):
                if i == len(indx) - 1:
                    temp = df.iloc[indx[i]:]
                else:
                    temp = df.iloc[indx[i]:indx[i+1]]
                
                benchmark_data = temp.loc[temp['Unnamed: 1'].isnull()]
                benchmark_data = benchmark_data.dropna(subset = [first_col])
                peerset = temp.loc[temp['Unnamed: 1'].isnull()!=True]
                category = temp.iloc[0][first_col]
                category = category.replace('/','_')
                category = category.replace(':','_')
                
                if name=='Returns of ETFs and Index.csv':
                    if category=='Value Research' or category=='Equity Index Funds' or category=='ETF Funds' or category=='Passive Funds' or category=='Index Funds' or ('Return' in category):
                        continue
                    if 'ETF' in category:
                        benchmark_data.to_csv(current_dir+'/default/ETF_benchmark_values/'+category+'.csv',index=False)
                        peerset.to_csv(current_dir+'/default/Schemes/ETF/'+category+'.csv',index=False)
                    else:
                        benchmark_data.to_csv(current_dir+'/default/Index_benchmark_values/'+category+'.csv',index=False)
                        peerset.to_csv(current_dir+'/default/Schemes/Index/'+category+'.csv',index=False)
                else:
                    if category=='Value Research' or category=='Equity Investment Solutions' or category=='FoFs' or ('Return' in category):
                        continue
                    if name=='Ret. Compr.(Equity) - Reg.csv':
                        benchmark_data.to_csv(current_dir+'/default/Equity_benchmark_values/'+category+'.csv',index=False)
                        peerset.to_csv(current_dir+'/default/Equity_peer_set/'+category+'.csv',index=False)
                    elif name=='Ret. Compr.(Debt) - Dir.csv':
                        benchmark_data.to_csv(current_dir+'/default/Debt_benchmark_values/'+category+'.csv',index=False)
                        peerset.to_csv(current_dir+'/default/Debt_peer_set//'+category+'.csv', index=False)
                    elif name=='Ret. Compr.(Equity) - Dir.csv':
                        benchmark_data.to_csv(current_dir+'/undefault/Equity_benchmark_values/'+category+'.csv',index=False)
                        peerset.to_csv(current_dir+'/undefault/Equity_peer_set/'+category+'.csv',index=False)
                    else:
                        benchmark_data.to_csv(current_dir+'/undefault/Debt_benchmark_values/'+category+'.csv',index=False)
                        peerset.to_csv(current_dir+'/undefault/Debt_peer_set//'+category+'.csv', index=False)
    
    print("VR files Created")
