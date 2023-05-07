import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import json 
db = SQLAlchemy()

# Table scheme for the database
class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_name = db.Column(db.String(100), nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(80), nullable=False)
    # updated = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    desc = db.Column(db.Text)

    def __repr__(self):
        return f'<Job {self.job_name}>'
# Function to create the joblist from json 
def create_job_list(jsob):
    joblist = list()
    json_data = json.dumps(jsob)
    # print(jsob.keys())
    # print(len(jsob.keys()))
    # print(jsob["data"][0]['employer_name'])
    actual_data = jsob["data"]
    for i in range(0,len(actual_data)):
        company_name = actual_data[i]["employer_name"]
        job_apply_link = actual_data[i]["job_apply_link"]
        job_role = actual_data[i]["job_title"]
        job = createJob(job_role=job_role,company_name=company_name,link = job_apply_link)
        joblist.append(job)
        db.session.add(job)
        db.session.commit()
    return joblist


# Function to add data to the database from csv

def add_data_to_db(db,joblist):
    df = pd.read_csv('static\Combined01&02.csv')
    data_size = len(df)
    print(data_size)
    for i in range(0,data_size):
        company_name = df.loc[i,"employer_name"]
        job_apply_link = df.loc[i,"job_apply_link"]
        job_role =  df.loc[i,"job_title"]
        job = createJob(job_role=job_role,company_name=company_name,link = job_apply_link)
        db.session.add(job)
        db.session.commit()

# Function to make job instance
def createJob(job_role, company_name, link):
    return Job(job_name=job_role, company_name=company_name, link=link)
