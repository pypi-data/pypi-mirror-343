import os
from ryo.src.github import GitHubRepo


def commit_file(step: dict, repo: GitHubRepo):
    """
    Commit a file with a message.
    
    Args:
        step (dict): The step configuration containing file path and commit message.
    """
    file_path = step.get("file_path", "README.md") 
    commit_msg = step.get("commit_msg", "Update README.md") 
    auto_commit = step.get("auto_commit", "false")
    
    repo.commit(commit_file=file_path, commit_message=commit_msg, auto_commit=auto_commit)
 

def approve_pull_request(step: dict, repo: GitHubRepo):
    """
    Approve a pull request.
    
    Args:
        step (dict): The step configuration containing target branch.
    """
    target_branch = step.get("target_branch", "develop")
    source_branch = step.get("source_branch", "")
    repo.approve_pull_request(target_branch=target_branch, source_branch=source_branch)   
    

def workflow_monitor(step: dict, repo: GitHubRepo):
    """
    Monitor a workflow.
    
    Args:
        step (dict): The step configuration containing workflow name.
    """
    workflow_name = step.get("workflow_name")
    show_workflow = step.get("show_workflow", "false").lower()
    
    repo.workflow_monitor(workflow_name=workflow_name, show_workflow=show_workflow)


