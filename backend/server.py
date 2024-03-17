from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import logging
from datetime import datetime
from schema import TaskSchema

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"]}})
# use sqlite as db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
taskSchema = TaskSchema()

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    due_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Task {self.title}>"

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'due_date': self.due_date.isoformat(),
            'status': self.status
        }

with app.app_context():
    db.create_all()

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    response = jsonify([task.to_dict() for task in tasks])
    return response

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get_or_404(task_id)
    return jsonify(task.to_dict())

@app.route('/tasks/add', methods=['POST'])
def create_task():
    data = request.json
    try:
        taskSchema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    if data['status'] not in ['TO DO', 'In Progress', 'Completed']:
        return jsonify({'error': 'Status is not valid'}), 400
    # creat new id for task 
    max_id = db.session.query(db.func.max(Task.id)).scalar()
    if max_id is None:
        id = 1
    else:
        id = max_id + 1
    task = Task(id=id, title=data['title'], description=data['description'], due_date=datetime.strptime(data['due_date'], '%Y-%m-%d'), status=data['status'])
    db.session.add(task)
    db.session.commit()
    response = jsonify(task.to_dict())
    return response, 201

@app.route('/tasks/update/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.json
    try:
        taskSchema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    task.title = data['title']
    task.description = data['description']
    task.due_date = datetime.strptime(data['due_date'], '%Y-%m-%d')
    task.status = data['status']
    if task.status not in ['TO DO', 'In Progress', 'Completed']:
        return jsonify({'error': 'Status is not valid'}), 400
    db.session.commit()
    return jsonify(task.to_dict())

@app.route('/tasks/delete/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)