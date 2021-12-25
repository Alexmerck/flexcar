from flask import render_template, flash, redirect, url_for, request
from webapp import app
from webapp.forms import CarinputForm


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Alex'}
    post = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, post=post)


@app.route('/usercars')
def usercar():
    user = {'username': 'testuser'}
    carlist =[
        {'manufacturer': 'BMW',
        'model':'X1'},
        {'manufacturer': 'ff',
        'model':'X176'},
        {'manufacturer': 'deawoo',
        'model':'1'}
        ]
    return render_template('usercars.html', title = 'GARAGE', user = user, carlist = carlist)


@app.route('/carinput')
def сarinput():
    title = "Добавление авто в гараж"
    сarinput_form = CarinputForm()
    return render_template('carinput.html', page_title=title, form=сarinput_form)