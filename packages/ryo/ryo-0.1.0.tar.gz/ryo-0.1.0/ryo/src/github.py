import os
import subprocess
import time

class GitHubRepo:
    def __init__(self, repo_path,  base_path):
        self.repo_path = os.path.abspath(os.path.join(base_path, repo_path))
        self.repo_name = repo_path.split("/")[-1]
        self.base_path = base_path
        # self.workflows_availables = workflows_availables

        # print(f"----------------- GitHub Repo -----------------")
        # print(f"Repositório: {self.repo_name}")
        # print(f"Base Path: {self.base_path}")
        # print(f"Caminho: {self.repo_path}")
        # print(f"Workflows disponíveis: {self.workflows_availables}")

    def cd_repo_path(self):
        try:
            # print(f"Alterando diretório para: {self.repo_path}")
            os.chdir(self.repo_path)
            return True
        except FileNotFoundError:
            print("Repositório não encontrado.")
            return
    
    def run_command(self, command):
        """Executa um comando no shell e retorna a saída."""
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return result.stdout.strip(), result.stderr.strip()
        except subprocess.CalledProcessError as e:
            print(f"Erro ao executar comando: {command}\n{e}")
            return None

    
    def commit(self, commit_file, commit_message, auto_commit):
        """Realiza um commit no arquivo README.md para execução dos workflows."""
        print(f"\n Processando repositório: {self.repo_name}")
        
        print(f"\n------------------------ Run Commit -------------------------")

        self.cd_repo_path()

        print("------------------- Realizando o git pull -------------------")
        
        self.run_command("git pull")

        status_output, _ = self.run_command("git status --porcelain")
        if status_output:
            print("Existem alterações pendentes no repositório.")
        elif auto_commit.lower() == "true":
            print("-------------------- Alterando o arquivo --------------------")
            with open(commit_file, "a") as file:
                file.write(" ")
        else:
            print("-------------- Nenhuma alteração foi encontrada -------------")
            return

        print("------------- Adicionando o arquivo ao staging --------------")
        self.run_command("git add .")

        print("-------- Realizando o commit com a mensagem fornecida -------")
        self.run_command(f'git commit -m "{commit_message}"')

        print("--------------------- Realizando o push ---------------------")
        self.run_command("git push")

        print(f"Repositorio alterado e com a mensagem: '{commit_message}'.")
        os.chdir(self.base_path)

    def approve_pull_request(self, source_branch, target_branch):
        """Aprova um pull request."""
        
        print(f"\n----------------- Run Approve Pull Request ------------------")

        self.cd_repo_path()
        pr_number = ""
        if source_branch == "":
            source_branch, _ = self.run_command("git rev-parse --abbrev-ref HEAD")
            print("Branch atual:", source_branch)
        
        print(f"Verificando a existência de PR '{source_branch}' -> '{target_branch }'")        
        if "*" in target_branch and "*" not in source_branch:
            target_branch_base = target_branch.rstrip("*")
            comando = ['gh', 'pr', 'list', '--head', source_branch , '--json', 'number,baseRefName', '--jq', f'.[] | select(.baseRefName | startswith("{target_branch_base}")) | .number']

            pr_numbers, _ = self.run_command(comando)
            if pr_numbers:
                numeros_str = pr_numbers.strip().split('\n')
                numeros_int = [int(num) for num in numeros_str if num.strip()]
                pr_number = max(numeros_int)
        elif "*" in source_branch and "*" not in target_branch:
            source_branch_base = source_branch.rstrip("*")
            comando = ['gh', 'pr', 'list', '--base', target_branch , '--json', 'number,headRefName', '--jq', f'.[] | select(.headRefName | startswith("{source_branch_base}")) | .number']

            pr_numbers, _ = self.run_command(comando)
            if pr_numbers:
                numeros_str = pr_numbers.strip().split('\n')
                numeros_int = [int(num) for num in numeros_str if num.strip()]
                pr_number = max(numeros_int)
        elif "*" not in source_branch and "*" not in target_branch:
            comando = [ 'gh', 'pr', 'list', '--head', source_branch, '--base', target_branch, '--json', 'number', '--jq', '.[0].number']
            pr_number, _ = self.run_command(comando)
        else:
            print("Pelo menos um dos parâmetros não pode conter '*'")
            return
            
        if pr_number:
            print(f"------------- Um PR foi encontrado: #{pr_number} ------------")
            self.run_command(f"gh pr merge {pr_number} --merge")
            print("Merge realizado com sucesso.")
        else:
            print("------------ Nenhum PR encontrado foi encontrado ------------")
            return
        
    def workflow_monitor(self, workflow_name, show_workflow):
        """Monitora a execução de um workflow."""
        print(f"\n------------------- Run Workflow Monitor --------------------")
        self.cd_repo_path()

        print(f"Monitorando o workflow: {workflow_name}")
        # time.sleep(30)  

        if show_workflow.lower() == "true":
            print(f"Exibindo detalhes do workflow: {workflow_name}")

        while True:
            last_workflow_execution, _ = self.run_command(f"gh run list | grep '{workflow_name}' | head -n 1")

            if last_workflow_execution:
                elementos = last_workflow_execution.split('\t')
                status = elementos[0]
                result = elementos[1]
                workflow_id = elementos[6]

                if status == "completed":
                    print(f"O workflow foi concluido com status: {result}.")
                    if show_workflow.lower() == "true":
                        print(f"Exibindo detalhes do workflow: {workflow_id}")
                        self.run_command(f"gh run view {workflow_id} -w")
                    return
                elif status == 'cancelled':
                    print("O workflow foi cancelado.")
                    return
                elif status == 'skipped':
                    print("O workflow foi ignorado.")
                    return
                elif status == 'pending':
                    print("O workflow está pendente.")
                    print("Aguardando 30 segundos antes de verificar novamente.")
                    time.sleep(30)  
                elif status == 'queued':
                    print("O workflow está na fila.")
                    print("Aguardando 30 segundos antes de verificar novamente.")
                    time.sleep(30)
                elif status == 'in_progress':
                    print("O workflow está em andamento.")
                    print("Aguardando 30 segundos antes de verificar novamente.")
                    time.sleep(30)
                elif status == 'waiting':
                    print("O workflow está aguardando.")
                    print("Aguardando 30 segundos antes de verificar novamente.")
                    time.sleep(30)
                elif status == 'failure':
                    print("O workflow falhou.")
                    if show_workflow.lower() == "true":
                        print(f"Exibindo detalhes do workflow: {workflow_id}")
                        self.run_command(f"gh run view {workflow_id} -w")
                    return
                else:
                    print(f"Status desconhecido: {status}")
                    return
            else:
                print(f"Workflow '{workflow_name}' não encontrado.")
                return

