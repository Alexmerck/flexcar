from flask import render_template, flash, redirect, url_for
from webapp import app


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

