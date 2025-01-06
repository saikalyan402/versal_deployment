from application.model.model import db, Category, BenchmarkConfig
import csv

def populate_benchmark_config(current_dir):
    with open(current_dir + '/benchmark_master.csv', mode ='r')as file:
        csvFile = csv.reader(file)
        for line in csvFile:
            category = Category.query.filter_by(name=line[2]).first()
            if category:
                check_existing_config = BenchmarkConfig.query.filter_by(benchmark_name = line[0]).filter_by(category_id = category.id).first()
                if check_existing_config is None:
                    new_category = BenchmarkConfig(benchmark_name=line[0], category_id=category.id)
                    
                    try:
                        db.session.add(new_category)
                        db.session.commit()
                    except Exception as e:
                        db.session.rollback()
                        print(e)
                        print("unable to add the  Benchmark category: " + str(line))
            else:
                print("Category not found: " + line[2])
    pass