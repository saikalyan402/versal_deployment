from application.model.model import db, Company
import pandas as pd
from pandas import read_excel





def populate_company(current_dir):
    existing_companies = Company.query.all()

    existing_companies_name_list = [company.name for company in existing_companies]
    
    
    company_data = pd.read_excel(current_dir+'/All Schemes List_data as on 28th june 2024.xlsx')
    try:
        company_names = list(company_data['Suggested Name'].dropna())
        for company_name in company_names:
            if company_name not in existing_companies_name_list:
                company = Company(name=company_name)
                try:
                    db.session.add(company)
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    print("unable to add the company: " + company_name)
        
        print("Companies table updated")
        
        pass
    except:
        print("No 'Suggested Name' column exist")
    
    
    