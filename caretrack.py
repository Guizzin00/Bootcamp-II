import json
import os
import argparse
import requests

# Use /tmp directory if running on Vercel (read-only filesystem workaround)
if os.environ.get("VERCEL"):
    DB_FILE = "/tmp/caretrack_db.json"
else:
    DB_FILE = "caretrack_db.json"

def load_tasks():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_tasks(tasks):
    with open(DB_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

def add_task(title):
    if not title.strip():
        print("Erro: A tarefa não pode ser vazia.")
        return False
    tasks = load_tasks()
    new_id = 1 if not tasks else max(t['id'] for t in tasks) + 1
    tasks.append({"id": new_id, "title": title.strip(), "completed": False})
    save_tasks(tasks)
    print(f"Tarefa adicionada: {title.strip()}")
    return True

def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("Nenhuma tarefa de autocuidado registrada.")
        return []
    print("\n--- Sua Checklist de Autocuidado ---")
    for t in tasks:
        status = "[x]" if t['completed'] else "[ ]"
        print(f"{t['id']} - {status} {t['title']}")
    print("------------------------------------\n")
    return tasks

def complete_task(task_id):
    tasks = load_tasks()
    for t in tasks:
        if t['id'] == task_id:
            t['completed'] = not t['completed']
            save_tasks(tasks)
            state = "concluída" if t['completed'] else "reaberta"
            print(f"Tarefa {task_id} marcada como {state}!")
            return True
    print(f"Erro: Tarefa {task_id} não encontrada.")
    return False

def remove_task(task_id):
    tasks = load_tasks()
    new_tasks = [t for t in tasks if t['id'] != task_id]
    if len(tasks) == len(new_tasks):
        print(f"Erro: Tarefa {task_id} não encontrada.")
        return False
    save_tasks(new_tasks)
    print(f"Tarefa {task_id} removida com sucesso!")
    return True

def get_weather_advice():
    # São Paulo coordinates
    lat, lon = -23.5505, -46.6333
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        temp = data.get("current_weather", {}).get("temperature")
        
        print(f"\n🌍 Temperatura atual (São Paulo): {temp}°C")
        if temp and temp > 28:
            print("⚠️ ATENÇÃO: O clima está muito quente! Dobre sua ingestão de água hoje.")
            return "hot"
        elif temp and temp < 15:
            print("❄️ ATENÇÃO: O clima está frio. Não esqueça de se hidratar mesmo sem sede!")
            return "cold"
        else:
            print("✅ Clima ameno. Mantenha sua rotina normal de hidratação.")
            return "normal"
    except requests.RequestException:
        print("Erro ao buscar dados climáticos. Tente novamente mais tarde.")
        return "error"

def main():
    parser = argparse.ArgumentParser(description="CareTrack - Checklist de Autocuidado e Hidratação")
    subparsers = parser.add_subparsers(dest="command", help="Comandos disponíveis")

    add_parser = subparsers.add_parser("add", help="Adicionar uma nova tarefa")
    add_parser.add_argument("title", type=str, help="Título da tarefa")

    subparsers.add_parser("list", help="Listar todas as tarefas")

    complete_parser = subparsers.add_parser("complete", help="Marcar uma tarefa como concluída")
    complete_parser.add_argument("id", type=int, help="ID da tarefa")

    remove_parser = subparsers.add_parser("remove", help="Remover uma tarefa")
    remove_parser.add_argument("id", type=int, help="ID da tarefa")

    subparsers.add_parser("advice", help="Obter recomendação de hidratação baseada no clima")

    args = parser.parse_args()

    if args.command == "add":
        add_task(args.title)
    elif args.command == "list":
        list_tasks()
    elif args.command == "complete":
        complete_task(args.id)
    elif args.command == "remove":
        remove_task(args.id)
    elif args.command == "advice":
        get_weather_advice()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
