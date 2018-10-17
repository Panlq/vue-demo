"""
    python flask mini-server for vue-test

"""
import time
import pymongo
from flask import Flask
from flask import request
from flask import jsonify, make_response
DB_NAME = "vueTest"
COLLECTION = "data"

client = pymongo.MongoClient()
mongoMgr = client[DB_NAME][COLLECTION]

app = Flask(__name__)


def buildResponse(status, data, info=None):
    res = {
        "status": status,
        "data": data,
        "errorInfo": info
    }
    resp = make_response(jsonify(res))
    resp.headers["Access-Control-Allow-Origin"] = "*"
    return resp


@app.route('/')
def index():
    return "index"


@app.route("/get")
def getData():

    res = mongoMgr.find(projection={"_id": False})
    res = list(res)
    print(res)
    return buildResponse(0, res)


@app.route("/post", methods=["POST"])
def postData():
    data = request.form.to_dict()
    res = mongoMgr.count(filter={"username": data["username"]})
    if res > 0:
        return buildResponse(1, "", "username existed.")
    temp = {
      "rateTime": time.time(),
      "rateType": 0,
      "avatar": "http://static.galileo.xiaojukeji.com/static/tms/default_header.png",
      "recommend": [""]
    }
    data.update(temp)
    res = mongoMgr.insert_one(data)
    return buildResponse(0, "", "ok")


@app.route("/del", methods=["POST"])
def delData():
    data = request.form.to_dict()
    res = mongoMgr.delete_one({"username": data["username"]})
    return buildResponse(0, "", "ok")

if __name__ == '__main__':
    import os
    print(os.getcwd())
    app.run(debug=True, port=8000)