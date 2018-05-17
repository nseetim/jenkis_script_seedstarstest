# Import statements
from jenkinsapi.jenkins import Jenkins 
import sqlite3
from datetime import datetime

# Define the Jenkins server parameters
jenkins_url = 'http://172.82.162.36:8080'
username = 'jenkinstest'
password = 'jenkinstest1'

# Database details
db_name = 'jenkins_test.db'  # sqlite database path

# get server instance
server = Jenkins(jenkins_url, username, password)

# create dictionary that holds the jobs name as keys and status as values
jobs_dict = {}

# connect to database
connection = sqlite3.connect(db_name)
conn = connection.cursor()

for job_name, job_instance in server.get_jobs():
    if job_instance.is_running():
        status = 'RUNNING'
    elif job_instance.get_last_build_or_none() is None:
        status = 'NOT-BUILT'
    else:
        simple_job = server.get_job(job_instance.name)
        simple_build = simple_job.get_last_build()
        status = simple_build.get_status()

    i = datetime.now()
    checked_time = i.strftime('%Y/%m/%d %H:%M:%S')
    job_lists1 = (job_instance.name, status, checked_time)
    conn.execute("SELECT id FROM jenkins WHERE job_name = ?", (job_instance.name,))
    data = conn.fetchone()
    if data is None:
        conn.execute('INSERT INTO jenkins (job_name, status, date_checked) VALUES (?,?,?)', job_lists1)
    else:
        job_lists2 = (status, checked_time, job_instance.name)
        conn.execute('UPDATE jenkins SET status=?, date_checked=? WHERE job_name=?', job_lists2)

    # Add to dictionary
    dict[job_instance.name] = status

# Save (commit) the changes
connection.commit()

# We can close the connection
connection.close()
