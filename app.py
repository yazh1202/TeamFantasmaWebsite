import os
import json
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import datetime
from sqlalchemy.sql import func
import pandas as pd
from database import db,Job,create_job_list
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def index():
    jobs = Job.query.all()
    return render_template('home.html', jobs=jobs, utc_dt=datetime.datetime.utcnow())


@app.route('/search',methods=['GET'])
def search_handle():
    query = request.args.get('query')
    if query:
        results = Job.query.filter(Job.job_name.like(query)).all()
        if len(results)==0:
            app.logger.info("API CALLED")
            from api import api_call
            js_results = api_call(query)
        
            res = create_job_list(js_results)
            print(res)
            return render_template('home.html',jobs = res)

        return render_template('home.html',jobs = results)
    else:
        all_jobs = Job.query.all()
       
        return render_template('home.html',jobs = all_jobs)



@app.route('/api',methods=['POST'])
def api_handle():
    button_value = request.form['button']
    if button_value=="CallButton":
        print("The Button is Clicked Now")
    from api import apiCall
    
    return render_template()

# Function to redirect the URL

@app.route('/redirect', methods=['POST'])
def redirect_external():
    external_url = request.form.get('external_url')
    return redirect(external_url)

with app.app_context():
    db.create_all()
    from database import add_data_to_db
    add_data_to_db(db)
    app.run(debug=True)
    