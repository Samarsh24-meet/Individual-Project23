from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config = {
  "apiKey": "AIzaSyBJR-fdKzyBdnzshKxe5kbl5aH2vEw2wVQ",
  "authDomain": "cookbook-50c2e.firebaseapp.com",
  "projectId": "cookbook-50c2e",
  "storageBucket": "cookbook-50c2e.appspot.com",
  "messagingSenderId": "249930564425",
  "appId": "1:249930564425:web:3ae3b4141d39456adf9098",
  "measurementId": "G-ZQ1NDYVBEB" ,
  "databaseURL" : "https://cookbook-50c2e-default-rtdb.europe-west1.firebasedatabase.app/"
};

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

#Code goes below here

@app.route('/', methods=['GET','POST'])
def signin():
    try:
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            login_session['user'] = auth.sign_in_with_email_and_password(email,password)
            return redirect(url_for('home_page'))
    except:
        return render_template('signin.html')
    return render_template('signin.html')

@app.route('/signup', methods=['GET','POST'])
def signup():
    try:
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            username = request.form['username']
            bio = request.form['bio']
            login_session['user'] = auth.create_user_with_email_and_password(email,password)
            return redirect(url_for('home'))
    except:
        return render_template('signup.html')
    return render_template('signup.html')


@app.route('/home_page', methods=['GET', 'POST'])
def home():
    try:
        if request.method == "POST":
            title = request.form['title']
            optional = request.form['optional']
            if request.method == "POST":
                ingredients = request.form['ingredients']
            if request.method == 'POST':
                steps = request.method['steps']
            return redirect(url_for('home'))
    except:
        return render_template("home.html")

    return render_template('home.html', st = steps , ing = ingredients)






#Code goes above here

if __name__ == '__main__':
    app.run(debug=True)