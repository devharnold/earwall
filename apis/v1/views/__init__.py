"""Blueprint instance for API v1 views"""

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/apis/v1')

from apis.v1.views.users import *
from apis.v1.views.cashwallet import *
from apis.v1.views.transactions import *
from apis.v1.views.batch_transactions import *