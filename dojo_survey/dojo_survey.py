from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/results', methods=['POST']) #this route will handle our form submission; defined which HTTP methods are allowed by this route
def get_results():
    name = request.form['name']
    location = request.form['dojo_location']
    language = request.form['favorite_language']
    comment = request.form['comment']
    return render_template('dojo_survey_results.html', name=name, location=location, language=language, comment=comment)
app.run(debug=True)