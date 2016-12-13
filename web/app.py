from flask import Flask, request, abort
# from flask_restful import Resource, Api
import os
import re
import json

from shared import db
from mixins. serializer import JsonSerializer


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

from models import Product


@app.route('/items', methods=['GET'])
def get_items():
    products = None
    all_args = request.args.to_dict()

    # check if upc provided
    if 'upc' in all_args:
        if re.match('^[0-9]{12}$', all_args['upc']):
            products = Product.query.filter(Product.upc == all_args['upc'])
        else:
            abort(400)
            # check if min price of max price
    elif 'max_price' or 'min_price' in all_args:
        max_price_q = 9999999.99
        min_price_q = 0.0
        if 'max_price' in all_args:
            if match_price(all_args['max_price']):
                max_price_q = float(all_args['max_price'])
            else:
                abort(400)
        if 'min_price' in all_args:
            if match_price(all_args['min_price']):
                min_price_q = float(all_args['min_price'])
            else:
                abort(400)
        if min_price_q > max_price_q:
            abort(400)
        products = Product.query.filter(
            Product.price >= min_price_q).filter(Product.price <= max_price_q)
    # Check if no arguments are present
    elif all_args == {}:
        products = Product.query.all()
    # in all other cases return bad request

    if products is not None:
        products_json = []
        for product in products:
            products_json.append(ProductJsonSerializer().serialize(product))
        return json.dumps(products_json)
    else:
        abort(400)


def match_price(price):
    return re.match('^\d+(\.\d{1,2})?', price)


class ProductJsonSerializer(JsonSerializer):
    __attributes__ = ['id', 'upc', 'item_name', 'price', 'image']
    __required__ = ['id', 'upc', 'item_name', 'price', 'image']
    __object_class__ = Product


if __name__ == '__main__':
    app.run()
