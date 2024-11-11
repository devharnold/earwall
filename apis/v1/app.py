# setting up the flask app

from flask import Flask
from apis.v1.views import graphql_bp

app = Flask(__name__)

#register the graphql blueprint
app.register_blueprint(graphql_bp, url_prefix='/api/v1')


if __name__ == "__main__":
    app.run(debug=True, port=5000)