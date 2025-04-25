import argparse
from .git_handler import GitHandler
from .stackspot_service import StackspotService
from .commit_tool import CommitTool
from .config import load_stackspot_config

def main():
    parser = argparse.ArgumentParser(description="Commit and push to Git with an option to include the branch number in the message.")
    parser.add_argument("-b", "--branch", action="store_true", help="Include branch number in the message")
    args = parser.parse_args()
    config = load_stackspot_config()
    git_handler = GitHandler(include_branch_number=args.branch)
    stackspot_service = StackspotService(config)
    commit_tool = CommitTool(git_handler, stackspot_service)
    commit_tool.auto_commit()

if __name__ == "__main__":
    main()