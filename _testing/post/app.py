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
import caas.lib
import caas.proc
import json

app = Flask(__name__)  # create the Flask app


def monitor_results(func):
    def wrapper(*func_args, **func_kwargs):
        print("===")
        print('function call ' + func.__name__ + '()')
        print("---")
        retval = func(*func_args, **func_kwargs)
        print("---")
        print('function ' + func.__name__ + '() returns ' + repr(retval))
        print("===")
        return retval
    wrapper.__name__ = func.__name__
    return wrapper


@app.route('/api/v1/feedback', methods=['GET'])
def image_analysis_feedback():

    print("/api/v1/feedback called")
    # print(request)

    feedbackInformation = {
        "id": request.args.get("id"),
        "userliking": request.args.get("userliking"),
    }

    for key, value in request.args.to_dict().items():
        print("** key: {} \nvalue: {}".format(key, value))

    message_text = "😊\nThat really makes us happy.\nThank you for your feedback!"

    if feedbackInformation["userliking"] == "bad":
        message_text = "😢\nWe are sorry we couldn't help this time.\nThank you for your feedback!"

    data = {
        'message': [
            message_text
        ]
    }

    returnData = jsonify(data)

    print("message : {}".format(data['message']))

    return returnData

# allow both GET and POST requests
# @app.route('/form-example', methods=['GET', 'POST'])


@app.route('/api/v1/image', methods=['POST'])
@monitor_results
def image_analysis_request():
    print("/api/v1/image called")
    print(request)
    if request.method == 'POST':  # this block is only entered when the form is submitted
        print("1---")

        imageData = request.get_data()

        for key, value in request.args.to_dict().items():
            print("** key: {} \nvalue: {}".format(key, value))


        print("15--")

        # prepare file locations

        timestamp = caas.lib.get_timestamp()
        uuid = caas.lib.get_uuid()

        location_prefix_of_data_directories = "data"

        directory_name_of_current_image = timestamp + "_" + str(uuid)
        filename_of_current_image = timestamp + "_" + str(uuid) + ".jpg"

        path_and_filename_to_current_image = os.path.join(
            location_prefix_of_data_directories, directory_name_of_current_image, filename_of_current_image)
        path_to_current_image = os.path.join(
            location_prefix_of_data_directories, directory_name_of_current_image)
        pathlib.Path(path_to_current_image).mkdir(parents=True, exist_ok=True)

        # write information

        newFile = open(path_and_filename_to_current_image, 'wb')
        newFile.write(imageData)
        newFile.close()

        with open(os.path.join(path_to_current_image, 'deviceInformation.json'), 'w') as fp:
            json.dump(request.args.to_dict(), fp)

        print("2---")
        print("path_and_filename_to_current_image : {}".format(
            path_and_filename_to_current_image))
        print("path_to_current_image              : {}".format(
            path_to_current_image))
        print("3---")

        # resultData = {}
        resultData = caas.proc.process_main(
            path_to_current_image, path_and_filename_to_current_image)

        print("34--")

        print(resultData)

        print("35--")

        best_color = resultData["results"]["color"]["results"]["best"]
        feedback_identifier = resultData["results"]["workingPath"]

        data = {
            'meta': {
                'uuid': uuid,
                'timestamp': timestamp,
                'filenameServer': path_and_filename_to_current_image
            },
            'device': 'x',
            'result': resultData,
            'result_simple': [
                "Your color is called \n{}\n and comes from the color-scheme\n{}.".format(
                    best_color["name"], best_color["scheme"]),
                best_color["rgb"][0],
                best_color["rgb"][1],
                best_color["rgb"][2],
                feedback_identifier
            ]
        }

        returnData = jsonify(data)

        with open(os.path.join(resultData["results"]["workingPath"], 'returnData.json'), 'w') as fp:
            json.dump(repr(data), fp)

        print("3.5--")
        print("result simple : {}".format(data['result_simple']))
        print("4---")
        print(data)
        print("5---")

        return returnData

    return jsonify({"message": "request not supported"}), 405


if __name__ == '__main__':
    print("running from main")
    # run app in debug mode on port 5000
    app.run(debug=True, port=5000, host='0.0.0.0')
