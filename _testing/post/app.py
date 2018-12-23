# import main Flask class and request object
from flask import Flask, request, jsonify

import pathlib
import os
import caas
import caas.lib
import caas.proc
import json

app = Flask(__name__)  # create the Flask app


@app.route('/api/v1/feedback', methods=['GET'])
def image_analysis_feedback():

    print("/api/v1/feedback called")

    feedbackInformation = {
        "workingPath": request.args.get("id"),
        "userliking": request.args.get("userliking"),
    }

    workingPath = feedbackInformation["workingPath"]

    print("feedbackInformation :")
    print(json.dumps(feedbackInformation))

    pfnOutFile = os.path.join(workingPath, "feedback.json")

    caas.lib.save_dict_as_json(feedbackInformation, pfnOutFile)

    message_text = "😊\nThat really makes us happy.\nThank you for your feedback!"

    if feedbackInformation["userliking"] == "bad":
        message_text = "😢\nWe are sorry we couldn't help this time.\nThank you for your feedback and keep the love!"

    data = {
        'message': [
            message_text
        ]
    }

    returnData = jsonify(data)

    return returnData


@app.route('/api/v1/image', methods=['POST'])
def image_analysis_request():

    print("/api/v1/image called")

    if request.method == 'POST':  # this block is only entered when the form is submitted

        # prepare working paths and directories
        print("1---")

        folder_manager = caas.lib.FolderManager()
        folder_manager.create_folder_structure()
        print(folder_manager)

        # write image data
        print("2--- data from image")

        print("get image-data start")
        imageData = request.get_data()
        print("get image-data end")

        print("write image-data start")
        with open(folder_manager.path_and_filename_to_incoming_image, 'wb') as f:
            f.write(imageData)
            
        print("write image-data end")

        # write request dat (urlencoded)
        print("3--- data from request")

        for key, value in request.args.to_dict().items():

            print(" -- key: {} \nvalue: {}".format(key, value))

            # write data to files

            pfnJson = pathlib.PurePath(
                folder_manager.path_to_incoming_image, "{}.json".format(key))

            caas.lib.save_json(value, pfnJson)

        # processing
        print("3---")

        resultData = caas.proc.process_main(folder_manager)

        # result preparation
        print("4---")

        best_color = resultData["results"]["color"]["results"]["best"]
        feedback_identifier = resultData["results"]["workingPath"]

        data = {
            'meta': {
                'uuid': folder_manager.uuid,
                'timestamp': folder_manager.timestamp,
                'storageImagePfn': folder_manager.path_and_filename_to_incoming_image,
                'storageImage': folder_manager.path_to_incoming_image,
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

        return returnData

    return jsonify({"message": "request not supported"}), 405


if __name__ == '__main__':
    print("running from main")
    # run app in debug mode on port 5000
    app.run(debug=True, port=5000, host='0.0.0.0')
