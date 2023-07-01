from flask import Flask, render_template, request, redirect, url_for
from data import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/internships/<program_type>')
def internships(program_type):
    programs_list = read_programs_by_program_type(program_type)
    return render_template("internship.html", program_type=program_type, programs=programs_list)

@app.route('/internships/<int:program_id>')
def program(program_id):
    program = read_programs_by_program_type(program_id)
    return render_template("program.html",program=program)


@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/processed', methods=['post'])
def processing():
    program_data = {
        "program_type": request.form['program_type'],
        "program_name": request.form['program_name'],
        "salary": request.form['program_salary'],
        "duration": request.form['program_duration'],
        "description": request.form['program_desc'],
        "url": request.form['program_url']
    }
    insert_program(program_data)
    return redirect(url_for('internships', program_type=request.form['program_type']))


@app.route('/modify', methods=['post'])
def modify():
    # 1. identify whether user clicked edit or delete
       # if edit, then do this:
    if request.form["modify"] == "edit":
        # retrieve record using id
        program_id = request.form["program_id"]
        program = read_programs_by_program_type(program_id)
        # update record with new data
        return render_template('update.html', program=program)
    # if delete, then do this
    elif request.form["modify"] == "delete":
        # retrieve record using id
        program_id = request.form["program_id"]
        program = read_programs_by_program_type(program_id)
        # delete the record
        delete_program(program_id)
        # redirect user to program list by program type
        return redirect(url_for("internships", program_type=program["program_type"]))

@app.route('/update', methods=['post'])
def update():
    program_data = {
        "program_id" : request.form["program_id"],
        "program_type": request.form['program_type'],
        "program_name": request.form['program_name'],
        "salary": request.form['program_salary'],
        "duration": request.form['program_duration'],
        "description": request.form['program_desc'],
        "url": request.form['program_url']
    }
    update_program(program_data)
    return redirect(url_for('program',program_id = request.form['program_id']))

def delete_program(program_id):
    conn, cur = connect_to_db(db_path)
    query = "DELETE FROM programs WHERE id = ?"
    values = (program_id,)
    cur.execute(query, values)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    app.run(debug=True)