from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.sighting import Sighting

@app.route('/dashboard')
def dashboard():   
    if 'user_id' not in session:
        return redirect('/')
    all_the_sightings = Sighting.get_all_sightings()
    return render_template("dashboard.html", all_the_sightings=all_the_sightings)


@app.route('/new/sighting')
def new_recipe_page():   
    if 'user_id' not in session:
        return redirect('/')
    return render_template("new.html")

@app.route('/sightings/create', methods=['POST'])
def create():
    if 'user_id' not in session:
        return redirect('/')
    if not Sighting.validate_sighting(request.form):
        return redirect('/new/sighting')
    data = {
    "location": request.form['location'],
    "description": request.form['description'],
    "sightingsdate": request.form['sightingsdate'],
    "sasquatchnumber": request.form['sasquatchnumber'],
    "users_id": session['user_id']
    }
    sighting_id = Sighting.save(data)
    return redirect('/dashboard')

@app.route('/show/<int:sighting_id>')
def show(sighting_id):
    if 'user_id' not in session:
        return redirect('/')
    sighting = Sighting.get_one_sighting(sighting_id)
    return render_template("view.html", sighting = sighting )

@app.route('/edit/<int:sighting_id>')
def editpage(sighting_id):
    if 'user_id' not in session:
        return redirect('/')
    sighting = Sighting.get_one_sighting(sighting_id)
    if sighting.users_id != session['user_id']:
        return redirect('/')
    return render_template("edit.html", sighting = sighting)

@app.route('/edit', methods=['POST'])
def edit():
    if 'user_id' not in session:
        return redirect('/')
    sighting = Sighting.get_one_sighting(request.form['id'])
    if sighting.users_id != session['user_id']:
        return redirect('/')
    if not Sighting.validate_sighting(request.form):
        redirect_url = '/edit/' + request.form['id']
        return redirect(redirect_url)
    data = {
    "id": request.form['id'],
    "location": request.form['location'],
    "description": request.form['description'],
    "sightingsdate": request.form['sightingsdate'],
    "sasquatchnumber": request.form['sasquatchnumber'],
    }
    sighting_id = Sighting.edit(data)
    return redirect('/dashboard')

@app.route('/sightings/delete/<int:sighting_id>')
def delete(sighting_id):
    Sighting.delete(sighting_id)
    return redirect('/dashboard')
