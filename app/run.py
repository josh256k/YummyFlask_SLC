
from flask import Flask, flash, render_template, session, url_for, redirect, request
from models import User, Category, Recipe

app = Flask(__name__)
app.secret_key = 'secret'
Users = {}


def register(firstname, lastname, email, password):
    """ This function handles user registration"""
    if firstname and lastname and email and password:
        Users[email] = User(firstname, lastname, email, password)
        return "Registration successful"
    return "None input"


def login(email, password):
    """ Handles user login """
    if email and password:
        if Users.get(email):
            if Users[email].password == password:
                return "Login successful"
            return "Wrong password"
        return "User not found"
    return "None input"


@app.route("/")
def main():
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """ Handles the sign_up route """
    if request.method == 'POST':
        # creating an instance of the register fuction
        returnvalue = register(request.form['firstname_field'], request.form['lastname_field'],
                               request.form['email_field'], request.form['password_field'])
        if returnvalue == "Registration successful":
            flash(returnvalue, 'info')
            return redirect(url_for('showlogin'))
        flash(returnvalue, 'warning')
    return render_template('signup.html')


@app.route("/showlogin", methods=['POST', 'GET'])
def showlogin():
    """ Handles the login route """
    if request.method == 'POST':
        result = login(request.form['email_field'],
                       request.form['password_field'])
        if result == "Login successful":
            session['email'] = request.form['email_field']
            return redirect(url_for('category'))
        flash(result, 'warning')
    return render_template('login.html')


@app.route('/category', methods=['POST', 'GET'])
def category():

    return render_template('dashboard.html', categories=Users[session['email']].categories)


@app.route('/add_category', methods=['GET', 'POST'])
def add_category():
    if request.method == 'POST':
        return_value = Users[session['email']
                             ].add_category(request.form['title'])
        if return_value == True:
            return redirect(url_for('category'))
    return render_template('dashboard.html', categories=Users[session['email']].categories)


@app.route('/delete_category/<title>', methods=['POST', 'GET'])
def delete_category(title):
    result = Users[session['email']].delete_category(title)
    if result == True:
        flash("delete successful")
    else:
        flash(result, 'warning')
    return redirect(url_for('category'))


@app.route('/edit_category/<title>', methods=['POST', 'GET'])
def edit_category(title):
    session['category_title'] = title
    if request.method == 'POST':
        return_value = Users[session['email']].edit_category(
            session['category_title'], request.form['title'])
        if return_value == True:
            return redirect(url_for('category'))
            flash("edited category")
    return render_template('editcategory.html')


@app.route('/show_recipe/<category_title>', methods=['GET', 'POST'])
def show_recipe(category_title):
    """ Handles displaying recipes """
    session['current_category_title'] = category_title
    return render_template('viewrecipe.html', recipes=Users[session['email']]
                           .categories[category_title].recipes)


@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    """ Handles new addition of recipes requests """
    if request.method == 'POST':
        result = Users[session['email']].categories[session['current_category_title']].add_recipe(
            request.form['name'], request.form['contents'], request.form['instructions'])
        if result == True:
            flash("recipe added")
        else:
            flash("Not added")
        return redirect(url_for('show_recipe', category_title=session['current_category_title']))
    return render_template('addrecipe.html', recipes=Users[session['email']]
                           .categories[session['current_category_title']].recipes)
@app.route('/delete_recipe/<name>',methods=['GET', 'POST'])
def delete_recipe(name):
    """ Handles request to delete a recipe """
    result = Users[session['email']].categories[session['current_category_title']].delete_recipe(
        name)
    if result == True:
        flash("deleted")
    else:
        flash("not deleted")
    return redirect(url_for('show_recipe', category_title=session['current_category_title']))

if __name__ == "__main__":
    app.run(debug=True)