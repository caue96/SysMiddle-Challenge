from datetime import datetime
import os
import subprocess
import sys

# Certifica que os pacotes necessários estão instalados
def install_dependencies():
    try:
        import requests
        import dotenv
    except ImportError:
        print("Pacotes necessários não encontrados. Instalando...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

# Chama a função para instalar as dependências
install_dependencies()

# Importa os módulos depois de garantir que os pacotes foram instalados
from utils import (
    get_trello_boards,
    get_trello_lists,
    get_trello_cards,
    create_asana_project,
    create_asana_section,
    create_asana_task,
)

def main():
    # Pega os quadros do Trello
    boards = get_trello_boards()
    for board in boards:
        board_name = board['name']
        board_desc = board.get('desc', '')

        # Cria os projetos no Asana
        project = create_asana_project(board_name, board_desc)
        project_gid = project['data']['gid']

        # Pega as listas do Trello
        lists = get_trello_lists(board['id'])
        for list_ in lists:
            list_name = list_['name']

            # Cria as seções no Asana
            section = create_asana_section(project_gid, list_name)
            section_gid = section['data']['gid']

            # Pega os cartões do Trello
            cards = get_trello_cards(list_['id'])
            for card in cards:
                card_name = card['name']
                card_desc = card.get('desc', '')
                card_due = card.get('due', None)

                if card_due:
                    try:
                        # Converte a data para o padrão ISO 8601
                        parsed_date = datetime.strptime(card_due, "%Y-%m-%dT%H:%M:%S.%fZ")
                        card_due = parsed_date.isoformat()
                    except ValueError:
                        print(f"Não pode ser convertido a data limite: {card_due}")

                # Cria as tarefas no Asana
                create_asana_task(project_gid, section_gid, card_name, card_desc, card_due)

if __name__ == '__main__':
    main()