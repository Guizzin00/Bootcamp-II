# CareTrack 💧

CareTrack é uma aplicação de Linha de Comando (CLI) simples e eficiente para gerenciar metas diárias de autocuidado e hidratação.

[![CI/CD Pipeline](https://github.com/Guizzin00/Bootcamp-II/actions/workflows/ci.yml/badge.svg)](https://github.com/Guizzin00/Bootcamp-II/actions/workflows/ci.yml)

## 📌 Problema Real

Com a rotina agitada de estudos e trabalho, muitas pessoas esquecem de tarefas fundamentais de autocuidado:
- Beber água frequentemente
- Fazer pausas ergonômicas
- Tomar medicamentos no horário

**A Solução:** O CareTrack permite o registro rápido e prático dessas tarefas no terminal, mantendo o usuário focado sem a distração de abrir uma interface gráfica complexa.

## 👥 Público-Alvo
Estudantes, desenvolvedores e profissionais com rotinas aceleradas que precisam de um lembrete rápido e livre de distrações visuais para manter hábitos saudáveis.

## 🚀 Funcionalidades
- Adicionar tarefas de autocuidado.
- Listar tarefas pendentes e concluídas.
- Marcar tarefas como concluídas.
- Remover tarefas.

## 🛠️ Tecnologias Utilizadas
- **Python 3** (Linguagem Principal)
- **pytest** (Testes Automatizados)
- **ruff** (Linting e Qualidade de Código)
- **GitHub Actions** (CI/CD Automático)

## 📦 Instalação

1. Clone este repositório:
   ```bash
   git clone https://github.com/Guizzin00/Bootcamp-II.git
   cd Bootcamp-II
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## ▶️ Como Executar

A aplicação é executada via linha de comando (`caretrack.py`).

**Adicionar uma tarefa:**
```bash
python caretrack.py add "Beber 2 litros de água"
```

**Listar tarefas:**
```bash
python caretrack.py list
```

**Concluir uma tarefa (pelo ID):**
```bash
python caretrack.py complete 1
```

**Remover uma tarefa (pelo ID):**
```bash
python caretrack.py remove 1
```

**Obter Recomendação Climática:**
Consulta a API Open-Meteo para retornar uma recomendação de hidratação baseada no clima atual.
```bash
python caretrack.py advice
```

## 🌐 Deploy (Distribuição)

Como se trata de uma aplicação CLI (Linha de Comando), a nossa "publicação" é realizada diretamente através de repositórios Git, permitindo que qualquer desenvolvedor possa clonar e rodar em seu próprio terminal.
Alternativamente, esta aplicação pode ser empacotada via Docker ou distribuída como pacote no PyPI.

Repositório Público do Projeto: [https://github.com/Guizzin00/Bootcamp-II](https://github.com/Guizzin00/Bootcamp-II)

## 🧪 Rodando os Testes

Para garantir que tudo funciona corretamente, utilize o `pytest`:
```bash
pytest
```

## 🧹 Rodando o Lint (Ruff)

Para verificar o padrão de código:
```bash
ruff check .
```

## 🏷️ Versão Atual
Consulte o arquivo `VERSION` para a versão atual.
Versão Semântica: **1.0.0**

## 👨‍💻 Autor
[Amanda Pacheco]
