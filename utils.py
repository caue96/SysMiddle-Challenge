import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Variáveis de ambiente
TRELLO_API_KEY = os.getenv('TRELLO_API_KEY')
TRELLO_TOKEN = os.getenv('TRELLO_TOKEN')
ASANA_ACCESS_TOKEN = os.getenv('ASANA_ACCESS_TOKEN')
WORKSPACE_ID = os.getenv('WORKSPACE_ID')
TRELLO_BASE_API_URL = 'https://api.trello.com/1'
ASANA_BASE_API_URL = 'https://app.asana.com/api/1.0'

# Autentificação do Trello e Asana
def authenticate_trello():
    return {
        'key': TRELLO_API_KEY,
        'token': TRELLO_TOKEN
    }

def authenticate_asana():
    return {
        'Authorization': f'Bearer {ASANA_ACCESS_TOKEN}'
    }

# Leitura dos quadros do Trello
def get_trello_boards():
    auth = authenticate_trello()
    response = requests.get(f'{TRELLO_BASE_API_URL}/members/me/boards', params=auth)
    if response.status_code == 200:
        boards = response.json()
        if not boards:
            print(f"Não foi encontrado quadro.")
        return boards
    else:
        print(f"Falha na sincronização dos quadros. Código de status: {response.status_code}")
        print(f"Resposta: {response.text}")
        return []

# Criação de projetos no Asana
def create_asana_project(board_name, board_desc):
    headers = authenticate_asana()
    data = {
        'data': {
            'name': board_name,
            'notes': board_desc,
            'workspace': WORKSPACE_ID
        }
    }
    response = requests.post(f'{ASANA_BASE_API_URL}/projects', json=data, headers=headers)
    if response.status_code == 201:
        project = response.json()
        if not project.get('data'):
            print("Resposta na criação do projeto está vazia.")
            return None
        return project
    else:
        print(f"Falha na criação de projeto no Asana. Código de status: {response.status_code}")
        print(f"Resposta: {response.text}")
        return None

# Leitura das listas do Trello
def get_trello_lists(board_id):
    auth = authenticate_trello()
    response = requests.get(f'{TRELLO_BASE_API_URL}/boards/{board_id}/lists', params=auth)
    if response.status_code == 200:
        lists = response.json()
        if not lists:
            print(f"Sem listas achadas no quadro de ID {board_id}.")
        return lists
    else:
        print(f"Falha na sincronização das listas. Código de status: {response.status_code}")
        print(f"Resposta: {response.text}")
        return []

# Criação de seções no Asana
def create_asana_section(project_gid, list_name):
    headers = authenticate_asana()
    data = {
        'data': {
            'name': list_name
        }
    }
    response = requests.post(f'{ASANA_BASE_API_URL}/projects/{project_gid}/sections', json=data, headers=headers)
    if response.status_code == 201:
        section = response.json()
        if not section.get('data'):
            print("Resposta na criação da seção está vazia.")
            return None
        return section
    else:
        print(f"Falha na criação de seção no Asana. Código de status: {response.status_code}")
        print(f"Resposta: {response.text}")
        return None

# Leitura dos cartões do Trello
def get_trello_cards(list_id):
    auth = authenticate_trello()
    response = requests.get(f'{TRELLO_BASE_API_URL}/lists/{list_id}/cards', params=auth)
    if response.status_code == 200:
        cards = response.json()
        if not cards:
            print(f"Sem cartões achados na lista de ID {list_id}.")
        return cards
    else:
        print(f"Falha na sincronização dos cartões. Código de status: {response.status_code}")
        print(f"Resposta: {response.text}")
        return []

# Criação de tarefas no Asana
def create_asana_task(project_gid, section_gid, card_name, card_desc, card_due):
    headers = authenticate_asana()
    data = {
        'data': {
            'name': card_name,
            'notes': card_desc,
            'due_on': card_due,
            'workspace': WORKSPACE_ID,
            "memberships": [
                {
                    "project": project_gid,
                    "section": section_gid
                }
            ]
        }
    }
    response = requests.post(f'{ASANA_BASE_API_URL}/tasks', json=data, headers=headers)
    if response.status_code == 201:
        task = response.json()
        if not task.get('data'):
            print("Resposta na criação de tarefa está vazia.")
            return None
        return task
    else:
        print(f"Falha na criação de tarefa no Asana. Código de status: {response.status_code}")
        print(f"Resposta: {response.text}")
        return None