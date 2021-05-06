from flask import Flask
from flask_cors import CORS
from basic.controllers import front_controller as FC
from basic.data_initialization import initialize_data


app = Flask(__name__)

app.config['SECRET_KEY'] = 'secrecy'

CORS(app)

FC.route(app)

if __name__ == '__main__':

    initialize_data()

    app.run(debug=True)
