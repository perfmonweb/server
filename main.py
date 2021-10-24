import json
from flask import Flask, make_response
from flask.json import jsonify
from flask_cors import CORS
from adbm import ADB_Modules
from fps import FPS
from utils import Utils

app = Flask(__name__)
CORS(app)


@app.route("/")
def hello():
    return jsonify({'text': 'Hello World'})


@app.route('/fps/<package_name>', methods=['GET', 'POST'])
def getfps(package_name):
    fps = FPS(package_name=package_name, duration=60, dumpfile="text",
              print_latency=False, require_full_name=True)
    frames = fps._get_recent_frames()
    if not fps.error:
        if len(frames) < 3:
            return
        total = len(frames) - 1
        dt = (frames[-1].vsync - frames[0].vsync) / 1000000000
        avg = total / dt
        return jsonify(str(avg))
    else:
        return fps.error


@app.route('/checkadb', methods=['GET'])
def checkADB():
    mod = ADB_Modules()
    return mod.verifyAdb()


@app.route('/getdevices', methods=['GET'])
def getDevices():
    mod = ADB_Modules()
    return mod.showDevices()


@app.route('/getdeviceprop', methods=['GET'])
def getDeviceProp():
    mod = ADB_Modules()
    return mod.get_device_info()


@app.route("/setpackage")
def set_package_name():
    return "hello"


@app.route("/getpackage")
def get_package_name():
    return "hello"


@app.route("/packages/<package_name>", methods=['POST'])
def validate_package_name(package_name):
    utils = Utils()
    return utils._validate_package_name(package_name)


if __name__ == "__main__":
    app.run(port=5002)
