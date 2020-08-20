from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(64), index=True)
    surname = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User: {}>'.format(self.firstname)

# class List(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     status = db.Column(db.String(32))

#     def __repr__(self):
#         return '<List number: {}>'.format(self.id)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(64), index=True)
    name = db.Column(db.String(64), index=True)
    price = db.Column(db.String(32))
    quantity = db.Column(db.Integer)

    def __repr__(self):
        return '<Product: {}>'.format(self.name)
