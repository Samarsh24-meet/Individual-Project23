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
            return redirect(url_for('home'))
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
            UID = login_session['user']['localId']
            info = {'username':username }
            db.child('Users').child(UID).set(info)
            login_session['user'] = auth.create_user_with_email_and_password(email,password)
            return redirect(url_for('home'))
    except Exception as e:
        print(e)
        return render_template('signup.html')
    return render_template('signup.html')


@app.route('/home_page', methods=['GET', 'POST'])
def home():
    UID = login_session['user']['localId']
    recipes = None  
    if request.method == "POST":
        title = request.form['title']
        optional = request.form['optional']
        x = request.form['ingredients']
        ste = request.form['steps']
        steps = ste.split(',')
        ingredients = x.split()
        recipe = {'title': title, 'optional': optional, 'ingredients': ingredients, 'steps': steps, "uid": UID}
        db.child('Recipes').push(recipe)
        return redirect(url_for('home'))
    else:
        recipes = db.child('Recipes').get().val()
    return render_template('home.html', recipes=recipes)


if __name__ == '__main__':
    app.run(debug=True)