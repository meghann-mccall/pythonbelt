from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.skeptic import Skeptic


@app.route('/skeptics/addme/<int:sighting_id>')
def addme(sighting_id):   
    if 'user_id' not in session:
        return redirect('/')
    data = {
    "sightings_id": sighting_id,
    "users_id": session['user_id']
    }
    skeptic_id = Skeptic.save(data)
    redirect_url = '/show/' + str(sighting_id)
    return redirect(redirect_url)

@app.route('/skeptics/delete/<int:sighting_id>')
def deleteskeptic(sighting_id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
    "sightings_id": sighting_id,
    "users_id": session['user_id']
    }
    Skeptic.delete(data)
    redirect_url = '/show/' + str(sighting_id)
    return redirect(redirect_url)
