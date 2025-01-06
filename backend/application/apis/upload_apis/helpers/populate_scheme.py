import os
from application.model.model import db, Scheme, Category, Company
import pandas as pd
from sqlalchemy import func




def populate_scheme(current_dir,first_col="Daily Competition Returns Comparison Report as of 04-Jul-24"):
    Debt_direct = os.listdir(current_dir+"/default/Schemes/Debt")
    Equity_regular = os.listdir(current_dir+"/default/Schemes/Equity")
    Debt_regular = os.listdir(current_dir+"/undefault/Schemes/Debt")
    Equity_direct = os.listdir(current_dir+"/undefault/Schemes/Equity")
    Etf = os.listdir(current_dir+"/default/Schemes/ETF")
    Indx = os.listdir(current_dir+"/default/Schemes/Index")
    filetype = [Debt_direct,Equity_regular,Debt_regular,Equity_direct]
    df=pd.DataFrame(columns=['scheme_name','scheme_type','scheme_subtype','category','AMC'])
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
            sub_df=pd.DataFrame(columns=['scheme_name','scheme_type','scheme_subtype','category','AMC'])
            if file!='MasterSheet.csv':
                df_temp = pd.read_csv(file_path+file)
                df_temp.columns = df_temp.iloc[1].values
                if 'Source :- ICRA Analytics Limited' in list(df_temp.iloc[df_temp.shape[0]-3]):
                    df_temp.columns = df_temp.iloc[4].values
                    df_temp = df_temp.iloc[5:df_temp.shape[0]-11]
                if 'Corpus (In crs.)' not in df_temp.columns:
                    continue
                else:
                    df_temp = df_temp.iloc[2:df_temp.shape[0]-5]
                temp_category=file.split(".")[0]

              
                try:
                    temp_category=temp_category.split('- ')[1]
                except Exception as e:
                    pass
                temp_category=temp_category.strip()
                
                new_scheme_name = []
                for row in df_temp.iterrows():
                    
                    is_scheme_in_database = Scheme.query.filter_by(name = row[1]['Scheme Name']).first()
                    if is_scheme_in_database is None:
                        new_scheme_name.append(row[1]['Scheme Name'])
                        
                        
                sub_df['scheme_name'] = new_scheme_name

                sub_df['category'] = [temp_category]*(sub_df.shape[0])
                if files==Debt_direct:
                    sub_df['scheme_type']=['Debt']*(sub_df.shape[0])
                    sub_df['scheme_subtype']=['Direct']*(sub_df.shape[0])
                elif files==Equity_regular:
                    sub_df['scheme_type']=['Equity']*(sub_df.shape[0])
                    sub_df['scheme_subtype']=['Regular']*(sub_df.shape[0])
                elif files==Debt_regular:
                    sub_df['scheme_type']=['Debt']*(sub_df.shape[0])
                    sub_df['scheme_subtype']=['Regular']*(sub_df.shape[0])   
                else:
                    sub_df['scheme_type']=['Equity']*(sub_df.shape[0])
                    sub_df['scheme_subtype']=['Direct']*(sub_df.shape[0])
              
                df = pd.concat([df,sub_df],axis=0)
                df = df[df['scheme_name']!='IDBI Equity Advantage Fund - Reg - Growth']
    
    all_scheme_etf_index = pd.DataFrame(columns=['scheme_name','scheme_type','scheme_subtype','category','AMC'])
    for files in [Etf,Indx] :
        for filename in files:
            etf_indx_temp = pd.DataFrame(columns=['scheme_name','scheme_type','scheme_subtype','category','AMC'])
            if files==Etf:
                etf_indx_df = pd.read_csv(current_dir+'/default/Schemes/ETF/'+filename)
            else:
                etf_indx_df = pd.read_csv(current_dir+'/default/Schemes/Index/'+filename)
            
            new_etf_scheme_name = []
            for row in etf_indx_df.iterrows():
                is_scheme_in_database = Scheme.query.filter_by(name = row[1][first_col]).first()
                if is_scheme_in_database is None:
                    new_etf_scheme_name.append(row[1][first_col])
                        
                        
            
            etf_indx_temp['scheme_name'] = new_etf_scheme_name
            
            c,ty,sub = [],[],[]
            for i in range(etf_indx_temp.shape[0]):
                c.append(filename.split('.')[0])
                sub.append('Regular')
                if files==Etf :
                    ty.append('ETF')
                else:
                    ty.append('Index')
            etf_indx_temp['category'] = c
            etf_indx_temp['scheme_type'] = ty
            etf_indx_temp['scheme_subtype'] = sub
            etf_indx_temp = etf_indx_temp[1:]
            all_scheme_etf_index = pd.concat([all_scheme_etf_index,etf_indx_temp],axis=0)
    df = pd.concat([df,all_scheme_etf_index], axis=0)
    All_Scheme = df
    
    all_scheme_names = All_Scheme['scheme_name']
    all_scheme_amc=[]
    for i in all_scheme_names:
        first_word=i.split(' ')[0]
        if(first_word=='Aditya'):
            all_scheme_amc.append('ABSL')
        elif(first_word=='Bank'):
            all_scheme_amc.append('BOI')
        elif(first_word=='360'):
            all_scheme_amc.append('360 One')
        elif(first_word=='Parag'):
            all_scheme_amc.append("PPFAS")
        elif((first_word=='Tata')or(first_word=='TATA')):
            all_scheme_amc.append("Tata")
        elif(first_word=='Old'):
            all_scheme_amc.append("Old Bridge")
        elif(first_word=='Templeton'):
            all_scheme_amc.append("Franklin")
        else:
            all_scheme_amc.append(first_word)
    All_Scheme['AMC']=all_scheme_amc
  

    new_category=[]
    for i in range(All_Scheme.shape[0]):
        flag=0
        if(All_Scheme.iloc[i]['category']=='Banking and PSU'):
            new_category.append("Banking & PSU")
        elif(All_Scheme.iloc[i]['category']=='Children Plan'):
            new_category.append("Children Equity")
        elif(All_Scheme.iloc[i]['category']=='Credit Risk Fund'):
            new_category.append("Credit Risk Funds")
        elif(All_Scheme.iloc[i]['category']=='Dynamic Bond Fund'):
            new_category.append("Dynamic Funds")
        elif(All_Scheme.iloc[i]['category']=='Corporate Bond Fund'):
            new_category.append("Corporate Bond Funds")
        elif(All_Scheme.iloc[i]['category']=='Corporate Bond'):
            new_category.append("Corporate Bond Funds")
        elif(All_Scheme.iloc[i]['category']=='Floater Fund'):
            new_category.append("Floater")
        elif(All_Scheme.iloc[i]['category']=='Money Market Fund'):
            new_category.append("Money Manager")
        elif(All_Scheme.iloc[i]['category']=='Regular Savings'):
            new_category.append("Conservative Hybrid")
        elif(All_Scheme.iloc[i]['category']=='Short Duration Fund'):
            new_category.append("Short Duration")
        elif(All_Scheme.iloc[i]['category']=='MNC Funds'):
            new_category.append("MNC Fund")
        elif(All_Scheme.iloc[i]['category']=='Transport and Logistics'):
            new_category.append("Transportation and Logistics")
        else:
            new_category.append(All_Scheme.iloc[i]['category'])
    All_Scheme['category']=new_category
    All_Scheme_1=pd.DataFrame()
    All_Scheme_1=All_Scheme.copy()

    
    for index, row in All_Scheme.iterrows():
        company_name = row['AMC']
        category_name = row['category']
        company = Company.query.filter(func.lower(Company.name) == company_name.lower()).first()
        category = Category.query.filter(func.lower(Category.name) == category_name.lower()).first()
        if company is None:
            
            message = f"Company not found {company_name}, while adding scheme {row['scheme_name']}"
            print(message)
            
            return "new_company_found" ,message
        if category is None:
            message = f"Category not found {category_name}, while adding scheme {row['scheme_name']}"
            print(message)
            return "new_category_found" , message 

            
        if category and company:
            existing_duplicate_category_company = Scheme.query.filter_by(category_id = category.id).filter_by(company_id = company.id).filter_by(type = row['scheme_type']).filter_by(subtype = row['scheme_subtype']).first()
            if existing_duplicate_category_company is None:
                print(f"adding new scheme: {row['scheme_name']}")
                new_scheme = Scheme(
                    name=row['scheme_name'],
                    type=row['scheme_type'],
                    description = "No description available!",
                    subtype=row['scheme_subtype'],
                    category_id=category.id,
                    company_id=company.id
                )
                try:
                    db.session.add(new_scheme)
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    print(f"unable to add the scheme: {row['scheme_name']}")
                    print(e)
                    continue
            else:
                print("company_name",company_name)
                print("scheme_name", row["scheme_name"]) 
                print("changed scheme name from: " + existing_duplicate_category_company.name + " to: "  + row["scheme_name"] )
                
                existing_duplicate_category_company.name = row['scheme_name']
                
                try:
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    print("unable to change the name of the scheme form: " + existing_duplicate_category_company.name + " to: " + row['scheme_name'])
                    continue
            
    return "successful", "none"