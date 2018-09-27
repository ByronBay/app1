# app.py
# References:
# https://stackoverflow.com/questions/5769382/can-i-put-a-breakpoint-in-a-running-python-program-that-drops-to-the-interactive
# https://scotch.io/bar-talk/processing-incoming-request-data-in-flask
# https://groups.google.com/forum/#!topic/mitappinventortest/JmmIYXAs_uM
# http://puravidaapps.com/postfile.php
# https://stackoverflow.com/questions/47679398/file-upload-error-in-flask


# import main Flask class and request object
from flask import Flask, request, jsonify

import pathlib
import os
import caas
import json

app = Flask(__name__)  # create the Flask app


def monitor_results(func):
    def wrapper(*func_args, **func_kwargs):
        print('function call ' + func.__name__ + '()')
        retval = func(*func_args, **func_kwargs)
        print('function ' + func.__name__ + '() returns ' + repr(retval))
        return retval
    wrapper.__name__ = func.__name__
    return wrapper


# @app.route('/query-example')
@app.route('/qe')
def query_example():
    return 'Todo...'

# allow both GET and POST requests
# @app.route('/form-example', methods=['GET', 'POST'])


@app.route('/fe', methods=['GET', 'POST'])
@monitor_results
def form_example():
    print("fe called")
    print(request)
    if request.method == 'POST':  # this block is only entered when the form is submitted
        print("1---")

        imageData = request.get_data()

        deviceInformation = {
            "fileName": request.args.get("fileName"),
            "deviceID": request.args.get("deviceID"),
            "simSerialNumber": request.args.get("simSerialNumber"),
            "phoneNumber": request.args.get("phoneNumber"),
            "networkOperatorName": request.args.get("networkOperatorName"),
            "browserNavAttributes": request.args.get("browserNavAttributes"),
            "locationSensor" : request.args.get("locationSensor"),
            "timeNow" : request.args.get("timeNow"),
            "timeSystem" : request.args.get("timeSystem")
        }

        print(deviceInformation["locationSensor"])
        
        print("13--")

        print(deviceInformation)

        print("15--")

        timestamp = caas.lib.get_timestamp()
        uuid = caas.lib.get_uuid()

        directoryServer = timestamp + "_" + str(uuid)
        fileNameServer = timestamp + "_" + str(uuid) + ".jpg"

        pfnImageServer = os.path.join(directoryServer, fileNameServer)
        pathlib.Path(directoryServer).mkdir(parents=True, exist_ok=True)

        newFile = open(pfnImageServer, 'wb')
        newFile.write(imageData)
        newFile.close()

        print("2---")
        print(pfnImageServer)
        print("3---")

        #resultData = {}
        resultData = caas.proc.process_main(directoryServer, pfnImageServer)

        print("34--")

        print(resultData)

        print("35--")

        best_color = resultData["results"]["color"]["results"]["best"]

        data = {
            'meta': {
                'uuid': uuid,
                'timestamp': timestamp,
                'filenameServer': pfnImageServer
            },
            'device': deviceInformation,
            'result': resultData,
            'result_simple' : [ "Your color is called \n{}\n and comes from the color-scheme\n{}.".format(best_color["name"],best_color["scheme"]), best_color["rgb"][0], best_color["rgb"][1], best_color["rgb"][2]]
        }

        returnData = jsonify(data)

        print("4---")
        print(data)
        print("5---")


        return returnData

    return '''request was not post'''


if __name__ == '__main__':
    print("running from main")
    # run app in debug mode on port 5000
    app.run(debug=True, port=5000, host='0.0.0.0')
