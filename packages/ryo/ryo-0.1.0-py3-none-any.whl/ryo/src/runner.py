
from ryo.src.core import commit_file, workflow_monitor, approve_pull_request
from pathlib import Path
from ryo.src.github import GitHubRepo

def run_steps(task: dict, base_path: str ):
    """
    Execute the steps in the task.

    Args:
        task (dict): The task configuration.
    """
    task_repo = task.get("repository")
    steps = task.get("steps", [])

    for step in steps:
        action = step.get("action")
        step_repo = step.get("repository", '')
        repository = task_repo if step_repo == '' else step_repo
        repo = GitHubRepo(repo_path=repository, base_path=base_path)
        if action == "commit_file":
            commit_file(step, repo)
        elif action == "workflow_monitor":
            workflow_monitor(step, repo)
        elif action == "approve_pull_request":
            approve_pull_request(step, repo)
        else:
            print(f"Unknown action: {action}")


