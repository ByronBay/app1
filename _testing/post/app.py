# app.py
# References:
## https://stackoverflow.com/questions/5769382/can-i-put-a-breakpoint-in-a-running-python-program-that-drops-to-the-interactive
## https://scotch.io/bar-talk/processing-incoming-request-data-in-flask
## https://groups.google.com/forum/#!topic/mitappinventortest/JmmIYXAs_uM
## http://puravidaapps.com/postfile.php
## https://stackoverflow.com/questions/47679398/file-upload-error-in-flask


from flask import Flask, request  # import main Flask class and request object

app = Flask(__name__)  # create the Flask app


#@app.route('/query-example')
@app.route('/qe')
def query_example():
    return 'Todo...'


# allow both GET and POST requests
#@app.route('/form-example', methods=['GET', 'POST'])
@app.route('/fe', methods=['GET', 'POST'])
def form_example():
    if request.method == 'POST':  # this block is only entered when the form is submitted
        language = request.form.get('language')
        framework = request.form['framework']

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
    app.run(debug=True, port=5000)  # run app in debug mode on port 5000
