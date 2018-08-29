# app.py
# References:
## https://stackoverflow.com/questions/5769382/can-i-put-a-breakpoint-in-a-running-python-program-that-drops-to-the-interactive
## https://scotch.io/bar-talk/processing-incoming-request-data-in-flask
## https://groups.google.com/forum/#!topic/mitappinventortest/JmmIYXAs_uM
## http://puravidaapps.com/postfile.php
## https://stackoverflow.com/questions/47679398/file-upload-error-in-flask


from flask import Flask, request, jsonify  # import main Flask class and request object
import datetime

import csv

app = Flask(__name__)  # create the Flask app

def monitor_results(func):
    def wrapper(*func_args, **func_kwargs):
        print('function call ' + func.__name__ + '()')
        retval = func(*func_args,**func_kwargs)
        print('function ' + func.__name__ + '() returns ' + repr(retval))
        return retval
    wrapper.__name__ = func.__name__
    return wrapper


#@app.route('/query-example')
@app.route('/qe')
def query_example():
    return 'Todo...'

# allow both GET and POST requests
#@app.route('/form-example', methods=['GET', 'POST'])
@app.route('/fe', methods=['GET', 'POST'])
@monitor_results
def form_example():
    print("fe called")
    print(request)
    if request.method == 'POST':  # this block is only entered when the form is submitted
        print("1---")
        image =  request.get_data()
        newFile=open('test.jpg','wb')
        newFile.write(image)
        print("2---")
        fileName = request.args.get("fileName")
        print(fileName)
        print("3---")

        return '''<h1>The image is is: {}</h1>
                  <h1>The color is: {}</h1>'''.format(fileName, "dummy")

    return '''<form method="POST">
                  Language: <input type="text" name="language"><br>
                  Framework: <input type="text" name="framework"><br>
                  <input type="submit" value="Submit"><br>
              </form>'''


# allow both GET and POST requests
#@app.route('/form-example', methods=['GET', 'POST'])
@app.route('/fe_dev', methods=['GET', 'POST'])
@monitor_results
def form_example_dev():
    print("fe _dev called")
    print(request)
    if request.method == 'POST':  # this block is only entered when the form is submitted
        print("1---")
        print(request.get_data())
        print("2---")
        f = request.form
        print(f)
        fileName = request.form.get('fileName')
        print(fileName)
        print("3---")
        a = request.args
        print(a)
        print("4---")

        file = open('outfile.txt', 'w') 
        writer = csv.writer(file, delimiter = '\t')

        for key in f.keys():
            print(key)
            for value in f.getlist(key):
                print(key,":",value)
                writer.writerow([key] +[":"]+ [value])
                writer.writerow(["new"] +[":"]+ ["line"])
                

        framework = request.form.get('framework')
        language = request.form.get('language')

        return '''<h1>The language value is: {}</h1>
                  <h1>The framework value is: {}</h1>'''.format(language, framework)

    return '''<form method="POST">
                  Language: <input type="text" name="language"><br>
                  Framework: <input type="text" name="framework"><br>
                  <input type="submit" value="Submit"><br>
              </form>'''


@app.route('/json-example')
def json_example():
    return 'Todo...'


if __name__ == '__main__':
    print("running from main")
    app.run(debug=True, port=5000, host= '0.0.0.0')  # run app in debug mode on port 5000
