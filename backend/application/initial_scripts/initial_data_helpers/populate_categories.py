from application.model.model import db, Category
import csv


def intially_populate_categories(current_dir):
    with open(current_dir + '/categories.csv', mode ='r')as file:
        csvFile = csv.reader(file)
        for line in csvFile:
            new_category = Category(name=line[0])
            try:
                db.session.add(new_category)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print("unable to add the category: " + line[0])
    pass