import caretrack

tarefas = [
    "Beber 2 litros de água ao longo do dia",
    "Fazer 30 minutos de caminhada",
    "Alongamento de 10 minutos pela manhã",
    "Comer pelo menos uma fruta no almoço",
    "Pausa ergonômica a cada 1 hora de tela",
    "Dormir pelo menos 7 horas",
    "Tomar o medicamento da manhã",
    "Desligar as telas 30 minutos antes de dormir",
]

for t in tarefas:
    caretrack.add_task(t)

print("\nTarefas no banco:")
caretrack.list_tasks()
