from flask import render_template
from app import app
from app.forms import LoginForm, RegistrationForm, PostForm, ThreadForm
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post, Thread
from app import db
from werkzeug.urls import url_parse
import logging

gyms = [ \
    {'organization': 'KiipeilyAreena',\
        'name': 'Salmisaari',\
        'price': 'One-time payment Mon-Fri 10am - 4pm: <br> Adult 10 &euro; (shoes 14&euro;) <br> <br> One-time payment Mon-Fri 4pm - 10pm: <br> Adult (Lead) 16 &euro; (equipment 22&euro;) <br> Adult (Bouldering) 13 &euro; (shoes 17&euro;) <br> Child 10 &euro; (shoes 16&euro;) <br> (Additional information and prices on the website)',\
        'schedule':'Mo-Fri 10h00-22h00 | Sat-Sun 10h00-20h00</div>',\
        'types':'Lead, Bouldering',\
        'coordinates': [60.165756, 24.903293],\
        'website':'https://kiipeilyareena.com/',\
        },\
    {'organization': 'KiipeilyAreena',\
        'name': 'Kalasatama',\
        'price': 'One-time payment Mon-Fri 10am - 4pm: <br> Adult 10 &euro; (shoes 14&euro;) <br> <br> One-time payment Mon-Fri 4pm - 10pm: <br> Adult 13 &euro; (shoes 17&euro;) <br> Child 10 &euro; (shoes 16&euro;) <br> (Additional information and prices on the website)',\
        'schedule':'Mo-Fri 10h00-22h00 | Sat-Sun 10h00-20h00',\
        'types':'Bouldering',\
        'coordinates': [60.186183, 24.978350],\
        'website':'https://kiipeilyareena.com/',\
        },\
    {'organization': 'KiipeilyAreena',\
        'name': 'Tammisto',\
        'price': 'One-time payment Mon-Fri 10am - 4pm: <br> Adult 10 &euro; (shoes 14&euro;) <br> <br> One-time payment Mon-Fri 4pm - 10pm: <br> Adult 13 &euro; (shoes 17&euro;) <br> Child 10 &euro; (shoes 16&euro;) <br> (Additional information and prices on the website)',\
        'schedule':'Mo-Fri 10h00-22h00 | Sat-Sun 10h00-20h00',\
        'types':'Bouldering',\
        'coordinates': [60.282405, 24.971577],\
        'website':'https://kiipeilyareena.com/',\
        },\
    {'organization': 'Boulderkeskus',\
        'name': 'Herttoniemi',\
        'price': 'One-time payment Mon-Fri 10am - 3pm: <br> Adult 9 &euro; <br> Child 5 &euro; <br> <br> One-time payment Mon-Fri 3pm - 9pm: <br> Adult 12 &euro; <br> Child 6 &euro; <br> <br> One-time payment Sat-Sun: <br> Adult 12 &euro; <br> Child 6 &euro; <br> (Additional information and prices on the website)',\
        'schedule':'Mo-Fri 10h00-21h00 | Sat-Sun 12h00-18h00',\
        'types':'Bouldering',\
        'coordinates': [60.203830, 25.047545],\
        'website':'https://www.boulderkeskus.com',\
        },\
    {'organization': 'Boulderkeskus',\
        'name': 'Konala',\
        'price': 'One-time payment Mon-Fri 10am - 3pm: <br> Adult 9 &euro; <br> Child 5 &euro; <br> <br> One-time payment Mon-Fri 3pm - 9pm: <br> Adult 12 &euro; <br> Child 6 &euro; <br> <br> One-time payment Sat-Sun: <br> Adult 12 &euro; <br> Child 6 &euro; <br> (Additional information and prices on the website)',\
        'schedule':'Mo-Fri 10h00-21h00 | Sat-Sun 12h00-18h00',\
        'types':'Bouldering',\
        'coordinates': [60.236702, 24.859604],\
        'website':'https://www.boulderkeskus.com',\
        },\
    {'organization': 'Boulderkeskus',\
        'name': 'Pasila',\
        'price': 'One-time payment Mon-Fri 10am - 3pm: <br> Adult 9 &euro; <br> Child 5 &euro; <br> <br> One-time payment Mon-Fri 3pm - 9pm: <br> Adult 12 &euro; <br> Child 6 &euro; <br> <br> One-time payment Sat-Sun: <br> Adult 12 &euro; <br> Child 6 &euro; <br> (Additional information and prices on the website)',\
        'schedule':' Mo-Fri 10h00-21h00	| Sat-Sun 12h00-18h00',\
        'types':'Bouldering',\
        'coordinates': [60.195968, 24.932598],\
        'website':'https://www.boulderkeskus.com',\
        },\
    {'organization': 'Boulderkeskus',\
        'name': 'Espoo',\
        'price': 'One-time payment Mon-Fri 10am - 3pm: <br> Adult 9 &euro; <br> Child 5 &euro; <br> <br> One-time payment Mon-Fri 3pm - 9pm: <br> Adult 12 &euro; <br> Child 6 &euro; <br> <br> One-time payment Sat-Sun: <br> Adult 12 &euro; <br> Child 6 &euro; <br> (Additional information and prices on the website)',\
        'schedule':'Mo-Fri 10h00-21h00 | Sat-Sun 10h00-18h00',\
        'types':'Bouldering',\
        'coordinates': [60.166007, 24.702586],\
        'website':'https://www.boulderkeskus.com',\
        },\
    {'organization': 'KiipeilyKeskus',\
        'name': 'Helsinki',\
        'price': 'One-time payment Mon-Fri 9am - 4pm / 8pm - 10pm: <br> Adult 9 &euro; <br> <br> One-time payment Mon-Fri 4pm - 8pm: <br> Adult 12 &euro; <br> <br> One-time payment Sat-Sun: <br> Adult 12 &euro; <br> (Additional information and prices on the website)',\
        'schedule':'Mo-Fri 09h00-22h00 | Sat-Sun 10h00-20h00',\
        'types':'Lead, Bouldering',\
        'coordinates': [60.265213, 25.016267],\
        'website':'http://kiipeilykeskus.com/eng',\
        },\
]

@app.route('/')
@app.route('/index')
def index():
    app.logger.info('testing info log')
    return render_template('index.html', title='Home', gyms=gyms)

@app.route('/maps')
def maps():
    return render_template('maps.html', title="Maps", gyms=gyms)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
		#redirect to next=... that is in the url
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)

@app.route('/forum')
def forum():
    threads = Thread.query.order_by(Thread.timestamp.desc()).all()
    return render_template('forum.html', title="Forum", threads=threads)

@app.route('/createthread', methods=['GET','POST'])
@login_required
def createthread():
    form = ThreadForm()
    if form.validate_on_submit():
        thread = Thread(title=form.threadname.data, author=current_user)
        post = Post(body=form.post.data, author=current_user, thread=thread)
        db.session.add(thread)
        db.session.add(post)
        db.session.commit()
        flash('your post is now live!')
        return redirect(url_for('forum'))
    return render_template("createthread.html", title="Write a post", form=form)

@app.route('/thread/<thread_id>',methods=['GET','POST'])
def thread(thread_id):
    form=PostForm()
    if form.validate_on_submit():
        post=Post(body=form.post.data, author=current_user,thread_id=thread_id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('thread',thread_id=thread_id))
    thread = Thread.query.filter_by(id=thread_id).first_or_404()
    posts = Post.query.filter_by(thread_id=thread_id)
    return render_template('thread.html', thread = thread, posts=posts, form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))