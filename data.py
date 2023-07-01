import sqlite3

db_path = "pa.db"

# This function conencts to the DB and returns a conn and cur objects
def connect_to_db(path):
    conn = sqlite3.connect(path)
    # Converting tuples to dictionaries
    conn.row_factory = sqlite3.Row
    return (conn, conn.cursor())

# This function returns programs by program_type
def read_programs_by_program_type(program_type):
    conn, cur = connect_to_db(db_path)
    query = 'SELECT * FROM programs WHERE program_type = ?'
    value = program_type
    results = cur.execute(query,(value,)).fetchall()
    conn.close()
    return results

# This function retrieves 1 program by program_id
def read_programs_by_program_id(program_id):
    conn, cur = connect_to_db(db_path)
    query = 'SELECT * FROM programs WHERE id = ?'
    value = program_id
    result = cur.execute(query,(value,)).fetchone()
    conn.close()
    return result

# This function inserts 1 program data
def insert_program(program_data):
    conn, cur = connect_to_db(db_path)
    query = 'INSERT INTO programs (program_type, program_name, salary, duration, description, url) VALUES (?,?,?,?,?,?)' #baguhin
    values = (program_data['program_type'], program_data['program_name'],
              program_data['salary'], program_data['duration'],
              program_data['description'], program_data['url'])
    cur.execute(query,values)
    conn.commit()
    conn.close()

# This function updates a record
def update_program(program_data):
    conn, cur = connect_to_db(db_path)
    query = "UPDATE programs SET program_type=?, name=?, salary=?, duration=?, description=?, url=? WHERE id=?" #baguhin
    values = (program_data['program_type'], program_data['program_name'],
              program_data['salary'], program_data['duration'],
              program_data['description'], program_data['url'],
              program_data['program_id'])
    cur.execute(query, values)
    conn.commit()
    conn.close()