from backend.models.user import User
from dotenv import load_dotenv
from apis.v1.views import app_views
from engine.db_storage import get_db_connection
from flask import jsonify, request, abort, make_request

load_dotenv()

