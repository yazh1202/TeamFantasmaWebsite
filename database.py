import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import json 
db = SQLAlchemy()

# Table scheme for the database
class Job(db.Model):
    id = db.Column(db.String(40), primary_key=True)
    job_role = db.Column(db.String(100), nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(80), nullable=True)
    location = db.Column(db.String(80),nullable=True)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    desc = db.Column(db.Text)

    def __repr__(self):
        return f'<Job {self.job_role}>'
        
# Function to create the joblist from json 
def create_job_list(jsob):
    joblist = list()
    # json_data = json.dumps(jsob)
    actual_data = jsob["data"]
    for i in range(0,len(actual_data)):
        desc = actual_data[i]["job_description"]
        id = actual_data[i]["job_id"]
        company_name = actual_data[i]["employer_name"]
        job_apply_link = actual_data[i]["job_apply_link"]
        job_role = actual_data[i]["job_title"]
        
        #Location
        city = actual_data[i]['job_city']
        state = actual_data[i]['job_state']
        country = actual_data[i]['job_country']
        job_location = str(f'{city}, {state}, {country}')

        #Creating job
        job = createJob(lc = job_location,desc = desc,id=id,role=job_role,company=company_name,link = job_apply_link)
        joblist.append(job)
        db.session.merge(job)
         

        db.session.commit()
    return joblist


# Function to add data to the database from a csv file

def add_data_to_db(db):
    # df = pd.read_csv('static/CSV_DATA4.csv')
    data_size = len(df)
    for i in range(0,data_size):
        company_name = df.loc[i,"employer_name"]
        job_apply_link = df.loc[i,"job_apply_link"]
        job_role =  df.loc[i,"job_title"]
        job_desc = replace_full_stops(df.loc[i,'job_description'])
        job_id = df.loc[i,"job_id"]
        #Location
        city = df.loc[i,'job_city']
        state = df.loc[i,'job_state']
        country = df.loc[i,'job_country']
        job_location = str(f'{city}, {state}, {country}')

        job = createJob(lc = job_location,desc = job_desc,id=job_id,role=job_role,company=company_name,link = job_apply_link)
        db.session.merge(job)
        db.session.commit()

# Helper method to replace the full stops with linebreaks
def replace_full_stops(string):
    return string.replace('<br>', '\n')

# Function  to update db
def updateDatabase():
    mainData = Job.query.all()
    for row in mainData:
        row.location = row.location.replace("nan"," ")
        row.location = row.location.replace(","," ")
        db.session.commit()

# Function to make job instance
def createJob(id,role, company,lc,desc,link):
    return Job(id = id,job_role=role, company_name=company,location=lc,desc=desc, link=link)