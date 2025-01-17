import os
import subprocess
from datetime import datetime


def run_git_command(command: str, cwd: str, env: dict = None) -> str:
    """
    Run a Git command in the specified directory.
    :param command: Git command to execute.
    :param cwd: Directory containing the Git repository.
    :param env: Optional environment variables to set for the command.
    :return: Output of the Git command.
    """
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            env=env,  # Pass the environment variables if provided
            shell=True,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Git command failed: {command}\nError: {e.stderr.strip()}") from e


def auto_commit_and_push(repo_path: str, branch_name: str, old_date: str, commit_message: str = "Auto-commit"):
    """
    Automatically commits all changes in the repository and optionally pushes them to the remote.
    :param repo_path: Path to the Git repository.
    :param branch_name: Name of the new branch.
    :param commit_message: Commit message to use.
    """
    # Validate the date format
    print(f"Old date provided: {old_date}")
    try:
        datetime.strptime(old_date, "%Y-%m-%dT%H:%M:%S")  # Validate ISO 8601 format
    except ValueError as e:
        raise ValueError(f"Invalid date format: {old_date}. Use ISO 8601 format: YYYY-MM-DD HH:MM:SS") from e

    # Step 1: Ensure we're in a valid Git repository
    if not os.path.exists(os.path.join(repo_path, ".git")):
        raise FileNotFoundError(f"No Git repository found at {repo_path}")

    # Set custom commit date
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = old_date
    env["GIT_COMMITTER_DATE"] = old_date

    # Step 1.1 Create new branch
    run_git_command(f"git checkout -b {branch_name}", cwd=repo_path)
    # Step 2: Add all changes
    run_git_command("git add .", cwd=repo_path)
    print("All changes staged.")

    # Step 3: Commit changes
    run_git_command(f'git commit -m "{commit_message}"', cwd=repo_path, env=env)
    print(f"Changes committed with message: '{commit_message}'")

    # Step 4: Retrieve and log the commit SHA and ID
    commit_sha = run_git_command("git rev-parse HEAD", cwd=repo_path)
    commit_id = run_git_command("git log --format='%H' -n 1", cwd=repo_path)
    print(f"Commit successful!")
    print(f"Commit SHA: {commit_sha}")
    print(f"Commit ID: {commit_id}")

    # Step 5: Push changes to the remote repository
    run_git_command(f"git push -u origin {branch_name}", cwd=repo_path)
    print("Changes pushed to the remote repository.")


def main():
    # Path to your Git repository (PyCharm project directory)
    repo_path = os.path.abspath(os.path.dirname(__file__))  # Dynamically detects current script's directory
    git_path = '\\'.join(repo_path.split('\\')[:-2])
    print(f'git_path : {git_path}')
    changes_today = input("Hi Good day what all changes you have made today? \n")
    branch = changes_today.replace(' ', '_')
    old_date = "2025-01-17T09:00:00"
    commit_message = f"Auto-commit for {changes_today} "

    try:
        auto_commit_and_push(git_path, branch, old_date, commit_message)
    except Exception as e:
        print(f"Error during Git automation: {e}")


if __name__ == "__main__":
    main()
