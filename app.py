import os
from requests import request
import json
from jsonschema import validate, ValidationError
from flask import Flask,request,make_response,jsonify
import execute_db

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config['Json_SORT_KEYS'] = False
ip_address = os.getenv("IP")
host = f'{ ip_address }/v1'
error_message = { "message":"ERROR" }
# 在庫の更新、作成 ＆ 在庫チェック
@app.route("/stocks", methods=['POST'])
def update_stocks():
    if not request.headers.get("Content-Type") == "application/json":
        return make_response(jsonify(error_message))
    data = request.get_json()
    schema = {
        "type":"object",
        "properties":{
            "name":     {"type":"string"},
            "amount":   {"type":"integer","minimum":1}
        },
        "required":["name"],
        "additionalProperties":False
    }
    try:
        validate(data,schema)
    except ValidationError:
        print("error")
        return make_response(jsonify(error_message))

    name = data.get("name") 
    amount = data.get("amount") or 1
    
    execute_db.update(name,amount)

    return_message = request.get_json()
    resp = make_response(json.dumps(return_message,separators=(',',':')))
    resp.headers['Content-Type'] = "application/json"
    resp.headers['Location'] = host+"/stocks/"+name
    return resp

# 在庫チェック
# URLが/v1/stocks/xxxの場合
@app.route("/stocks/<name>",methods=["GET"])
def return_stock(name):
    data = execute_db.check(name)
    resp = make_response(json.dumps(data,separators=(',',':')))
    resp.headers['Content-Type'] = "application/json"
    return resp

# URLが/v1/stocksの場合
@app.route("/stocks", methods=["GET"])
def return_all():
    data = execute_db.check()
    resp = make_response(json.dumps(data,separators=(',',':'),sort_keys=True))
    resp.headers['Content-Type'] = "application/json"
    return resp

# 販売
@app.route("/sales",methods=["POST"])
def sales():
    if not request.headers.get("Content-Type") == "application/json":
        return make_response(jsonify(error_message))
    data = request.get_json()
    schema = {
        "type":"object",
        
        "properties":{
            "name":     {"type":"string"},
            "amount":   {"type":"integer","minimum":1},
            "price":    {"type":"number","minimum":0}
        },
        "required":["name"],
        "additionalProperties":False
    }
    try:
        validate(data,schema)
    except ValidationError:
        print("error")
        return make_response(jsonify(error_message))

    data = request.get_json()
    name = data.get("name")
    amount = data.get("amount") or 1
    price = data.get("price")

    resp = execute_db.sales(name,amount,price)
    if resp == None:
        resp = make_response(json.dumps(request.get_json(),separators=(',',':')))
        resp.headers['Content-Type'] = "application/json"
        resp.headers['Location'] = host+"/stocks/"+name
        return resp
    else:
        return make_response(jsonify(error_message))
# 売り上げチェック
@app.route("/sales",methods=["GET"])
def check_sales():
    data = execute_db.getsales()
    return make_response(jsonify(data))

# 全削除
@app.route("/stocks",methods=["DELETE"])
def delete():
    execute_db.all_delete()
    return make_response()

if __name__ == '__main__':
    app.run()
    