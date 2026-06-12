import os
import argparse
import requests
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

def get_supabase_client():
    if not SUPABASE_URL or not SUPABASE_KEY:
        return None
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def load_tasks():
    client = get_supabase_client()
    if not client:
        return []
    try:
        response = client.table("tasks").select("*").order("id").execute()
        return response.data
    except Exception as e:
        print(f"Erro ao carregar tarefas: {e}")
        return []

def add_task(title):
    if not title.strip():
        print("Erro: A tarefa não pode ser vazia.")
        return False
    client = get_supabase_client()
    if not client:
        print("Erro: Banco de dados não configurado. Defina SUPABASE_URL e SUPABASE_KEY.")
        return False
    
    try:
        client.table("tasks").insert({"title": title.strip(), "completed": False}).execute()
        print(f"Tarefa adicionada: {title.strip()}")
        return True
    except Exception as e:
        print(f"Erro ao adicionar tarefa: {e}")
        return False

def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("Nenhuma tarefa de autocuidado registrada.")
        return []
    print("\n--- Sua Checklist de Autocuidado ---")
    for t in tasks:
        status = "[x]" if t.get('completed') else "[ ]"
        print(f"{t.get('id')} - {status} {t.get('title')}")
    print("------------------------------------\n")
    return tasks

def complete_task(task_id):
    client = get_supabase_client()
    if not client:
        print("Erro: Banco de dados não configurado.")
        return False
    
    try:
        response = client.table("tasks").select("completed").eq("id", task_id).execute()
        if not response.data:
            print(f"Erro: Tarefa {task_id} não encontrada.")
            return False
        
        current_status = response.data[0].get("completed", False)
        new_status = not current_status
        
        client.table("tasks").update({"completed": new_status}).eq("id", task_id).execute()
        state = "concluída" if new_status else "reaberta"
        print(f"Tarefa {task_id} marcada como {state}!")
        return True
    except Exception as e:
        print(f"Erro ao concluir tarefa: {e}")
        return False

def remove_task(task_id):
    client = get_supabase_client()
    if not client:
        print("Erro: Banco de dados não configurado.")
        return False
        
    try:
        response = client.table("tasks").select("id").eq("id", task_id).execute()
        if not response.data:
            print(f"Erro: Tarefa {task_id} não encontrada.")
            return False
            
        client.table("tasks").delete().eq("id", task_id).execute()
        print(f"Tarefa {task_id} removida com sucesso!")
        return True
    except Exception as e:
        print(f"Erro ao remover tarefa: {e}")
        return False

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
