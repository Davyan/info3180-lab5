"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

This file creates your application.
"""

from app import app
from flask import render_template, request, redirect, url_for,jsonify,g,session
from app import db

from app.models import Myprofile
from app.forms import LoginForm,ProfileForm

from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid


@app.before_request
def before_request():
    g.user = current_user
    
@app.before_request
def before_request():
    g.user = None
    if 'openid' in session:
        g.user = User.query.filter_by(openid=session['openid']).first()
    
@lm.user_loader
def load_user(id):
    return MyProfile.query.get(int(id))
    
###
# Routing for your application.
###

@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    print app.config['OPENID_PROVIDERS']
    if form.validate_on_submit():
        openid = request.form.get('openid')
        if openid:
        # user = MyProfile.query.filter_by(username=username).first()
        # if user.username==form.username.data and user.password==form.password.data:
        #     userid = MyProfile.query.get(int(id))
        #     loggeduser =load_user(userid)
        #     login_user(loggeduser)
            session['remember_me'] = form.remember_me.data
            oid.try_login(form.openid.data, ask_for=['username', 'password'])
            return redirect(request.args.get("next") or url_for("home"))
    return render_template('login.html', title='Sign In',form=form, providers=app.config['OPENID_PROVIDERS'])
                           
@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    user = MyProfile.query.filter_by(email=resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        user = MyProfile(nickname=nickname, email=resp.email)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember = remember_me)
    return redirect(request.args.get('next') or url_for('index'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
    
@app.route('/')
@login_required
def home():
    user = g.user
    return render_template('home.html',user=user)

@app.route('/profile/', methods=['POST','GET'])
def profile_add():
    form = ProfileForm()
    print openid
    if request.method == 'POST':
        # write the information to the database
       
        newprofile = Myprofile(first_name=form.first_name.data,last_name=form.last_name.data,username=form.username.data,email=form.email.data,password=form.password.data)
        db.session.add(newprofile)
        db.session.commit()

        return "{} {} was added to the database".format(request.form['first_name'],
                                             request.form['last_name'])

    form = ProfileForm()
    return render_template('profile_add.html',
                           form=form)

@app.route('/profiles/',methods=["POST","GET"])
def profile_list():
    profiles = Myprofile.query.all()
    if request.method == "POST":
        return jsonify({"age":4, "name":"John"})
    return render_template('profile_list.html',
                            profiles=profiles)

@app.route('/profile/<int:id>')
def profile_view(id):
    profile = Myprofile.query.get(id)
    return render_template('profile_view.html',profile=profile)


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')


###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8888")
