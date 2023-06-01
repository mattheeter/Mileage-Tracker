from flask import Flask # Importing the Flask class to create a Flask object
from flask import render_template # render_template used to return html from the routes
from flask import request # For getting user data

app = Flask(__name__) # Creating new Flask object, with the special vairable __name__ used to automatically choose the module name

@app.route('/', methods=['POST', 'GET']) # Decorator for "registering" the route, methods added for inuptting user data
def home():
    if request.method == 'POST': # If a post request occurs, this if runs
        print(request.form['vehicle']) # Printing the values put into the forms
        print(request.form['mileage']) # Words in brackets were used in html name attributes
    return render_template('home.html')
