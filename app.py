from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# 🔹 Create a new student
@app.route('/student', methods=['POST'])
def create_student():
    data = request.get_json()
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute("INSERT INTO students (student_id, first_name, last_name, dob, amount_due) VALUES (?, ?, ?, ?, ?)",
              (data['student_id'], data['first_name'], data['last_name'], data['dob'], data['amount_due']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Student added successfully'}), 201

# 🔹 Read all students
@app.route('/students', methods=['GET'])
def get_students():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute("SELECT * FROM students")
    rows = c.fetchall()
    conn.close()
    students = []
    for row in rows:
        students.append({
            'student_id': row[0],
            'first_name': row[1],
            'last_name': row[2],
            'dob': row[3],
            'amount_due': row[4]
        })
    return jsonify(students)

# 🔹 Read single student by ID
@app.route('/student/<int:student_id>', methods=['GET'])
def get_student(student_id):
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute("SELECT * FROM students WHERE student_id=?", (student_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return jsonify({
            'student_id': row[0],
            'first_name': row[1],
            'last_name': row[2],
            'dob': row[3],
            'amount_due': row[4]
        })
    else:
        return jsonify({'error': 'Student not found'}), 404

# 🔹 Update a student
@app.route('/student/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.get_json()
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute('''
        UPDATE students 
        SET first_name=?, last_name=?, dob=?, amount_due=?
        WHERE student_id=?
    ''', (data['first_name'], data['last_name'], data['dob'], data['amount_due'], student_id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Student updated successfully'})

# 🔹 Delete a student
@app.route('/student/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute("DELETE FROM students WHERE student_id=?", (student_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Student deleted successfully'})

# 🔹 Start the Flask app
if __name__ == '__main__':
    app.run(debug=True)
