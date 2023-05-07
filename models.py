
def addToDB(job,db):
    db.session.add(job)
    db.session.commit()
