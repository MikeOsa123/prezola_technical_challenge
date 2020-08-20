from app import db

from app.models import Product

import json

# read products json file
with open('products.json') as f:
    file_data = json.load(f)

# loop though each product in json file and add to Product database and commit changes
for obj in file_data:
    new_row = Product(brand=obj["brand"], name=obj["name"], price=obj["price"], quantity=obj["in_stock_quantity"])
    db.session.add(new_row)
    db.session.commit()
