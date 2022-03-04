from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.listing_mod import Listings
from flask_app.models.user_mod import Users

# Add template for "new listing"
@app.route('/new_listing/<int:userId>')
def create_listing(userId):
    if 'userId' not in session:
        return redirect('/')
    userId = session['userId']
    return render_template('create.html', current_user = userId)

@app.route('/process_listing/<int:userId>', methods=['POST'])
def process_listing(userId):
    userId = session['userId']
    if not Listings.validate_listing(request.form):
        return redirect(f'/new_listing/{userId}') 
    
    data = {
        'title': request.form['title'],
        'description': request.form['description'],
        'listPrice': request.form['listPrice'],
        'imgURL': request.form['imgURL'],
        'userId': session['userId']
    }
    Listings.save_listing(data)
    return redirect(f'/profile/{userId}')

@app.route('/edit_listing/<int:userId>/<listingID>')
def edit_listing(userId, listingID):
    userId = session['userId']
    data = {
        'id': listingID
    }
    one_listing = Listings.get_one_listing(data)
    return render_template('edit.html', current_user = userId, listing = one_listing)

@app.route('/update_listing/<int:userId>/<listingID>', methods=['POST'])
def update_listing(userId, listingID):
    userId = session['userId']
    if 'userId' not in session:
        return redirect('/')
    if not Listings.validate_edit(request.form):
        return redirect(f'/edit_listing/{userId}/{listingID}')
    data = {
        'id': listingID,
        'title': request.form['title'],
        'description': request.form['description'],
        'listPrice': request.form['listPrice'],
        'imgURL': request.form['imgURL'],
        'userId': session['userId']
    }
    Listings.update_listing(data)
    return redirect(f'/profile/{userId}')

@app.route('/view_listing/<int:userId>/<listingID>')
def single_listing(userId, listingID):
    session['userId'] = userId
    if 'userId' not in session:
        return redirect('/')
    data = {
        'id': listingID

    }
    Listings.get_one_listing(data)
    
    return render_template('view.html', listing_info = Listings.get_one_listing(data))

@app.route('/delete_listing/<int:userId>/<listingID>')
def delete_listing(userId, listingID):
    userId = session['userId']
    if 'userId' not in session:
        return redirect('/')
    data = {
        'id': listingID
    }
    Listings.delete_listing(data)
    return redirect(f'/profile/{userId}')

@app.route('/like_listing/<int:userId>/<listingID>')
def like_listing(userId, listingID):
    if 'userId' not in session:
        return redirect('/')
    data = {
        'userID': userId,
        'listingID' : listingID
    }

    Listings.like_listing(data)

    return redirect('/')

@app.route('/unlike_listing/<int:userId>/<listingID>')
def unlike_listing(userId, listingID):
    if 'userId' not in session:
        return redirect('/')
    data = {
        'userID': userId,
        'listingID' : listingID
    }

    Listings.unlike_listing(data)

    return redirect(f'/profile/{userId}')




