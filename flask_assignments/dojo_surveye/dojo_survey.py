from flask import Flask, render_template, request, redirect, url_for, session, flash
app = Flask(__name__)
app.secret_key = "Id0n0tLVpi"
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/results', methods=['POST']) #this route will handle our form submission; defined which HTTP methods are allowed by this route
def get_results():
    # establish variables
    session['name'] = request.form['name']
    session['location'] = request.form['dojo_location']
    session['language'] = request.form['favorite_language']
    session['comment'] = request.form['comment']
    # validate the input
    if len(request.form['name']) < 1:  
        flash("You must enter a name.")
        return redirect('/')
    if len(request.form['comment']) < 1: 
        flash("You must enter a comment. Keep it short (no more than 120 characters).")
        return redirect('/')
    elif len(request.form['comment']) > 120: 
        flash("Thanks for the feedback, but please limit comments to 120 characters or less.")
        return redirect('/')
    else:
        # display the results
        return render_template('dojo_survey_results.html', name=session['name'], location=session['location'], language=session['language'], comment=session['comment'])
app.run(debug=True)