from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_registration(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
    "first_name": request.form["first_name"],
    "last_name" : request.form["last_name"],
    "email" : request.form["email"],
    "password" : pw_hash,
    }
    user_id = User.save(data)
    session['user_id'] = user_id
    session['user_name'] = request.form["first_name"]
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    data = { "email" : request.form["email"] }
    user_in_db = User.get_user_by_email(data)
    if not user_in_db:
        flash("A user with this email address does not exist. Please register first.", 'login')
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Password", 'login')
        return redirect('/')
    session['user_id'] = user_in_db.id
    session['user_name'] = user_in_db.first_name
    return redirect("/dashboard")

@app.route('/logout')
def logout():
    session.clear()
    return redirect ('/')