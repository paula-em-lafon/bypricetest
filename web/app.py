from flask import Flask
import os
from shared import db

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

from models import Product


@app.route('/items', methods=['GET'])
def get_items():
    if request.args == []:


@app.route('/<int:upc>', methods=['GET'])
def get_product(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

if __name__ == '__main__':
    app.run()
