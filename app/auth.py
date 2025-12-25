from flask import Blueprint, render_template, redirect, url_for, flash, request
from .forms import LoginForm, RegisterForm
from .models import User
from . import db
from flask_login import login_user, logout_user, login_required

bp = Blueprint('auth', __name__, template_folder='templates')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        identifier = form.identifier.data
        user = User.query.filter_by(username=identifier).first() or User.query.filter_by(email=identifier).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('web.index'))
        flash('Invalid username or password')
    return render_template('login.html', form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('web.index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already taken')
            return render_template('register.html', form=form)
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already registered')
            return render_template('register.html', form=form)
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. Please log in.')
        return redirect(url_for('auth.login'))
    else:
        # show validation errors for debugging/testing
        if request.method == 'POST':
            flash('Validation errors: ' + str(form.errors))
    return render_template('register.html', form=form)
