# -*- coding: UTF-8 -*-
from flask import render_template, redirect, url_for, request
from flask_login import LoginManager, login_required, login_user, logout_user

from app.auth.forms import SignInForm
from app.auth.forms import SignUpForm

from app.blueprints import auth
from app.user.models import User

from app.extensions import db
from app.extensions import login_manager


@login_manager.user_loader
def load_user(userid):
    return User.query.filter(User.id == userid).first()


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = SignInForm()
    #if form.validate_on_submit():
    if form.validate() and form.is_submitted():
        user = User.query.filter_by(email=form.email.data).first_or_404()
        if user.is_correct_password(form.password.data):
            login_user(user)

            next = request.args.get('next')
            return redirect(next or url_for('home.index'))
        else:
            #return redirect(url_for('auth.login'))
            return "<script>alert('Logged in failed!');setTimeout(function(){window.location.href='http://127.0.0.1:5000/';}, 500);</script>"

    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    #return 'Logged out successfully!'
    return "<script>alert('Logged out successfully!');setTimeout(function(){window.location.href='http://127.0.0.1:5000/';}, 500);</script>"


