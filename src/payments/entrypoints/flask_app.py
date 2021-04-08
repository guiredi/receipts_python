from flask import request, Blueprint

from payments import app
from payments.domain import commands
from payments.service_layer import messagebus

bp_payment = Blueprint('admin', __name__, url_prefix='/payment')

@app.route("/credit", methods=["POST"])
def add_batch():
    cmd = commands.PayByCreditCard(
        request.json["ref"], request.json["sku"], request.json["qty"], eta
    )
    messagebus.handle(cmd)
    return "OK", 201
