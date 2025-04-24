import yaml
import os
import argparse
from ryo.src.utils import get_task, convert_paths_in_config_file
from ryo.src.runner import run_steps

def main():
    parser = argparse.ArgumentParser(description="Um utilitário de linha de comando Ryo.")
    subparsers = parser.add_subparsers(dest="comando", help="Subcomandos disponíveis")

    task_parser = subparsers.add_parser("task", help="Acompanha a tarefa")
    task_parser.add_argument("nome", help="O nome da task a ser implementada")

    args = parser.parse_args()

    if args.comando == "task":
        task = get_task(args.nome)
        if task:
            run_steps(task, os.getcwd())
        else:
            print(f"Task '{args.nome}' não encontrada.")
        
    else:
        parser.print_help()

if __name__ == "__main__":
    main()


# import argparse

# def main():
#     parser = argparse.ArgumentParser(description='Uma ferramenta de linha de comando Ryo.')
#     parser.add_argument('--version', action='version', version='%(prog)s 0.1.0')
#     # Adicione outros argumentos conforme necessário
#     args = parser.parse_args()
#     print("Olá do Ryo!")

# if __name__ == '__main__':
#     main()