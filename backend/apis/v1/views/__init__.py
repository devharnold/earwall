"""Blueprint instance for API v1 views"""

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/apis/v1')

from apis.v1.views.userViews import *
from apis.v1.views.cashwalletViews import *
from apis.v1.views.transactionViews import *
from apis.v1.views.batchTransactionViews import *