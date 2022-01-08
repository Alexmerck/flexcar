import csv

from webapp import db
from webapp.models import Car_base

def save_cars_data_to_db_from_csv(filename):
    with open(filename, 'r', encoding="utf-8") as f:
        fields = ['manufacturer', 'model']
        reader = csv.DictReader(f, fields,delimiter=';')

        for row in reader:
            save_car_data(row)

def save_car_data(row):
    car = Car_base(manufacturer = row["manufacturer"], model = row["model"])
    db.session.add(car)
    db.session.commit()

if __name__ == "__main__":
    save_cars_data_to_db_from_csv("carbase.csv")
