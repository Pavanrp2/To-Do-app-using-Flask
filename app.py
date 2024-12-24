from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    tittle = db.Column(db.String(100), nullable = False)
    description = db.Column(db.Text, nullable = True)
    completed = db.Column(db.Boolean, default = False)
    
    def tasks_details(self):
       return {
           "id" : self.id,
           "tittle" : self.tittle,
           "description" : self.description,
           "completed" : self.completed
           } 

# from app_models import Task

#creating a new task
@app.route('/task', methods = ['POST'])
def create_task():
    try:
        data = request.get_json()
        if 'tittle' not in data:
            return jsonify({"error" : "tittle is required"}), 400
        
        existing_task = Tasks.query.filter_by(tittle = data['tittle']).first()
        if existing_task:
            return jsonify({"error" : "Task with tittle is already exists."})
        
        new_task = Tasks(
            tittle = data['tittle'],
            description = data.get('description', ''),
            completed = False
        )
        db.session.add(new_task)
        db.session.commit()
        return jsonify({"message" : "New task added success", "Task" : new_task.tasks_details()}), 201
    except Exception as e:
        return jsonify({"error" : "New task is not added"})
    

# get all tasks
@app.route('/tasks', methods = ['GET'])
def getTasks():
    try:
        tasks = Tasks.query.all()
        if not tasks:
            return jsonify({"message":"No tasks found."}), 404
        tasks_list = []
        for task in tasks:
            tasks_list.append(task.tasks_details())
        return jsonify(tasks_list), 200
    except Exception as e:
        return jsonify({"error":e})

# get specific task by ID
@app.route('/tasks/<int:task_id>', methods = ['GET'])
def getTask(task_id):
    try:
        task = Tasks.query.get(task_id)
        if not task:
            return jsonify({"message":"Task not found"}), 404
        return jsonify(task.tasks_details()), 200
    
    except Exception as e:
        return jsonify({"error":e}), 500

#  Update a task
@app.route('/tasks/<int:task_id>', methods = ['PUT'])
def update(task_id):
    try:
        task = Tasks.query.get(task_id)
        if not task:
            return jsonify({"message":"Task not found"})
        
        data = request.get_json()
        task.tittle = data.get('tittle', task.tittle)
        task.description = data.get('description', task.description)
        task.completed = data.get('completed', task.completed)
        db.session.commit()
        return jsonify({"message":"Task udated successfully", "Tasks": task.task.details()})
    
    except Exception as e:
        return jsonify({"error":e})

# Delete a task
@app.route('/tasks/<int:task_id>', methods = ['DELETE'])
def delete_task(task_id):
    try:
        data = Tasks.query.get(task_id)
        if not data:
            return jsonify({"message":"task not found."}), 404
        db.session.delete(data)
        db.session.commit()
        return jsonify({"message":"task deleted successfully."}), 200
    except Exception as e:
        return jsonify({"error": e})
    
    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8000)