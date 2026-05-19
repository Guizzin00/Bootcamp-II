from flask import Flask, render_template, jsonify, request
import caretrack
import sys
import io

# Forçar stdout para UTF-8 para evitar erros com emojis no Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    tasks = caretrack.load_tasks()
    return jsonify(tasks)

@app.route('/api/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    title = data.get('title', '')
    success = caretrack.add_task(title)
    if success:
        return jsonify({"status": "success", "message": "Tarefa adicionada."})
    return jsonify({"status": "error", "message": "Erro ao adicionar tarefa."}), 400

@app.route('/api/tasks/<int:task_id>/complete', methods=['POST'])
def complete_task(task_id):
    success = caretrack.complete_task(task_id)
    if success:
        return jsonify({"status": "success", "message": "Tarefa concluída."})
    return jsonify({"status": "error", "message": "Tarefa não encontrada."}), 404

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def remove_task(task_id):
    success = caretrack.remove_task(task_id)
    if success:
        return jsonify({"status": "success", "message": "Tarefa removida."})
    return jsonify({"status": "error", "message": "Tarefa não encontrada."}), 404

@app.route('/api/advice', methods=['GET'])
def get_advice():
    # Isso pode ser lento pois faz requisição à API externa
    status = caretrack.get_weather_advice()
    return jsonify({"status": status})

@app.route('/api/weather', methods=['GET'])
def get_weather():
    import urllib.request
    import json
    
    url = "https://api.open-meteo.com/v1/forecast?latitude=-23.5505&longitude=-46.6333&current=temperature_2m,relative_humidity_2m&daily=temperature_2m_max,temperature_2m_min&timezone=America%2FSao_Paulo"
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.loads(response.read().decode('utf-8'))
            return jsonify({
                "status": "success",
                "current": {
                    "temperature": data.get("current", {}).get("temperature_2m"),
                    "humidity": data.get("current", {}).get("relative_humidity_2m")
                },
                "daily": {
                    "time": data.get("daily", {}).get("time", [])[:5],
                    "temperature_2m_max": data.get("daily", {}).get("temperature_2m_max", [])[:5],
                    "temperature_2m_min": data.get("daily", {}).get("temperature_2m_min", [])[:5]
                }
            })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
