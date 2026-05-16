import json
import os
import argparse

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
            t['completed'] = True
            save_tasks(tasks)
            print(f"Tarefa {task_id} marcada como concluída!")
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

    args = parser.parse_args()

    if args.command == "add":
        add_task(args.title)
    elif args.command == "list":
        list_tasks()
    elif args.command == "complete":
        complete_task(args.id)
    elif args.command == "remove":
        remove_task(args.id)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
