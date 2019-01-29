#!/usr/bin/env python3

from flask import Flask, render_template, request, redirect, url_for
from flask import flash, jsonify
from functools import wraps

# import CRUD
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Category, Base, CategoryItem, User

from flask import session as login_session

import random
import string

# IMPORTS FOR THIS STEP

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog App"

# create a session to the DB
engine = create_engine('sqlite:///itemscatalogwithusersandtime.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in login_session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(
            json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')

    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user has an account, else create a new account
    user_id = getUserId(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;'
    output += '-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    # print "done!"

    return output


# DISCONNECT - Revoke a current user's token and reset their login_session

@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        # Reset the user's sesson.
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'

        return response


# User helper functions
def createUser(login_session):
    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserId(email):
    user = session.query(User).filter_by(email=email).one()
    return user.id


# Making an API Endpoint for all categories(GET Request)
@app.route('/JSON')
@app.route('/catalog/all/JSON')
def categoriesAllJSON():
    categories = session.query(Category).all()
    return jsonify(Categories=[i.serialize for i in categories])


# Endpoint to GET all categories
@app.route('/')
@app.route('/catalog/all/')
def categoriesAll():
    # display all categories
    categories = session.query(Category).all()
    items = session.query(CategoryItem).order_by(
                          CategoryItem.last_updated.desc()).limit(10).all()
    if 'username' not in login_session:
        return render_template('publiccatalog.html',
                               categories=categories, items=items)
    else:
        return render_template('catalog.html', categories=categories,
                               items=items)


# API endpoint for all items in a category
@app.route('/catalog/<path:category_name>/items/JSON')
def itemsByCategoryJSON(category_name):
    category = session.query(Category).filter_by(name=category_name).first()
    items = session.query(CategoryItem).filter_by(category=category)
    return jsonify(CategoryItems=[i.serialize for i in items])


# Endpoint to show the items by category
@app.route('/catalog/<path:category_name>/items')
def itemsByCategory(category_name):
    category = session.query(Category).filter_by(name=category_name).first()
    items = session.query(CategoryItem).filter_by(category=category)
    if 'username' not in login_session:
        return render_template('publiccatalogitems.html',
                               category=category, items=items)
    else:
        return render_template('catalogitems.html',
                               category=category, items=items)


# Endpoint to show description of an item
@app.route('/catalog/<path:category_name>/<path:item_name>')
def displayItem(category_name, item_name):
    category = session.query(Category).filter_by(name=category_name).first()
    itemDetail = session.query(CategoryItem).filter_by(name=item_name).one()
    if 'username' not in login_session:
        return render_template('publicitemdetails.html', category=category,
                               itemDetail=itemDetail)
    else:
        return render_template('itemdetails.html', category_name=category_name,
                               itemDetail=itemDetail)


# Endpoint to add a new item
@app.route('/catalog/<path:category_name>/new', methods=['GET', 'POST'])
@login_required
def addCategoryItem(category_name):
    message = "Please Fill Out All Required Fields"
    if (request.method == 'POST'):
        category = session.query(Category).filter_by(
                                    name=request.form['category']).first()
        newItem = CategoryItem(name=request.form['name'],
                               description=request.form['description'],
                               category=category)
        if newItem.name == "":
            print("Empty Item Name")
            message = "Error: Empty Item Name, please fill out all fields"
            return render_template('addcategoryitem.html',
                                   category_name=category_name,
                                   message=message)
        else:
            session.add(newItem)
            session.commit()
            items = session.query(CategoryItem).filter_by(category=category)
            return render_template('catalogitems.html',
                                   category=category,
                                   items=items)
    else:
        return render_template('addcategoryitem.html',
                               category_name=category_name, message=message)


# Endpoint to edit an item
@app.route('/catalog/<path:category_name>/<path:item_name>/edit',
           methods=['GET', 'POST'])
@login_required
def editCategoryItem(category_name, item_name):
    editItem = session.query(CategoryItem).filter_by(name=item_name).one()
    # Get the creator of this item
    creator = getUserInfo(editItem.user_id)

    # Is the creator the same as the logged in user?
    if creator.id != login_session['user_id']:
        return redirect('login')

    if request.method == 'POST':
        if request.form['name']:
            editItem.name = request.form['name']
        if request.form['description']:
            editItem.description = request.form['description']
        if request.form['category']:
            category_name = request.form['category']
            category = session.query(Category).filter_by(
                                        name=category_name).first()
            editItem.category = category
        session.add(editItem)
        session.commit()
        return redirect(url_for('displayItem', category_name=category_name,
                                item_name=editItem.name))
    else:
        return render_template('editcategoryitem.html',
                               category_name=category_name, item=editItem)


# Endpoint to delete an item
@app.route('/catalog/<path:category_name>/<path:item_name>/delete',
           methods=['GET', 'POST'])
@login_required
def deleteCategoryItem(category_name, item_name):
    item = session.query(CategoryItem).filter_by(name=item_name).one()
    # Get the creator of this item
    creator = getUserInfo(editItem.user_id)

    # Is the creator the same as the logged in user?
    if creator.id != login_session['user_id']:
        return redirect('login')

    if request.method == 'POST':
        session.delete(item)
        session.commit()
        return redirect(url_for('itemsByCategory',
                                category_name=category_name))
    else:
        return render_template('deletecategoryitem.html',
                               category_name=category_name, item=item)


if __name__ == '__main__':
    # app.debug = True
    app.secret_key = 'super_secret_key'
    app.run(host='0.0.0.0', port=5000)
