from flask import Flask, request, jsonify
from flask_cors import CORS
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__, static_folder='static')
metrics = PrometheusMetrics(app)
CORS(app)  

# In-memory task list
tasks = []

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    print("Received JSON:", data)  # Debug
    if data and 'task' in data:
        tasks.append(data['task'])
        return jsonify({'message': 'Task added'}), 201
    return jsonify({'error': 'No task provided'}), 400

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
        return jsonify({'message': 'Task deleted'})
    return jsonify({'error': 'Invalid task ID'}), 404

@app.route('/')
def home():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8080)
