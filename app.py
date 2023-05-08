import os
import json
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import datetime
from sqlalchemy.sql import func
import pandas as pd
from database import db,Job,create_job_list

#Things 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String,or_
from sqlalchemy.sql.expression import and_

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
def search_results():
    query = request.args.get('query')
    if query:
        search_words =  query.split()

        # Create a list of filter conditions using or_()
        filter_condition1 = [Job.desc.ilike(f'%{word}%') for word in search_words]
        filter_condition2 = [Job.job_role.ilike(f'%{word}%') for word in search_words]

        # Combining the filter conditions using or_()
        db_query = db.session.query(Job).filter(and_(*filter_condition2,*filter_condition1))
        # print(query)
        print(search_words)
        # Retrieve the matching records
        results = db_query.all()
        print(len(results))
        if len(results)==0:
            app.logger.info("API CALLED")
            from api import api_call
            js_results = api_call(query)
            print(js_results)
        
            res = create_job_list(js_results)
            
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

def init_db():
    db.create_all()        
with app.app_context():
    from database import updateDatabase,create_job_list,add_data_to_db
    add_data_to_db(db)
  
    app.run(debug=True)
if __name__=="main":
    init_db()