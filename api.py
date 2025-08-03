from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid

app = Flask(__name__)
CORS(app)  # Enable CORS for local development

# Mock user storage
users = []
# Mock task storage
tasks = []

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.json
    required_fields = ['name', 'password']
    if not all(field in data and data[field] for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    # Check for existing user
    if any(u["username"] == data.get("username") for u in users):
        return jsonify({"error": "Username already exists"}), 409

    user = {
        "id": str(uuid.uuid4()),
        "name": data.get("name"),
        "username": data.get("username", ""),
        "email": data.get("email", ""),
        "password": data.get("password")  # Note: Plaintext for mock only
    }
    users.append(user)
    return jsonify({"message": "User registered successfully"}), 201

@app.route('/api/signin', methods=['POST'])
def signin():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    for user in users:
        if user["username"] == username and user["password"] == password:
            return jsonify({"message": "Login successful", "user": user}), 200

    return jsonify({"error": "Invalid credentials"}), 401

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    status = request.args.get("status")
    if status in ["completed", "todo"]:
        filtered = [task for task in tasks if task["status"] == status]
        return jsonify(filtered)
    return jsonify(tasks)

@app.route('/api/tasks', methods=['POST'])
def add_task():
    data = request.json
    title = data.get("title")
    description = data.get("description", "")

    if not title:
        return jsonify({"error": "Title is required"}), 400

    task = {
        "id": str(uuid.uuid4()),
        "title": title,
        "description": description,
        "status": "todo"
    }
    tasks.append(task)
    return jsonify(task), 201

@app.route('/api/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.json
    for task in tasks:
        if task["id"] == task_id:
            task["title"] = data.get("title", task["title"])
            task["description"] = data.get("description", task["description"])
            task["status"] = data.get("status", task["status"])
            return jsonify(task)
    return jsonify({"error": "Task not found"}), 404

@app.route('/api/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task["id"] != task_id]
    return jsonify({"message": "Task deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)
