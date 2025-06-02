from flask import Flask
from routes.user_routes import app_views

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix="/api/v1")

if __name__ == '__main__':
    app.run(debug=True, port=5001)
