# coding:utf-8

from flask import Blueprint

app_orders = Blueprint("app_orders", __name__)


@app_orders()
def app_orders():
    return "app orders page"