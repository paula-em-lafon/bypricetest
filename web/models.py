from shared import db


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    upc = db.Column(db.String(12))
    item_name = db.Column(db.String())
    price = db.Column(db.Float(precision=2))
    image = db.Column(db.String())

    def __init__(self, upc, item_name, price, image):
        self.upc = upc
        self.item_name = item_name
        self.price = price
        self.image = image

    def __repr__(self):
        return '<item name %r>' % self.item_name
