from application.model.model import db, Category, FundManagerCategoryConfig
import csv



def FM_names(current_dir):
    with open(current_dir + '/FundManagers.csv', mode ='r')as file:
        csvFile = csv.reader(file)
        for line in csvFile:
            category = Category.query.filter_by(name=line[0]).first()
            if category is None:
                print("category not found", line[0])
                continue
            else:
                print("category found", line[0])
                check_existing = FundManagerCategoryConfig.query.filter_by(category_id = category.id).first()
                if check_existing is None:
                    new_fund_config = FundManagerCategoryConfig(fund_manager = line[1] , category_id = category.id, deupty_fund_managers = line[2])
                    try:
                        db.session.add(new_fund_config)
                        db.session.commit()
                    except Exception as e:
                        db.session.rollback()
                        print("unable to add the category: " + line[0])
                else:
                    print("already exist", line)
    pass